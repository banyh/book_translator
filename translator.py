from openai import OpenAI
import sqlite3
import settings


class StringCache():
    def __init__(self, db_path='translator_cache.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cache (
                input TEXT PRIMARY KEY,
                output TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def get(self, input_text):
        self.cursor.execute('SELECT output FROM cache WHERE input = ?', (input_text,))
        row = self.cursor.fetchone()
        return row[0] if row else None

    def set(self, input_text, output_text):
        self.cursor.execute('REPLACE INTO cache (input, output) VALUES (?, ?)', (input_text, output_text))
        self.conn.commit()

    def purge(self, period_days: int = 30):
        self.cursor.execute('DELETE FROM cache where updated_at < datetime("now", "-{period_days} days")')
        self.conn.commit()


class ChatGPT():
    def __init__(self,
            api_key=settings.openai_apikey,
            model=settings.openai_model,
            system_prompt=settings.system_prompt,
            user_prompt=settings.user_prompt,
        ):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt
        self.input_tokens = 0
        self.output_tokens = 0
        self.cache = StringCache()
        self.cache.purge()

    def cost(self):
        MODEL_PRICING = {
            'gpt-4o': (2.50, 10.00),
            'gpt-4.1': (2.00, 8.00),
            'gpt-4.1-mini': (0.40, 1.60),
            'gpt-4.1-nano': (0.10, 0.40),
            'gpt-5.2': (1.75, 14.00),
            'gpt-5.2 pro': (21.00, 168.00),
            'gpt-5': (1.25, 10.00),
            'gpt-5-mini': (0.25, 2.00),
            'gpt-5-nano': (0.05, 0.40),
            'gpt-5-pro': (15.00, 120.00),
        }
        input_price, output_price = MODEL_PRICING.get(self.model, (0.0, 0.0))
        return (
            (self.input_tokens / 1000000) * input_price +
            (self.output_tokens / 1000000) * output_price
        )

    def chat_complete(self, text):
        ret = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"{self.user_prompt}: \n{text}"}
            ],
        )
        self.input_tokens += ret.usage.prompt_tokens
        self.output_tokens += ret.usage.completion_tokens
        output = ret.choices[0].message.content
        self.cache.set(text, output)
        return output


if __name__ == "__main__":
    translator = ChatGPT(settings.openai_apikey, settings.openai_model,
                        settings.system_prompt, settings.user_prompt)
    translator.chat_complete("兄弟，我们当冒险者是为了什么？")
    translator.chat_complete("GPT-5 mini is a faster, more cost-efficient version of GPT-5.")
