__author__ = 'kartik'

import os, sys
import xml
from parser.wiktionary_parser import WiktionaryParser

# usage : run.py operation_mode file
# operation_mode : wiktionary / wikipedia
# file : wiktionary dump file or wikipedia dump file

if (__name__ == "__main__"):
    # print sys.argv
    # print sys.argv[1]
    file_name = sys.argv[1]

    # create an XMLReader
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    Handler = WiktionaryParser()
    parser.setContentHandler(Handler)
    parser.parse(file_name)