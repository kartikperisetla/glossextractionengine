__author__ = 'kartik'

from lib.filter.base_filter import BaseFilter

# class that filters sentences based on sentence length
class LengthFilter(BaseFilter):
    # method to filter sentence
    def filter(self, sentence):
        if not sentence is None:
            sentence = sentence.strip()
            if not sentence is "":
                tokens = sentence.split(" ")
                if len(tokens)>=self.min_length:
                    return True

        return False
