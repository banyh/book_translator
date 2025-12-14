from translator import ChatGPT
from lib_epub import EpubBook
from lib_pdf import PdfBook
from tqdm import tqdm
import sys
import os
import settings


def translate_book(input_file: str, output_file: str):
    gpt = ChatGPT(settings.openai_apikey, settings.openai_model,
                  settings.system_prompt, settings.user_prompt)
    if input_file.endswith('.epub'):
        book = EpubBook(input_file)
    elif input_file.endswith('.pdf'):
        book = PdfBook(input_file)
    else:
        print("Unsupported file format. Please use .epub or .pdf files.")
        return

    new_chunks = []
    chunks = book.chunking_text()
    for chunk in tqdm(chunks, desc="Translating"):
        new_chunks.append(gpt.chat_complete(chunk))
    book.replace_text(new_chunks)
    book.save(output_file)
    print(f'Translated book saved to {output_file}')
    print(f"Total cost: ${gpt.cost():.4f} (約 NT${gpt.cost()*30:.0f})")


if __name__ == "__main__":
    for filename in sys.argv[1:]:
        _, ext = os.path.splitext(filename)
        if ext not in ['.epub', '.pdf']:
            continue
        output_filename = filename.replace(ext, f'_翻譯{ext}')
        translate_book(filename, output_filename)
