openai_apikey = ''

openai_model = 'gpt-5-nano'  # 要選用的模型，以翻譯來說，專有名詞不多的情況用 nano 比較便宜

system_prompt = """你是一位專業的翻譯員，精通多種語言之間的翻譯。
請根據使用者提供的提示，將文本準確且流暢地翻譯成目標語言，同時保留原文的格式和標點符號。
保留格式指的是：保留Markdown、程式碼區塊、HTML標籤…等。
對於類似英文的文本，請自動識別行尾的斷行，並將其合併為完整的句子翻譯，但輸出時要保留斷行符號。
如果原文用<block></block>標籤包裹，請在翻譯後的文本中也使用相同的標籤包裹。"""

user_prompt = """將下列文字翻譯成繁體中文，翻譯時應盡可能使用台灣習慣詞語。"""

# Whether to output bilingual text or just translated text, set to "True" or "False"
bilingual_output = False

# Language code of the output epub file, e.g. "en", "zh-cn", "ja"
langcode = 'zh-tw'

# Translation begins from the specified start page number and is
# exclusively available for PDF files.
startpage = 1

# Translation will continue until the specified page number in
# a PDF file. This feature supports PDF files exclusively.
# If the input is equal to -1, the translation will proceed until
# the end of the file.
endpage = -1

# Foreign language transliteration list, a xlsx file.
# For example in the sample from English to simplified Chinese
transliteration_list = 'transliteration-list-example.xlsx'

# Whether case matching is enabled by transliteration
# list replacement, set to "True" or "False"
case_matching = True
