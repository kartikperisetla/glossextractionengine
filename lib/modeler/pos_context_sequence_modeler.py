__author__ = 'kartik'

from lib.modeler.base_modeler import BaseModeler
import nltk

class POSContextSequenceModeler(BaseModeler):

    def __init__(self,**kwargs):
        super(POSContextSequenceModeler, self).__init__(**kwargs)

    def train(self):
        _train_feature_collection = self.get_feature_collection()
        self.entity = nltk.MaxentClassifier.train(_train_feature_collection, algorithm='GIS', trace=0)