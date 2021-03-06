#!/usr/bin/python
import sys,ast
import re
import cStringIO
# add library to path
sys.path.insert(0, 'glossextractionengine.mod')

from lib.feature_extractor.pos_context_sequence_feature_extractor import POSContextSequenceFeatureExtractor

# mapper side - class that acts as proxy for feature extractor
class CrossValidationFeatureExtractionFlowMapper:
    def __init__(self, context_window_size=4, prime_feature_length=4, add_prime_feature_val = False):
        # get hold of suitable feature extractor
        # k_param: pass 4 tokens as context window length:

        self.feature_extractor = POSContextSequenceFeatureExtractor(k_param=context_window_size,prime_feature_length=prime_feature_length, add_prime_feature=add_prime_feature_val)

    def process(self, line):
        try:
            feature_dict,category,word = self.feature_extractor.extract_features(line)
            if not feature_dict is None:
                print word,"\t",category,"\t",feature_dict
        except Exception as ex:
            print >>sys.stderr,ex.message
            pass

if __name__ == '__main__':
    if len(sys.argv)<2:
        print "Too few arguments to instantiate FeatureExtractionFlowMapper"
        exit()
    _args = sys.argv[2]
    params = _args.split("#")
    _context_window_size = int(params[0].strip())
    _prime_feature_length = int(params[1].strip())
    _add_prime_feature = ast.literal_eval(params[2].strip())
    print>>sys.stderr," FeatureExtractionFlowMapper:_add_prime_feature: ",_add_prime_feature
    _instance = CrossValidationFeatureExtractionFlowMapper(context_window_size=_context_window_size, prime_feature_length=_prime_feature_length, add_prime_feature_val=_add_prime_feature)


    # a single line is <category> '<instance_name> | <instance>
    for line in sys.stdin:
        line = line.strip()
        _instance.process(line)