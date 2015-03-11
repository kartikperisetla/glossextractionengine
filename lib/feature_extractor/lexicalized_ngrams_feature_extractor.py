#!/usr/bin/python
import sys
# add library to path
sys.path.insert(0, 'glossextractionengine.mod')

from lib.feature_extractor.base_feature_extractor import BaseFeatureExtractor
from lib.feature_extractor.sentence_tokens_feature_extractor import SentenceTokensFeatureExtractor

import re,nltk

__author__ = 'kartik'

# class that extracts contextual features based on Part of speech tags around the word of interest
class LexicalizedNgramsFeatureExtractor(BaseFeatureExtractor):
    def __init__(self, n=2):
        self.n_value =n
        self.feature_dict ={}
        pass

    def extract_features(self, instance):
        _sentence_feature_extractor = SentenceTokensFeatureExtractor()
        result_tuple = _sentence_feature_extractor.extract_features(instance)
        # malformed instance
        if result_tuple is None:
            return (None,None,None)

        category,word,tokens,sentence,_old_word = result_tuple
        num_of_tokens = len(tokens)

        # if sentence contains the NP
        if word.lower() in sentence.lower() and self.n_value<=num_of_tokens :
            # capture index of head NP in the instance
            index = tokens.index(word)

            # head NP is first word in sentence
            if index==0:
                start = index+1
                end = start +self.n_value+1
                n_grams = tokens[start:end]
                result = ' '.join(n_grams)

            # head NP is last word in sentence
            elif index==len(tokens)-1:
                start = index- self.n_value
                end = index
                n_grams = tokens[start:end]
                result = ' '.join(n_grams)
            # for any other case
            else:
                _temp_lst = []
                curr_index = index-1
                while curr_index!=0 and curr_index>=(index-self.n_value):
                    _temp_lst.insert(0,tokens[curr_index])
                    curr_index = curr_index - 1
                result = ' '.join(_temp_lst)

            key = str(self.n_value)+"-gram"
            self.feature_dict[key] = result
            resultant_tuple = (self.feature_dict,None,tokens[index])
            return resultant_tuple
        return (None,None,None)