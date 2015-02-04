#!/usr/bin/python

__author__ = 'kartik'

import os, sys
# add library to path
# sys.path.insert(0, 'glossextractionengine.mod')

import xml
import parser

# adding parser package to path
sys.path.append("../parser")
sys.path.append("../filter")
sys.path.append("../utils")
sys.path.append("../extractor")
sys.path.append("../transformation")

from wiktionary_extractor import WiktionaryExtractor
from wiktionary_parser import WiktionaryParser
from wikipedia_parser import WikipediaParser
from length_filter import *
from dynamic_class_loader import DynamicClassLoader
from wiktionary_definition_transformation import  WiktionaryDefinitionTransformation

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


    def run(self, file_name):
        # _wiktionary_parser_instance = WiktionaryParser("G:\wikitionary\workspace\enwiktionary-20141004-pages-articles.xml")

        _wiktionary_parser_instance = WiktionaryParser(file_name)
        _len_filter = LengthFilter()
        _len_filter.min_length = 3


        _wiktionary_parser_instance._definition_score = "1"
        _wiktionary_parser_instance._nondefinition_score = "-1"
        _wiktionary_parser_instance.filters_for_definitions.append(_len_filter)
        _wiktionary_parser_instance.filters_for_non_definitions.append(_len_filter)

        _definition_transformation = WiktionaryDefinitionTransformation()

        _wiktionary_parser_instance.transformations_for_definitions.append(_definition_transformation)

        _wiktionary_parser_instance.start()


if __name__=="__main__":
    _file_name = sys.argv[1]
    s=StartupContext()
    s=s.run(_file_name)
    print "StartupContext: waiting after launching parser..."