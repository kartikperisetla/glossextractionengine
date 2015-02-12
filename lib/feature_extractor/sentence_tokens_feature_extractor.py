#!/usr/bin/python
import sys
# add library to path
sys.path.insert(0, 'glossextractionengine.mod')

__author__ = 'kartik'

from lib.feature_extractor.base_feature_extractor import BaseFeatureExtractor
import re,nltk

# method that extracts basic sentence features like tokens, instance_name in instance provided
class SentenceTokensFeatureExtractor(BaseFeatureExtractor):

    # method that takes instance as input and returns feature vector and optional category label
    # params: instance of format- <category> '<instance_name> | <instance>
    # returns: a tuple of (category, word, tokens, sentence)
    def extract_features(self, instance):
        line = instance.lower()
        # split the instance
        items = line.split(" | ")

        # get hold of the first part
        var = items[0]
        collection = var.split("'")

        # if its labeled training instances
        if len(collection)>1:
            # get the category of the instance
            category = collection[0].strip()
            # get the instance_name or Head NP or NP of our interest
            word = collection[1].strip()

            # get the sentence on right side of '|'
            sentence = items[1]

            word_replacement=re.sub(r' ','',word)
            sentence = re.sub(word,word_replacement,sentence)
            tokens = nltk.word_tokenize(sentence)
            word = word_replacement
            return (category,word,tokens,sentence)
        else:
            # flow for test instances
            sentence=items[1]
            tokens=nltk.word_tokenize(sentence)
            return (None,None,tokens,sentence)
