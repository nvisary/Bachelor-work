import xml.etree.ElementTree as ET
import os

FB2_TAG = "{http://www.gribuser.ru/xml/fictionbook/2.0}"
FB2_TYPE = "FB2"


class BookWorker:
    """Use to manipulate and parse books formats, etc fb2"""

    def __init__(self, book_path):
        self.book_path = book_path
        self.book_type = None

        filename, file_extension = os.path.splitext(self.book_path)
        if file_extension == ".fb2":
            self.book_type = FB2_TYPE

        self.book_tree = ET.parse(self.book_path)
        self.book_root = self.book_tree.getroot()

    def get_book_text(self):
        text = ""
        if self.book_type == FB2_TYPE:
            body = self.__get_fb2body()
            sections = body.findall(FB2_TAG + "section")
            for section in sections:
                for el in section:
                    if el is not None and el.text is not None:
                        text += el.text
        return text

    def get_book_title(self):
        title = ""
        if self.book_type == FB2_TYPE:
            body = self.__get_fb2body()
            title_tag = body.find(FB2_TAG + "title")
            if title_tag is not None:
                for el in title_tag:
                    title += el.text
                    title += "\n"

        return title

    def __get_fb2body(self):
        return self.book_root.find(FB2_TAG + "body")
