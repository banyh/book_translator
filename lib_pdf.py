import os
import fitz
import requests

WHITE, BLACK, GREY = (1, 1, 1), (0, 0, 0), (0.5, 0.5, 0.5)


def check_font_existence(font_file: str) -> bool:
    if os.path.exists(font_file):
        return True
    if font_file == 'NotoSerifCJKtc-Regular.otf':
        url = 'https://github.com/notofonts/noto-cjk/raw/refs/heads/main/Serif/OTF/TraditionalChinese/NotoSerifCJKtc-Regular.otf'
    elif font_file == 'NotoSansCJKtc-Regular.otf':
        url = 'https://github.com/notofonts/noto-cjk/raw/refs/heads/main/Sans/OTF/TraditionalChinese/NotoSansCJKtc-Regular.otf'
    else:
        raise ValueError(f'Only support font_file "NotoSerifCJKtc-Regular.otf" or "NotoSansCJKtc-Regular.otf"')
    resp = requests.get(url, allow_redirects=True)
    with open(font_file, 'wb') as f:
        f.write(resp.content)
    return True


class PdfBook():
    def __init__(self, filename: str):
        self.book = fitz.open(filename)
        check_font_existence('NotoSansCJKtc-Regular.otf')
        self.font = fitz.Font(fontfile="NotoSansCJKtc-Regular.otf")

    def extract_text(self) -> list[str]:
        text = []
        for page in self.book.pages():
            text_blocks = page.get_text('dict')['blocks']
            for block in text_blocks:
                if 'lines' not in block:
                    continue
                for ln in block['lines']:
                    text.append(''.join([span['text'] for span in ln['spans']]))
        return text

    def chunking_text(self, max_output_tokens: int = 128000):
        chunks = []
        for page in self.book.pages():
            text_blocks = page.get_text('dict')['blocks']
            texts = []
            for block in text_blocks:
                if 'lines' not in block:
                    continue
                texts.append('\n'.join([
                    ''.join([span['text'] for span in ln['spans']])
                    for ln in block['lines']
                ]))
            chunk = '\n'.join([f'<block>{t}</block>' for t in texts])
            chunks.append(chunk)
        return chunks

    def replace_text(self, new_chunks: list[str]):
        for page, chunk in zip(self.book.pages(), new_chunks):
            tw = fitz.TextWriter(page.rect)
            text_blocks = page.get_text('dict')['blocks']
            for block, new_text in zip(text_blocks, chunk.split('</block>')):
                if 'lines' not in block:
                    continue
                size = int(block['lines'][0]['spans'][0]['size'])
                new_text = new_text.replace('<block>', '').replace('\n', '').strip()
                page.draw_rect(block['bbox'], color=WHITE, fill=WHITE, overlay=True)
                tw.fill_textbox(block['bbox'], new_text, font=self.font, fontsize=size)
                tw.write_text(page)

    def save(self, filename: str):
        self.book.subset_fonts(verbose=True)
        self.book.save(filename)
