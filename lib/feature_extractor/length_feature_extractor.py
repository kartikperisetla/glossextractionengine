#!/usr/bin/python
import sys
# add library to path
sys.path.insert(0, 'glossextractionengine.mod')

__author__ = 'kartik'

from lib.feature_extractor.base_feature_extractor import BaseFeatureExtractor
from lib.feature_extractor.sentence_tokens_feature_extractor import SentenceTokensFeatureExtractor
from lib.filter.english_token_filter import EnglishTokenFilter

import re,nltk

# class that extracts length of instance in terms of tokens in it
class LengthFeatureExtractor(BaseFeatureExtractor):

    # method that extract feature from instance
    # param: instance
    # returns: a tuple of (<feature_dict>, <category>, <word>, <sentence>)
    def extract_features(self, instance):
        try:
            _sentence_feature_extractor = SentenceTokensFeatureExtractor()
            result_tuple = _sentence_feature_extractor.extract_features(instance)
            category,word,tokens,sentence,_old_word = result_tuple

            if not instance is None:
                tokens = nltk.word_tokenize(instance)
                length = len(tokens)
                feat_dict ={}
                feat_dict["instance_length"]=length

                return (feat_dict,None,word,instance)
        except Exception as ex:
            pass
        return (None,None,None,None)