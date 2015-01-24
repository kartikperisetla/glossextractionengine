__author__ = 'kartik'

import os, sys
import xml
import parser
import importlib

# adding parser package to path
sys.path.append("../parser")

# usage : run.py operation_mode file
# operation_mode : wiktionary / wikipedia
# file : wiktionary dump file or wikipedia dump file

# classs to handle startup of the framework
class Startup:
    def __init__(self):
        self.parser_collection = {}

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
            instance.start()


    def start(self):
        self.launch_parser()
        # self.launch_sampler()
        # self.launch_modeler()
        # self.launch_engine()

    def run(self):
        self.register_parser("wiktionary_parser", "WiktionaryParser","G:\wikitionary\workspace\enwiktionary-20141004-pages-articles.xml")
        self.start()

s=Startup()
s=s.run()
print "after run..."