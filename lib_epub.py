from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup


class EpubBook():
    def __init__(self, filename: str):
        self.book = epub.read_epub(filename)
        self.items = [item for item in self.book.get_items()]
        self.documents = [item for item in self.items if item.get_type() == ITEM_DOCUMENT]

    def extract_text(self) -> list[str]:
        text = []
        for item in self.documents:
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            for string in soup.strings:
                if len(string.strip()) > 0:
                    text.append(string.strip())
        return text

    def chunking_text(self, max_output_tokens: int = 128000):
        threshold = max_output_tokens * 0.25
        text = self.extract_text()
        chunks = []
        chunk = []
        for i in range(len(text)):
            chunk.append(text[i])
            if sum(len(c) + 1 for c in chunk) > threshold:
                chunks.append('\n'.join(chunk))
                chunk.clear()
        if len(chunk) > 0:
            chunks.append('\n'.join(chunk))
        return chunks

    def replace_text(self, new_chunks: list[str]):
        new_texts = [line for ch in new_chunks for line in ch.split('\n')]
        for doc in self.documents:
            soup = BeautifulSoup(doc.get_content(), 'html.parser')
            for string in soup.strings:
                if len(string.strip()) == 0:
                    continue
                new_string = new_texts.pop(0)
                string.replace_with(new_string)
            doc.set_content(str(soup).encode('utf-8'))

    def save(self, filename: str):
        epub.write_epub(filename, self.book)


if __name__ == "__main__":
    book = EpubBook("test.epub")
    texts = book.extract_text()
    for i in range(10):
        texts[i] = f"這是測試第 {i} 行"
    book.replace_text(texts)
    book.save("test_modified.epub")
