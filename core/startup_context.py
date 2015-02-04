__author__ = 'kartik'

import os, sys
import xml
import importlib
import parser
from parser import *


# adding parser package to path
sys.path.append("../parser")
sys.path.append("../filter")

from parser.wiktionary_parser import WiktionaryParser
from parser.wikipedia_parser import WikipediaParser
from filter.length_filter import *
from utils.dynamic_class_loader import DynamicClassLoader

# usage : startup_context.py operation_mode file
# operation_mode : wiktionary / wikipedia
# file : wiktionary dump file or wikipedia dump file

MIN_SENTENCE_LEN = 3

# classs to handle startup of the framework
class StartupContext:
    def __init__(self):
        self.parser_collection = {}
        self.filter_collection = {}
        self.transformation_collection = {}
    # These filters are consumed by BaseParser in apply_filter method

    # # method that registers a parser to parse target file
    # # params: parser_class- full class name including package and module name
    # def register_parser(self, parser_class, target_file, filter_list, transformation_list):
    #     key = parser_class
    #     self.parser_collection[key] = target_file
    #
    # # method to instantiate a class instance
    # def get_instance(self, class_name):
    #     _loader = DynamicClassLoader()
    #     _class_placeholder = _loader.load(class_name)
    #     _instance = _class_placeholder()
    #
    # # method to launch registered parsers
    #     if len(self.parser_collection.keys())>0:
    #         for class_name, target_file in self.parser_collection.iteritems():
    #             _instance = self.get_instance(class_name)

    # def start(self):
    #     self.launch_parser()
    #     # self.launch_sampler()
    #     # self.launch_modeler()
    #     # self.launch_engine()

    def run(self, file_name):
        # _wiktionary_parser_instance = WiktionaryParser("G:\wikitionary\workspace\enwiktionary-20141004-pages-articles.xml")

        _wiktionary_parser_instance = WiktionaryParser(file_name)
        _len_filter = LengthFilter()
        _len_filter.min_length = 3


        _wiktionary_parser_instance._definition_score = "1"
        _wiktionary_parser_instance._nondefinition_score = "-1"
        _wiktionary_parser_instance.filters_for_definitions.append(_len_filter)
        _wiktionary_parser_instance.filters_for_non_definitions.append(_len_filter)

        _wiktionary_parser_instance.start()


if __name__=="__main__":
    _file_name = sys.argv[1]
    s=StartupContext()
    s=s.run(_file_name)
    print "StartupContext: waiting after launching parser..."