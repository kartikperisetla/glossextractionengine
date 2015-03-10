__author__ = 'kartik'


import string,re

from lib.transformation.base_transformation import BaseTransformation
from lib.utils.regex_handler import RegexHandler

class RemoveNonAlphanumericTransformation(BaseTransformation):
    # method that applies transformation on text
    def transform(self, text):
        r = RegexHandler()
        # basically get the string printable on console
        result = r.get_alphanumeric(text)
        return result