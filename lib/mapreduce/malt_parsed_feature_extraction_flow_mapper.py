#!/usr/bin/python
import sys
import re
import cStringIO

# add library to path
sys.path.insert(0, 'glossextractionengine.mod')

from lib.feature_extractor.malt_parsed_pos_context_sequence_feature_extractor import MaltParsedPOSContextSequenceFeatureExtractor

# mapper side - class that acts as proxy for feature extractor for malt parsed sentences
class MaltParsedFeatureExtractionFlowMapper:
    def __init__(self):
        # get hold of suitable feature extractor
        # k_param: pass 4 tokens as context window length:
        self.feature_extractor = MaltParsedPOSContextSequenceFeatureExtractor(k_param=4)

    def process(self, line):

        result = self.feature_extractor.extract_features(line)
        if isinstance(result, list):
            for _item in result:
                feature_dict,category,word = _item
                # if not category is None and not word is None:
                    # not printing category as it will be always None for Test dataset
                print word,"\t",feature_dict,"\t",line
        else:
            feature_dict,category,word = result
            print word,"\t",feature_dict,"\t",line


if __name__ == '__main__':
    _instance = MaltParsedFeatureExtractionFlowMapper()

    # a single line is <category> '<instance_name> | <instance>
    for line in sys.stdin:
        line = line.strip()
        _instance.process(line)