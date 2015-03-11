#!/usr/bin/python
import sys
import re
import cStringIO

# add library to path
sys.path.insert(0, '.')
sys.path.insert(0, 'glossextractionengine.mod')
sys.path.insert(0, 'glossextractionengine.mod/saved_models')

from lib.modeler.pos_context_sequence_modeler import POSContextSequenceModeler
from ast import literal_eval


class MaltParsedFeatureExtractionFlowReducer:
    def __init__(self, saved_model_name):
        pass
        self._instance = POSContextSequenceModeler()
        coll = saved_model_name.split("/")
        saved_model_name = coll[-1:][0]
        self._instance.load_model(name = saved_model_name)

    def process(self, line):
        if line.strip()!="":
            try:
                # if line.count("\t")>=2:
                _collection = line.split("\t")
                word = _collection[0]
                feature_dict = _collection[1]
                line = _collection[2]
                _inst_feature_dict = literal_eval(feature_dict)
                result = self._instance.classify(_inst_feature_dict)

                # output only positive instances
                if not "-" in result:
                    feature_category_tuple = (word, result, feature_dict, line)
                    print feature_category_tuple
            except Exception as ex:
                print >>sys.stderr,ex.message
                pass


if __name__ == '__main__':
    if len(sys.argv)<2:
        print "MaltParsedFeatureExtractionFlowReducer: need model as parameter name"
    else:
        _model_file = sys.argv[1]
        _instance = MaltParsedFeatureExtractionFlowReducer(_model_file)

        # a single line is <word>,"\t",<feature_dict>,"\t",<line>
        for line in sys.stdin:
            line = line.strip()
            _instance.process(line)