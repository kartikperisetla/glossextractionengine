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

# usage : run.py operation_mode file
# operation_mode : wiktionary / wikipedia
# file : wiktionary dump file or wikipedia dump file

MIN_SENTENCE_LEN = 3

# classs to handle startup of the framework
class StartupContext:
    def __init__(self):
        self.parser_collection = {}
        self.filter_collection = {}
    # These filters are consumed by BaseParser in apply_filter method

    # method that registers a parser to parse target file
    def register_parser(self, module_name, parser_class, target_file):
        key = module_name+":"+parser_class
        self.parser_collection[key] = target_file

    # def start(self):
    #     self.launch_parser()
    #     # self.launch_sampler()
    #     # self.launch_modeler()
    #     # self.launch_engine()

    def run(self):
        _wiktionary_parser_instance = WiktionaryParser("G:\wikitionary\workspace\enwiktionary-20141004-pages-articles.xml")

        _len_filter = LengthFilter()
        _len_filter.min_length = 3


        _wiktionary_parser_instance.filters_for_definitions.append(_len_filter)
        _wiktionary_parser_instance.filters_for_non_definitions.append(_len_filter)

        _wiktionary_parser_instance.start()


s=StartupContext()
s=s.run()
print "StartupContext: waiting after launching parser..."