__author__ = 'kartik'

from parser.base_parser import BaseParser

class WikipediaParser():
    def custom_init(self, article_title_id_filename):
        print "WikipediaParser:init"
        self.article_title_filename = article_title_id_filename
        pass


    # method to get the definitions
    def get_definitions(self, extractor_instance, raw_text):
        pass

    # method to get the non definitions
    def get_non_definitions(self, extractor_instance, article_title):
        pass

    def run(self):
        pass


