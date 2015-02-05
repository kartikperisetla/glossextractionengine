#!/usr/bin/python

__author__ = 'kartik'

from lib.feature_extractor.base_feature_extractor import BaseFeatureExtractor
from lib.feature_extractor.sentence_tokens_feature_extractor import SentenceTokensFeatureExtractor
import re,nltk

KPARAM = "ALL"
PRIME_FEATURE_LENGTH = 4

# method that extracts contextual features based on Part of speech tags around the word of interest
class POSContextSequenceFeatureExtractor(BaseFeatureExtractor):

    def __init__(self, k_param=KPARAM,prime_feature_length=PRIME_FEATURE_LENGTH):
        super(POSContextSequenceFeatureExtractor, self).__init__()
        self.k_param = k_param
        self.prime_feature_length = prime_feature_length
        self.add_prime_feature = False
        self.debugFlag = 0 # off by default
        pass

    def debug(self,s):
        if self.debugFlag==1:
            print s

    # method that generates sequence model considering all words in the sentence
    # params- result_tuple with category, word, tokens
    def getFullSentenceSequenceModel(self, result_tuple):
        category,word,tokens,sentence = result_tuple
        pos_tags = nltk.pos_tag(tokens)
        feature_dict = {}
        for i,tpl in enumerate(pos_tags):
            key ="W"+str(i)
            wrd,p_tg = tpl
            val = p_tg
            feature_dict[key] = val
        return feature_dict

    # method that generates sequence model considering only k words from beginning of the line
    # params- result_tuple with category, word, tokens
    # returns a dictionary with features
    def getKSequenceModel(self, result_tuple):
        category,word,tokens,sentence = result_tuple
        pos_tags = nltk.pos_tag(tokens)
        feature_dict = {}
        for i,tpl in enumerate(pos_tags):

            # read k features- then break
            if i>self.k_param:
                break
            key ="W"+str(i)
            wrd,p_tg = tpl
            val = p_tg
            feature_dict[key] = val
        return feature_dict

    # method that gives start and end index of tokens to be considered for sequence model if NP lies in first half of the sentence
    def getIndicesFirstHalf(self,index,num_of_tokens):
        self.debug("num_of_tokens:"+str(num_of_tokens))
        self.debug("index got in getIndicesFirstHalf:"+str(index))

        self.debug("k_param:"+str(self.k_param))
        while( (num_of_tokens)-index)< self.k_param:
            index = index -1
        start_index = index
        end_index = index + self.k_param
        return (start_index,end_index)

    # method that gives start and end index of tokens to be considered for sequence model if NP lies in second half of the sentence
    def getIndicesSecondHalf(self,index,num_of_tokens):
        while(index)< self.k_param:
            index = index +1
        start_index = index-self.k_param+1
        end_index = index+1
        return (start_index,end_index)

    # method that gives start and end index of tokens to be considered for sequence model if NP lies at middle of the sentence
    def getIndicesForMiddleWord(self,index,num_of_tokens):
        if self.k_param % 2==0:
            start_index = index -(self.k_param/2)
            end_index = index + (self.k_param/2)
        else:
            start_index = index -(self.k_param/2)
            end_index = index + (self.k_param/2)+1
        return (start_index,end_index)

    # method that reads tokens and returns feature_dict
    def getSequenceModelForIndexRange(self,result_tuple,index,start_index,end_index):
        category,word,tokens,sentence = result_tuple
        pos_tags = nltk.pos_tag(tokens)

        self.debug(pos_tags)

        feature_dict = {}
        for i in range(start_index, end_index):
            key ="W"+str(i)
            wrd,p_tg = pos_tags[i]
            val = p_tg
            feature_dict[key] = val

        if self.add_prime_feature:
            self.debug("got features, looking for prime_feature")
            key="prime_feature"
            val=""
            if start_index==index:
                for i in range(index,index+self.prime_feature_length+1):
                    wrd,p_tg=pos_tags[i]
                    val=val+p_tg+" "
            elif end_index-1==index:
                self.debug("STR:"+str(index-self.prime_feature_length)+" END:"+str(index+1))
                for i in range(index-self.prime_feature_length,index+1):
                    wrd,p_tg=pos_tags[i]
                    val=val+p_tg+" "
            else:
                while(end_index-start_index>=self.prime_feature_length):
                    start_index=start_index+1
                    end_index=end_index-1
                    self.debug("MIDDLE_start_index:"+str(start_index)+" end_index:"+str(end_index))
                for i in range(start_index,end_index):
                    wrd,p_tg=pos_tags[i]
                    val=val+p_tg+" "
            feature_dict[key]=val[:-1]

        return feature_dict

    # method that takes instance as input and returns feature vector and optional category label
    # params: instance of format- <category> '<instance_name> | <instance>
    # returns: a tuple of (category, word, tokens, sentence)
    def extract_features(self, instance):
        _sentence_feature_extractor = SentenceTokensFeatureExtractor()
        result_tuple = _sentence_feature_extractor.extract_features(instance)
        category,word,tokens,sentence = result_tuple

        # if using test instance
        if category is None and word is None:
            if self.k_param==KPARAM:
                feature_dict = self.getFullSentenceSequenceModel(result_tuple)
            else:
                feature_dict = self.getKSequenceModel(result_tuple)

            return (feature_dict,None)


        tokens_set = set(tokens)
        num_of_tokens = len(tokens)

        # if sentence contains the NP
        if word in sentence.lower():
            self.debug("word in sentence")
            # tokens in sentence is less or equal to k param
            if len(tokens)<=self.k_param:
                feature_dict = self.getFullSentenceSequenceModel(result_tuple)
            else:

                if tokens.count(word)==0:
                    for token_index,token in enumerate(tokens):
                        if word in token:
                            index=token_index
                            break	# found the token containing this word
                else:
                    index = tokens.index(word)	# tokens.index(word)sss

                self.debug("INDEX_FOUND_AT:"+str(index))

                # word lies in first half of the sentence
                if index<num_of_tokens/2:
                    self.debug("lies in lower half")
                    start_index,end_index = self.getIndicesFirstHalf(index,num_of_tokens)
                    self.debug("start_index:"+str(start_index)+" end_index:"+str(end_index))

                # word lies in second half of the sentence
                if index>num_of_tokens/2:
                    start_index,end_index = self.getIndicesSecondHalf(index, num_of_tokens)
                    self.debug("lies in second half")
                    self.debug("start_index:"+str(start_index)+" end_index:"+str(end_index))

                # word lies in middle of the sentence
                if index == num_of_tokens/2:
                    start_index,end_index = self.getIndicesForMiddleWord(index,num_of_tokens)
                    self.debug("lies at the middle")
                    self.debug("start_index:"+str(start_index)+" end_index:"+str(end_index))

                # get sequence model for tokens in give index range
                feature_dict = self.getSequenceModelForIndexRange(result_tuple,index,start_index, end_index)

        else:	# sentence doesn't contains the NP
            self.debug("word not in line")
            if self.k_param==KPARAM:
                feature_dict = self.getFullSentenceSequenceModel(result_tuple)
            else:
                feature_dict = self.getKSequenceModel(result_tuple)

        return (feature_dict,category)