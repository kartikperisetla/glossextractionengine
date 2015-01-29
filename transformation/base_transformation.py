__author__ = 'kartik'


# class to present skeleton for basic transformation
class BaseTransformation:
    # constructor
    def __init__(self):
        print "BaseTransformation:init"

    # method that applies transformation on text
    def transform(self, text):
        pass
        # This method must be overriden by derived class