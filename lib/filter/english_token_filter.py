__author__ = 'kartik'

from lib.filter.base_filter import BaseFilter
import re
import string

# class that filters sentences based on sentence length
class EnglishTokenFilter(BaseFilter):
    # method that returns True if sentence contains only english tokens
    def filter(self, sentence):
        if set('[~!@#$%^&*()+{}":;\']+$').intersection(sentence):
            return False
        else:
            return True