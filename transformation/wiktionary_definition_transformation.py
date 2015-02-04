__author__ = 'kartik'

import string
from base_transformation import BaseTransformation

class WiktionaryDefinitionTransformation(BaseTransformation):

    # method that applies transformation on text
    def transform(self, article_title, article_text):
        # return "%s is defined as %s" %  article_title, article_textt

        result = article_title + " is defined as " + filter(lambda x: x in string.printable, article_text)
        return result