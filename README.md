# 電子書翻譯小工具

### 目標：將 epub/pdf 格式的電子書，翻譯成繁體中文，盡量維持格式不變

### Getting Start

1. `pip install -r requirements.txt`
   Installing dependencies
2. Set your OpenAI API key in `openai_apikey` in `settings.py`
3. Run `python book_translator.py {filename}`
    epub and pdf files are supported now
