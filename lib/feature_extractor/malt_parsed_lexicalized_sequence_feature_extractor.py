#!/usr/bin/python
import sys
# add library to path
sys.path.insert(0, 'glossextractionengine.mod')

from lib.feature_extractor.base_feature_extractor import BaseFeatureExtractor
from lib.feature_extractor.malt_parsed_sentence_feature_extractor import MaltParsedSentenceFeatureExtractor
from lib.feature_extractor.malt_parsed_lexicalized_ngrams_feature_extractor \
    import MaltParsedLexicalizedNgramsFeatureExtractor
import re
from lib.filter.english_token_filter import EnglishTokenFilter

SLICE_WINDOW_LENGTH = 4

# class that extracts lexical features based on Part of speech tags around the
# word of interest i.e Head NP
# NOTE: It assumes you have pos tags and tokens already extracted either through
#  malt parsed sentence feature extractor or by other means
class MaltParsedLexicalizedSequenceFeatureExtractor(BaseFeatureExtractor):

    # params:
    # k_param: the length n in n-grams to be considered in the context window
    # prime_feature_length: the length of context window pos tags of words
    # falling in that window will constitute the prime feature
    # add_prime_feature: boolean flag to indicate whether to generate prime
    # feature
    def __init__(self, slice_window_length = SLICE_WINDOW_LENGTH):
        self.slice_window_length = slice_window_length
        self.english_filter = EnglishTokenFilter()
        self.pos_list = ["DT","JJ","NN","NNP","NNS"]
        pass

    # method that gives start and end index of tokens to be considered for
    # sequence model if NP lies in first half of the sentence
    def getIndicesFirstHalf(self,index,num_of_tokens):
        if num_of_tokens<self.k_param:
            start_index = 0
            end_index = num_of_tokens - 1
            return (start_index,end_index)

        while( (num_of_tokens)-index)< self.k_param:
            index = index -1
        start_index = index
        end_index = index + self.k_param
        return (start_index,end_index)

    # method that gives start and end index of tokens to be considered for
    # sequence model if NP lies in second half of the sentence
    def getIndicesSecondHalf(self,index,num_of_tokens):
        if num_of_tokens<self.k_param:
            start_index = 0
            end_index = num_of_tokens - 1
            return (start_index,end_index)

        while(index)< self.k_param:
            index = index +1
        start_index = index-self.k_param+1
        end_index = index+1
        return (start_index,end_index)

    # method that gives start and end index of tokens to be considered for
    # sequence model if NP lies at middle of the sentence
    def getIndicesForMiddleWord(self,index,num_of_tokens):
        if num_of_tokens<self.k_param:
            start_index = 0
            end_index = num_of_tokens - 1
            return (start_index,end_index)

        if self.k_param % 2==0:
            start_index = index -(self.k_param/2)
            end_index = index + (self.k_param/2)
        else:
            start_index = index -(self.k_param/2)
            end_index = index + (self.k_param/2)+1
        return (start_index,end_index)

    # method that reads tokens and returns feature_dict
    # params: index - position of head NP in the sentence
    # result_tuple - tuple consisting of category, word, tokens, sentence and
    # old word
    def getLexicalFeaturesForIndexRange(self,result_tuple,index):
        category,word,tokens,sentence,_old_word = result_tuple
        pos_tags = self.word_pos_tuple_collection

        feature_dict = {}

        # adding prime feature for beginning and ending of the sentence as well
        # for lexical pattern beginning with HNP
        _pattern = ""
        for k in range(index, min(index+self.slice_window_length,len(pos_tags))):
            wrd,p_tg = pos_tags[k]
            # if curr token is head NP use HNP as pos tag
            if k==index:
                p_tg = "HNP"
                _pattern = _pattern + p_tg+" "
            elif p_tg in self.pos_list:
                _pattern = _pattern + p_tg+" "
            else:   # use word itself
                _pattern = _pattern + wrd +" "
        # if HNP is last token in sentence then don't add hnp_begin
        if _pattern.strip() != "HNP":
            feature_dict["hnp_begin"] = _pattern.strip()

        # for lexical pattern ending with HNP
        _pattern = " "
        for k in range(max(0,index-(self.slice_window_length-1)),
                       min(index+1,len(pos_tags))):
            wrd,p_tg=pos_tags[k]
            if k==index:
                p_tg = "HNP"
                _pattern = _pattern + p_tg+" "
            elif p_tg in self.pos_list:
                _pattern = _pattern + p_tg+" "
            else:   # use lexical feature
                _pattern = _pattern + wrd +" "
        # if HNP is first token in sentence then don't add hnp_end
        if _pattern.strip() != "HNP":
            feature_dict["hnp_end"] = _pattern.strip()

        return feature_dict

    # method that takes instance as input and returns feature vector and
    # optional category label
    # params: instance of format- <category> '<instance_name> | <instance>
    # returns: a tuple of (<feature_dict>, <category>, <word>, <sentence>) or
    # a list of such tuples
    def extract_features(self, instance):
        _sentence_feature_extractor = MaltParsedSentenceFeatureExtractor()
        result_tuple = _sentence_feature_extractor.extract_features(instance)

        # copying attributes
        self.token_collection = \
            _sentence_feature_extractor.get_token_collection()
        self.word_pos_tuple_collection = \
            _sentence_feature_extractor.get_word_pos_tuple_collection()

        # malformed instance
        if result_tuple is None:
            return (None,None,None)

        # call _get_seq_model after copying attributes from
        # MaltParsedFeatureExtactor

        # depending on if result_tuple is list or single tuple, take action
        if isinstance(result_tuple,list):
            result_list = []
            for _item in result_tuple:
                result_item = self._get_lexicalized_seq_model(_item)
                result_list.append(result_item)
            return result_list
        else:
            result = self._get_lexicalized_seq_model(result_tuple)
            return result

    # method to get the sequence model for malt parsed version of instance
    # returns a tuple: (feature_dict,category,word,sentence)
    def _get_lexicalized_seq_model(self, result_tuple):
        category,word,tokens,sentence,_old_word = result_tuple

        # if word is non english token then return None
        if not self.english_filter.filter(word):
            return (None,None,None, None)

        tokens_set = set(tokens)
        num_of_tokens = len(tokens)

        # if sentence contains the NP
        if word.lower() in sentence.lower():
            # if the word is not present as complete word in token list 'tokens'
            if tokens.count(word)==0:
                # iterate over tokens
                for token_index,token in enumerate(tokens):
                    # check if word is part of any token
                    if word in token:
                        index=token_index
                        # found the token containing this word
                        break
            else:
                # pick the first index of 'word' in token list 'tokens'
                index = tokens.index(word)	# tokens.index(word)

            # get sequence model for tokens in give index range
            feature_dict = \
                self.getLexicalFeaturesForIndexRange(result_tuple,index)

        else:	# sentence doesn't contains the head NP
            pass

        if not category is None:
            category = category.strip()

        return (feature_dict,category,word,sentence)