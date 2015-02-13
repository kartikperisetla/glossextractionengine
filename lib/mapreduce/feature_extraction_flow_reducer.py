#!/usr/bin/python
import sys
import re
import cStringIO
# add library to path
sys.path.insert(0, 'glossextractionengine.mod')

class FeatureExtractionFlowReducer:
    def process(self, line):
        if line.strip()!="":
            if line.count("\t")==2:
                _collection = line.split("\t")
                word = _collection[0]
                category = _collection[1]
                feature_dict = _collection[2]

                feature_category_tuple = (word,feature_dict,category)
                print feature_category_tuple


if __name__ == '__main__':
    _instance = FeatureExtractionFlowReducer()

    # a single line is <category> '<instance_name> | <instance>
    for line in sys.stdin:
        line = line.strip()
        _instance.process(line)