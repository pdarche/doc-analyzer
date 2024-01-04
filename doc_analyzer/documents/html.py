import os
import shutil
from ..documents.base import BaseDocument
from ..processors.html import HtmlProcessor
from ..utils import html

PROCESSORS = {
    'bs4': HtmlProcessor
}


class HtmlDocument(BaseDocument):
    """
    HTML document type
    """
    def __init__(self, name, uri, processor='bs4', bucket=None):
        self.name = name
        self.uri = uri
        self.bucket = bucket
        
        # Private attributes 
        self.table_text = "" 
        self.line_text = "" 
        self.pages = {} 
 
        # Set the data directory and source document path
        self.datadir = f".{self.name}__html"
        self.source_path = f"{self.datadir}/{self.name}.html" 
        self.processor = PROCESSORS[processor](self.datadir, self.source_path, bucket=bucket)

        # If the data directory doesn't exist, make the directories; otherwise load from pickles 
        # TODO: check to see if the data exists in s3
        if not os.path.exists(self.datadir):
            self._mkdirs()

        self.download()

    @property
    def text(self):
        return self.line_text

    def download(self, sync=False):
        if not os.path.exists(self.source_path):
            html.copy_html(self.uri, self.source_path)
        else:
            print("File exists locally, skipping download")
        
        if sync:
            self.sync()

    def split(self):
        print("Splitting (i.e. copying)")
        destination_path = f"./{self.datadir}/subdocs/subdoc_1.html"
        shutil.copy(self.source_path, destination_path)

    def process(self, sync=False):
        self.processor.process()
        # Set the line text
        text, page_text = self.processor.get_text()
        self.line_text = text
        self.pages = page_text