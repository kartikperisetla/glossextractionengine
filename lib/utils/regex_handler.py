#!/usr/bin/python

__author__ = 'kartik'

import re
import string

from lib.utils.wiki_extractor_util import clean


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

     # method to cleanup the a sentence
    def wiktionary_markup_cleanup(self, raw):
        result = re.sub('{{.*?}}', '', raw)
        result = re.sub('{{.*?}', '', result)
        result = re.sub('\[\[', '', result)
        result = re.sub('\]\]', '', result)
        result = re.sub('<ref.*>', '', result)
        result = re.sub('</ref>', '', result)
        return result

    # method to clean text using wiki_extractor method
    def clean_wikipedia_article(self, raw):
        return clean(raw)

    # method to clean line for sampling
    def get_clean_line_for_sampling(self, line):
        line=re.sub(':', ' ', line)
        line=re.sub('\[', ' ', line)
        line=re.sub('\]', ' ', line)
        line=re.sub('{', ' ', line)
        line=re.sub('}', ' ', line)
        line=re.sub(r'<!--',' ',line)
        line=re.sub(r'-->',' ',line)
        line=re.sub(r'&','and',line)
        line=re.sub(r'<','&lt;',line)
        line=re.sub(r'>','&gt;',line)
        line=re.sub(r'\)',' ',line)
        line=re.sub(r'\(',' ',line)
        line=re.sub(r'\\',' ',line)
        line=re.sub(r'\+',' ',line)
        line=re.sub(r'[^A-Za-z0-9\-\'\| ]',' ',line)

        # remove pipes from within the sentence
        items=line.split(" | ")
        label=items[0]
        sentence=items[1]
        sentence=re.sub(r'\|',' ',sentence)
        line=label+" | "+sentence

        # line=re.sub(r'\|','',line)
        return line

    # method to remove non (alphanumeric and punctuation)
    def give_printable_string(self, line):
        filtered_string = filter(lambda x: x in string.printable, line)
        return filtered_string

    # method to get alphanumeric version of a string
    def get_alphanumeric(self, line):
        result = re.sub(r'[^a-zA-Z0-9]',' ', line)
        return result