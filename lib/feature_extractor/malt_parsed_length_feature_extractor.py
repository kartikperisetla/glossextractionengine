#!/usr/bin/python
import sys
# add library to path
sys.path.insert(0, 'glossextractionengine.mod')

__author__ = 'kartik'

from lib.feature_extractor.base_feature_extractor import BaseFeatureExtractor
from lib.feature_extractor.malt_parsed_sentence_feature_extractor import MaltParsedSentenceFeatureExtractor
from lib.feature_extractor.sentence_tokens_feature_extractor import SentenceTokensFeatureExtractor
from lib.filter.english_token_filter import EnglishTokenFilter

import re,nltk

# class that extracts length of instance in terms of tokens in it
class MaltParsedLengthFeatureExtractor(BaseFeatureExtractor):

    # method that extract feature from instance
    # param: instance
    # returns: a tuple of (<feature_dict>, <category>, <word>, <sentence>)
    def extract_features(self, instance):
        try:
            _sentence_feature_extractor = MaltParsedSentenceFeatureExtractor()
            result_tuple = _sentence_feature_extractor.extract_features(instance)

            if result_tuple is None:
                return (None,None,None,None)

            # depending on if result_tuple is list or single tuple, take action
            if isinstance(result_tuple,list):
                result_list = []
                for _item in result_tuple:
                    result_item = self.get_instance_length(_item)
                    result_list.append(result_item)
                return result_list
            else:
                result = self.get_instance_length(result_tuple)
            return result

        except Exception as ex:
            pass
        return (None,None,None,None)

    def get_instance_length(self, result_tuple):
        category,word,tokens,sentence,_old_word = result_tuple

        if not result_tuple is None:
            length = len(tokens)
            feat_dict ={}
            feat_dict["instance_length"]=length

            return (feat_dict,None,word,sentence)