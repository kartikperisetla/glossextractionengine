#!/usr/bin/python
import sys
import re
import cStringIO
# add library to path
sys.path.insert(0, 'glossextractionengine.mod')

from lib.modeler.pos_context_sequence_modeler import POSContextSequenceModeler
from ast import literal_eval

class CrossValidationFeatureExtractionFlowReducer:
    def __init__(self, saved_model_name, threshold_value = 85):
        pass
        self._instance = POSContextSequenceModeler()
        coll = saved_model_name.split("/")
        saved_model_name = coll[-1:][0]
        self._instance.load_model(name = saved_model_name)
        self.threshold = threshold_value

    def process(self, line):
        try:
            if line.strip()!="":
                _collection = line.split("\t")
                word = _collection[0]
                category = _collection[1]
                feature_dict = _collection[2]

                _inst_feature_dict = literal_eval(feature_dict)
                prob_dist = self._instance.entity.prob_classify(_inst_feature_dict)

                pos_prob = prob_dist.prob('1')
                neg_prob = prob_dist.prob('-1')
                print>>sys.stderr, " pos_prob:",pos_prob
                print>>sys.stderr, " neg_prob:",neg_prob

                if float(pos_prob)*100 >= float(self.threshold):
                    result = "1"
                else:
                    result = "-1"

                flag = "NO-MATCH"
                if str(category.strip()) == str(result.strip()):
                    flag = "MATCH"

                feature_category_tuple = (word,result,category,flag, feature_dict, line)
                print feature_category_tuple
        except Exception as ex:
            print>>sys.stderr, ex.message,"\n for :",line


if __name__ == '__main__':
    _model_file = sys.argv[1]
    _threshold_value = sys.argv[2]
    _instance = CrossValidationFeatureExtractionFlowReducer(_model_file, _threshold_value)

    # a single line is <category> '<instance_name> | <instance>
    for line in sys.stdin:
        line = line.strip()
        _instance.process(line)