__author__ = 'kartik'

class BaseFilter:
    # constructor accepting sentence of min_length for filtering
    def __init__(self):
        print "BaseFilter:init"

    # method to filter sentence based on custom logic
    def filter(self, sentence):
        pass
        # This method must be overriden by derived class
