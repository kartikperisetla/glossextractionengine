__author__ = 'kartik'

import sys
# add library to path
sys.path.insert(0, 'glossextractionengine.mod')

from lib.feature_extractor.base_feature_extractor import BaseFeatureExtractor
from lib.transformation.remove_non_alphanumeric import RemoveNonAlphanumericTransformation
from lib.utils.regex_handler import RegexHandler
import re

class MaltParsedSentenceFeatureExtractor(BaseFeatureExtractor):

    def __init__(self):
        self.word_pos_tuple_collection = None
        self.token_collection = None

    # method that takes instance as input and returns feature vector and optional category label
    # params: malt parsed sentence ;
    #
    # instance of format-
    # Guests/NNS invited/VBD to/TO the/DT presidential/JJ ball/NN will/MD have/VB to/TO wear/VB tuxedoes/NNS ./.
    #
    # returns: a list of tuples of form : (category, word, tokens, sentence)
    def extract_features(self, instance):
        if instance.strip()=="":
            return (None, None, None, None)

        _malt_word = instance.split(" ")

        token_collection = []
        word_pos_tuple_collection =[]

        for item in _malt_word:
            if "/" in item:
                _coll = item.split("/")
                _word = _coll[0]
                _pos_tag = _coll[1]
                token_collection.append(_word)   # these are basically tokens in the sentence
                _new_item = (_word, _pos_tag)
                word_pos_tuple_collection.append(_new_item)

        # updating attributes as soon as you compute them
        self.word_pos_tuple_collection = word_pos_tuple_collection
        self.token_collection = token_collection
        result = self.parseInstanceWithMultipleNN(token_collection, word_pos_tuple_collection, instance)
        return result

    def get_token_collection(self):
        return self.token_collection

    def get_word_pos_tuple_collection(self):
        return self.word_pos_tuple_collection

    # method to check if there are multiple nouns in a sentence and if return list of tuples as returned by parseInstance
    def parseInstanceWithMultipleNN(self, tokens, word_pos_tuple_collection, instance):
        tuple_collection = []

        # iterate over the word-pos-tuple collection
        for i,item in enumerate(word_pos_tuple_collection):
            # except for the last token in sentence
            if i!=len(word_pos_tuple_collection)-1:
                curr_word, curr_word_tag = item
                next_word, next_word_tag = word_pos_tuple_collection[i+1]

                # if both noun tokens adjacent- merge them
                if "NN" in curr_word_tag and "NN" in next_word_tag:
                    merged_token = curr_word+"_"+next_word
                    merged_token_tag = "NNP"

                    # update the token list with new merged NNP token
                    tokens[i] = merged_token
                    del tokens[i+1]
                    tuple_collection.append((None, merged_token, tokens, instance,None))
                    i= i+1
                elif "NN" in curr_word_tag:
                    tuple_collection.append((None, wrd, tokens, instance,None))

        return tuple_collection


# s = "Guests/NNS invited/VBD to/TO the/DT presidential/JJ ball/NN will/MD have/VB to/TO wear/VB tuxedoes/NNS ./.      1"
# m = MaltParsedSentenceFeatureExtractor()
# print m.extract_features(s)

