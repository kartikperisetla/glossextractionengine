__author__ = 'kartik'

import re
from utils.wikimarkup_handler import WikiMarkupParser

# class to perform extraction operations on wikipedia raw article text
class WikipediaExtractor:
    def __init__(self):
        self.def_list = None
        self.non_def_list = None
        pass

    # generic method to extract definitions for noun, adjective word
    # params: raw text of wikipedia article, word type
    # raw is article text where ]n is replaced by space
    def extract_sentences(self, raw):
        _wiki_parser = WikiMarkupParser()
        # remove the wikipedia markup from raw article text
        clean_raw =_wiki_parser.parse_string(raw)
        # split raw article text into lines
        lines = clean_raw.split(".")
        self.def_list = lines[0:1]
        self.non_def_list = lines[1:]

    # method to extract definitions from raw article text
    # params: raw text of wikipedia article
    def get_definitions(self, raw):
        if not self.def_list is None:
            return self.def_list

        self.extract_sentences(raw)
        return self.def_list

    # method to extract non definitions from raw article text
    # params: raw text of wikipedia article
    def get_non_definitions(self, raw):
        if not self.non_def_list is None:
            return self.non_def_list

        self.extract_sentences(raw)
        return self.non_def_list
