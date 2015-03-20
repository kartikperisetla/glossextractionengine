#!/usr/bin/python
import sys,ast
import re
import cStringIO
# add library to path
sys.path.insert(0, 'glossextractionengine.mod')

from lib.feature_extractor.pos_context_sequence_feature_extractor import POSContextSequenceFeatureExtractor
from lib.feature_extractor.length_feature_extractor import LengthFeatureExtractor
from lib.mapreduce.base_flow_component import BaseFlowComponent

# mapper side - class that acts as proxy for feature extractor
class FeatureExtractionFlowMapper(BaseFlowComponent):
    def __init__(self, context_window_size=4, prime_feature_length=4, add_prime_feature_val = False):
        super(self.__class__, self).__init__()

        # get hold of suitable feature extractor
        # k_param: pass 4 tokens as context window length:

        # instantiate a pos context sequence feature extractor
        pos_context_seq_feature_extractor = POSContextSequenceFeatureExtractor(k_param=context_window_size,prime_feature_length=prime_feature_length, add_prime_feature=add_prime_feature_val)
        # register the feature extractor to this flow component
        self.register_feature_extractor(pos_context_seq_feature_extractor)

        # instantiate a length feature extractor
        length_feature_extractor = LengthFeatureExtractor()
        # register the feature extractor to this flow component
        self.register_feature_extractor(length_feature_extractor)

        # instantiate any other feature extractor and register it with flow components to start using it in the flow

    # param: string of format- <category> '<instance_name> | <instance>
    def process(self, line):
        try:
            # invokes feature extraction on all registered feature extractors
            result_tuple_collection = self.get_features(line)
            for tuple_instance in result_tuple_collection:
                feature_dict,category,word,sentence = tuple_instance
                if not feature_dict is None:
                    print word,"\t",category,"\t",feature_dict
        except Exception as ex:
            print >>sys.stderr,ex
            pass

if __name__ == '__main__':
    if len(sys.argv)<2:
        print "Too few arguments to instantiate FeatureExtractionFlowMapper"
        exit()
    _args = sys.argv[1]
    params = _args.split("#")
    _context_window_size = int(params[0].strip())
    _prime_feature_length = int(params[1].strip())
    _add_prime_feature = ast.literal_eval(params[2].strip())
    print>>sys.stderr," FeatureExtractionFlowMapper:_add_prime_feature: ",_add_prime_feature
    _instance = FeatureExtractionFlowMapper(context_window_size=_context_window_size, prime_feature_length=_prime_feature_length, add_prime_feature_val=_add_prime_feature)

    # a single line is <category> '<instance_name> | <instance>
    for line in sys.stdin:
        line = line.strip()
        _instance.process(line)