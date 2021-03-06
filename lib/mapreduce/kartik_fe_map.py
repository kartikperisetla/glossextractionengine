#!/usr/bin/python
import sys
import re
import cStringIO


# add library to path
sys.path.insert(0, 'glossextractionengine.mod')

from lib.feature_extractor.pos_context_sequence_feature_extractor import POSContextSequenceFeatureExtractor

# mapper side - class that acts as proxy for feature extractor
class FeatureExtractionFlowMapper:
    def __init__(self):
        # get hold of suitable feature extractor
        # k_param: pass 4 tokens as context window length:
        self.feature_extractor = POSContextSequenceFeatureExtractor(k_param=4)

    def process(self, line):
        feature_dict,category,word = self.feature_extractor.extract_features(line)
        if not feature_dict is None:
            print word,"\t",category,"\t",feature_dict

if __name__ == '__main__':
    _instance = FeatureExtractionFlowMapper()

    # a single line is <category> '<instance_name> | <instance>
    for line in sys.stdin:
        line = line.strip()
        _instance.process(line)