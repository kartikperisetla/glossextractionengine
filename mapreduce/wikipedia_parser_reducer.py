__author__ = 'kartik'

#!/usr/bin/env python
import sys,re
import cStringIO
import xml.etree.ElementTree as xml
from extractor.wikipedia_extractor import WikipediaExtractor


class WikipediaParserReducer:
    def __init__(self):
        self.buff = cStringIO.StringIO()
        self.article_title = False
        self.article_raw_text = False

    def process(self):
        _wikipedia_extractor = WikipediaExtractor()
        def_list = _wikipedia_extractor.get_definitions(self.article_raw_text)
        non_def_list = _wikipedia_extractor.get_non_definitions(self.article_raw_text)


if __name__ == '__main__':
    _instance = WikipediaParserReducer()

    for line in sys.stdin:
        items = line.split("\t")
        _instance.article_title = items[0]
        _instance.article_raw_text = items[1]
