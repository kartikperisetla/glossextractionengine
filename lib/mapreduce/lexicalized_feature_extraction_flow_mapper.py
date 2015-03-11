#!/usr/bin/python
import sys
import re
import cStringIO
# add library to path
sys.path.insert(0, 'glossextractionengine.mod')

from lib.feature_extractor.pos_context_sequence_feature_extractor import POSContextSequenceFeatureExtractor
from lib.feature_extractor.lexicalized_ngrams_feature_extractor import LexicalizedNgramsFeatureExtractor

# mapper side - class that acts as proxy for feature extractor
class LexicalizedFeatureExtractionFlowMapper:
    def __init__(self, context_window_size=4, prime_feature_length=4, add_prime_feature = False, ngram_value=2):
        # get hold of suitable feature extractor
        # k_param: pass 4 tokens as context window length:

        self.feature_extractor = POSContextSequenceFeatureExtractor(k_param=context_window_size,prime_feature_length=prime_feature_length, add_prime_feature=add_prime_feature)

        self.lexicalized_fe = LexicalizedNgramsFeatureExtractor(ngram_value)

    def process(self, line):
        try:
            feature_dict,category,word = self.feature_extractor.extract_features(line)
            lex_feature_dict, lex_cat, lex_word = self.lexicalized_fe.extract_features(line)

            # updating the feature dict with lexicalized features as well
            feature_dict.update(lex_feature_dict)

            if not feature_dict is None:
                print word,"\t",category,"\t",feature_dict
        except Exception as ex:
            print >>sys.stderr,ex.message
            pass

if __name__ == '__main__':
    if len(sys.argv)<2:
        print "Too few arguments to instantiate FeatureExtractionFlowMapper"
        exit()
    _args = sys.argv[1]
    params = _args.split("#")
    _context_window_size = int(params[0].strip())
    _prime_feature_length = int(params[1].strip())
    _add_prime_feature = bool(params[2].strip())
    _ngram_value = int(params[3].strip())

    _instance = LexicalizedFeatureExtractionFlowMapper(context_window_size=_context_window_size, prime_feature_length=_prime_feature_length, add_prime_feature=_add_prime_feature, ngram_value=_ngram_value)

    # a single line is <category> '<instance_name> | <instance>
    for line in sys.stdin:
        line = line.strip()
        _instance.process(line)