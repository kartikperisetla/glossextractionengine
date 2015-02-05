#!/usr/bin/python
import sys
import re
import cStringIO


# add library to path
sys.path.insert(0, 'glossextractionengine.mod')

class FeatureExtractionFlowReducer:
    def process(self, line):
        _collection = line.split("\t")
        category = _collection[0]
        feature_dict = _collection[1]

        feature_category_tuple = (feature_dict,category)
        print feature_category_tuple,"\n"


if __name__ == '__main__':
    _instance = FeatureExtractionFlowReducer()

    # a single line is <category> '<instance_name> | <instance>
    for line in sys.stdin:
        line = line.strip()
        _instance.process(line)