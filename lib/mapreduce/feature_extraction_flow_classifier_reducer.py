#!/usr/bin/python
import sys
import re
import cStringIO
# add library to path
sys.path.insert(0, 'glossextractionengine.mod')

from lib.modeler.pos_context_sequence_modeler import POSContextSequenceModeler
from ast import literal_eval

class FeatureExtractionFlowClassifierReducer:
    def __init__(self, saved_model_name):
        pass
        self._instance = POSContextSequenceModeler()
        coll = saved_model_name.split("/")
        saved_model_name = coll[-1:][0]
        self._instance.load_model(name = saved_model_name)

    def process(self, line):
        try:
            if line.strip()!="":
                _collection = line.split("\t")
                word = _collection[0]
                category = _collection[1]
                feature_dict = _collection[2]

                _inst_feature_dict = literal_eval(feature_dict)
                result = self._instance.classify(_inst_feature_dict)

                flag = "NO-MATCH"
                if str(category) == str(result):
                    flag = "MATCH"

                feature_category_tuple = (word,result,category,flag, feature_dict, line)
                print feature_category_tuple
        except Exception as ex:
            print>>sys.stderr, ex.message,"\n for :",line


if __name__ == '__main__':
    _instance = FeatureExtractionFlowClassifierReducer()

    # a single line is <category> '<instance_name> | <instance>
    for line in sys.stdin:
        line = line.strip()
        _instance.process(line)