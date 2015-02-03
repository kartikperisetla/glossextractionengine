#!/usr/bin/python

__author__ = 'kartik'

import re
from utils.wiki_extractor_util import clean

class RegexHandler:

    # method to cleanup the a sentence
    def wikipedia_markup_cleanup(self, raw):
        result = re.sub('{{.*?}}', '', raw)
        result = re.sub('{{.*?}', '', result)
        result = re.sub('\[.*?\]', '', result)
        result = re.sub("''", '', result)
        result = re.sub('\[\[', '', result)
        result = re.sub(']]', '', result)
        result = re.sub('<ref.*?>', '', result)
        result = re.sub('<ref.*\.*.*>', '', result)
        result = re.sub('</ref>', '', result)
        result = re.sub('#.+|', '', result)
        result = re.sub('<.*', '', result)
        result = re.sub('.*>', '', result)
        result = re.sub('\[.*', '', result)
        result = re.sub('.*\]', '', result)
        result = re.sub('\(.*', '', result)
        result = re.sub('.*\)', '', result)
        result = re.sub('{.*', '', result)
        result = re.sub('.*}', '', result)
        result = re.sub('&nbsp;', '', result)
        result = re.sub('\|', '', result)

        # remove lines with File: in it
        result = re.sub('.*File:.*', '', result)
        return result

    # method to clean text using wiki_extractor method
    def clean_wikipedia_article(self, raw):
        return clean(raw)