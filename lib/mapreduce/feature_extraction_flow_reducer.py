#!/usr/bin/python
import sys
import re
import cStringIO
# add library to path
sys.path.insert(0, 'glossextractionengine.mod')

class FeatureExtractionFlowReducer:
    def process(self, line):
        try:
            if line.strip()!="":
                _collection = line.split("\t")
                word = _collection[0]
                category = _collection[1]
                feature_dict = _collection[2]

                feature_category_tuple = (feature_dict,category.strip())
                print feature_category_tuple
        except Exception as ex:
            print>>sys.stderr, ex.message,"\n for :",line


if __name__ == '__main__':
    _instance = FeatureExtractionFlowReducer()

    # a single line is <category> '<instance_name> | <instance>
    for line in sys.stdin:
        line = line.strip()
        _instance.process(line)