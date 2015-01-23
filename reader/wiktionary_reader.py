#!/usr/bin/env python
# -*-coding: utf-8-*-

__author__ = 'kartik'
import sys, xml.sax, re
import codecs
import wikipedia
from base_reader import BaseReader
from utils.wikipedia_util import WikipediaConnector
from extractor.wiktionary_extractor import WiktionaryExtractor

WIKTIONARY_TITLE_KEYWORD = "wiktionary"

class WiktionaryReader(BaseReader):
    #constructor
    def __init__(self):
            self.CurrentData = ""
            self.title = None
            self.text = None
            self.file = open("result.txt", "w")

    # when parser comes across starting of an element
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if self.CurrentData == "title":
            self.title = ""
        if self.CurrentData == "text":
            self.text = ""

    # Call when a character is read
    def characters(self, content):
        if self.CurrentData == "title":
            self.title += content
        elif self.CurrentData == "text":
            self.text += content


    # when parser comes across ending of an element
    def endElement(self, tag):
        if self.CurrentData == "title":
            pass
        elif self.CurrentData == "text":    # reading the text of the article
            _article_raw_text = self.text.encode('utf-8')

            # invoking method to get definitions from article body
            _extractor_instance = WiktionaryExtractor()
            _def_list = _extractor_instance.get_definitions(_article_raw_text)

            if not _def_list is None:
                _def_set = set(_def_list)
                if len(_def_set) != 0:
                    for definition_instance in _def_set:
                        try:
                            # filtering out titles containing KEYWORD
                            if not WIKTIONARY_TITLE_KEYWORD in self.title.lower():
                                print self.title + "| " + definition_instance
                        except:
                            pass

            # get non definitional sentences
            self.getNonDefinitional(self.title)
        # clear the content buffer
        self.CurrentData = ""

    # method to capture non definitional sentences for this title
    def getNonDefinitional(self, title):
        if title.strip() == "":
            return

        w = WikipediaConnector()
        result = w.get_non_definitional_sentences_for_article(title)
        if result is None:
            return

        f = open("non-def.txt", "a")
        buff = ""
        if len(result) > 0:
            for line in result:
                buff += "0 | " + str(line).decode('utf-8') + "\n"
            f.write(buff.encode('utf-8'))
            f.close()

