__author__ = 'kartik'

import os, sys
import xml
import parser
import importlib

# adding parser package to path
sys.path.append("../parser")
sys.path.append("../filter")


# usage : run.py operation_mode file
# operation_mode : wiktionary / wikipedia
# file : wiktionary dump file or wikipedia dump file

MIN_SENTENCE_LEN = 3

# classs to handle startup of the framework
class StartupContext:
    def __init__(self):
        self.parser_collection = {}
        self.filter_collection = {}

    # method that registers a filter
    # param:
    # module_name: name of the module where filter class is located
    # filter_class: name of the filter class in provided module
    def register_filter(self, module_name, filter_class_name):
        key = module_name+":"+filter_class_name

        module = __import__(module_name)
        filter_class = getattr(module, filter_class_name)
        _filter_instance = filter_class()
        _filter_instance.min_length = MIN_SENTENCE_LEN
        self.filter_collection[key] = _filter_instance


    # These filters are consumed by BaseParser in apply_filter method

    # method that registers a parser to parse target file
    def register_parser(self, module_name, parser_class, target_file):
        key = module_name+":"+parser_class
        self.parser_collection[key] = target_file

    # method that launches parser threads
    def launch_parser(self):
        for key, target_file in self.parser_collection.iteritems():
            items = key.split(":")
            module_name = items[0]
            module = __import__(module_name)
            parser_class = items[1]
            _class = getattr(module, parser_class)

            # dynamic instantiation of instance
            instance = _class(target_file)
            # providing parser instance with registered filters
            instance.filter_collection = self.filter_collection
            # start the parser thread
            instance.start()


    def start(self):
        self.launch_parser()
        # self.launch_sampler()
        # self.launch_modeler()
        # self.launch_engine()

    def run(self):
        self.register_parser("wiktionary_parser", "WiktionaryParser","G:\wikitionary\workspace\enwiktionary-20141004-pages-articles.xml")

        self.register_filter("length_filter","LengthFilter")

        self.start()

s=StartupContext()
s=s.run()
print "after run..."