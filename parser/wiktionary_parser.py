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

        print "WiktionaryParser:init"

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

            # get definitions
            self.get_definitions(_extractor_instance, _article_raw_text)

            # get non definitional sentences
            self.get_non_definitions(_extractor_instance, self.title)

            # clear the content buffer
            self.flush()

    # method to get the definitions
    def get_definitions(self, extractor_instance, raw_text):
        _def_list = extractor_instance.get_definitions(raw_text)
        if not _def_list is None:
            _def_set = set(_def_list)
            if len(_def_set) != 0:
                _buffered_result = ""
                for definition_instance in _def_set:
                    # apply the length filter on each sentence
                    if self.apply_filter(self.filters_for_definitions, definition_instance):
                        try:
                            # filtering out titles containing KEYWORD
                            if not WIKTIONARY_TITLE_KEYWORD in self.title.lower():
                                _buffered_result += "1 '" + self.title.strip() + " | " + definition_instance + "\n"
                        except:
                            pass
                # save the definitions
                self.save_definitions(_buffered_result)

    # method to get the non definitions
    def get_non_definitions(self, extractor_instance, article_title):
        _non_def_result = extractor_instance.get_non_definitions(article_title)
        if not _non_def_result is None:
            _buffered_result = ""
            if len(_non_def_result) > 0:
                for non_definition_instance in _non_def_result:
                    if self.apply_filter(self.filters_for_non_definitions, non_definition_instance):
                        _buffered_result += "0 '" + article_title.encode("utf-8") + " | " + str(non_definition_instance) + "\n"

                # save the non definitions
                self.save_non_definitions(_buffered_result)

    def run(self):
        parser = xml.sax.make_parser()
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)

        Handler = self
        parser.setContentHandler(Handler)
        print "wiktionary_parser:run:parsing start"
        parser.parse(self.file_name)
        print "wiktionary_parser:run:parsing complete!"