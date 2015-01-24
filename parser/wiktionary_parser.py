#!/usr/bin/env python
# -*-coding: utf-8-*-

__author__ = 'kartik'
import sys, xml.sax, re
import codecs
import wikipedia
from base_parser import BaseParser
from utils.wikipedia_util import WikipediaConnector
from extractor.wiktionary_extractor import WiktionaryExtractor

WIKTIONARY_TITLE_KEYWORD = "wiktionary"

# class to parse wiktionary dataset
class WiktionaryParser(BaseParser,xml.sax.ContentHandler):
    # #constructor
    # def __init__(self, file_name):
    #     # invoking base class constructor
    #     super(WiktionaryParser, self).__init__(file_name)
    #     self.custom_init(file_name)

    def custom_init(self, file_name):
        self.current_data = ""
        self.title = None
        self.text = None
        self.file_name = file_name

        print "\nWiktionaryParser:init"

    # when parser comes across starting of an element
    def startElement(self, tag, attributes):
        self.current_data = tag
        if self.current_data == "title":
            self.title = ""
        if self.current_data == "text":
            self.text = ""

    # Call when a character is read
    def characters(self, content):
        if self.current_data == "title":
            self.title += content
        elif self.current_data == "text":
            self.text += content

    # method to clean the content buff
    def flush(self):
        self.current_data = ""

    # when parser comes across ending of an element
    def endElement(self, tag):
        if self.current_data == "title":
            pass
        elif self.current_data == "text":    # reading the text of the article
            _article_raw_text = self.text.encode('utf-8')
            self.title = self.title.strip()

            # invoking method to get definitions from article body
            _extractor_instance = WiktionaryExtractor()
            _def_list = _extractor_instance.get_definitions(_article_raw_text)

            if not _def_list is None:
                _def_set = set(_def_list)
                if len(_def_set) != 0:
                    _buffered_result = ""
                    for definition_instance in _def_set:
                        try:
                            # filtering out titles containing KEYWORD
                            if not WIKTIONARY_TITLE_KEYWORD in self.title.lower():
                                _buffered_result += self.title.strip() + "| " + definition_instance + "\n"
                        except:
                            pass
                    # save the definitions
                    self.save_definitions(_buffered_result)

            # get non definitional sentences
            _buffered_result = _extractor_instance.extract_non_definitions(self.title)
            if not _buffered_result is None:
                # save the non definitions
                self.save_non_definitions(_buffered_result)

            # clear the content buffer
            self.flush()

    def run(self):
        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)

        Handler = self
        parser.setContentHandler(Handler)
        print "\nwiktionary_parser:run:parsing start"
        parser.parse(self.file_name)
        print "\nwiktionary_parser:run:parsing complete!"