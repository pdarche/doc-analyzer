from bs4 import BeautifulSoup
import html2text
import shutil
from ..processors.base import BaseProcessor


class HtmlProcessor(BaseProcessor):
    def __init__(self, datadir, source_path, bucket=None):
        super().__init__(datadir, source_path, bucket=bucket)

    def process(self):
        if not self.num_subdocs:
            self._split()
            self._set_num_subdocs()

    def get_text(self):
        """ Constructs the text from the document """
        page_text = {}
        if self.num_texts:
            print("Text files exist, not extracting")
            for subdoc_num in range(1, self.num_texts+1):
                with open(f"./{self.datadir}/lines/subdoc_{subdoc_num}.txt", 'r') as file:
                    line_text = file.read()
                    page_text[subdoc_num] = line_text

        else:
            print("Text files do not, extracting")
            for subdoc_num in range(1, self.num_subdocs+1):
                html_path = f"./{self.datadir}/subdocs/subdoc_{subdoc_num}.html"
                with open(html_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                soup = BeautifulSoup(content, 'html.parser')
                line_text = html2text.html2text(str(soup))
                page_text[subdoc_num] = line_text
                with open(f"./{self.datadir}/lines/subdoc_{subdoc_num}.txt", 'w') as file:
                    file.write(line_text)
        full_text = "\n".join(page_text.values())
        return full_text, page_text

    def _split(self, pages_per_subdoc=1):
        """ Splits the PDF into n subdocs to simplify processing and attribution """
        if not self.num_subdocs:
            print("Splitting")
            destination_path = f"./{self.datadir}/subdocs/subdoc_1.html"
            shutil.copy(self.source_path, destination_path)
        else:
            print("Subdocs already created, skipping")
