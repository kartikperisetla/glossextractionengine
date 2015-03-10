__author__ = 'kartik'

from lib.transformation.base_transformation import BaseTransformation

class LowerCaseTransformation(BaseTransformation):

    # method that applies transformation on text
    def transform(self, text):
         if not text is None:
            return text.lower()
