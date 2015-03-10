__author__ = 'kartik'

import pickle,os,sys
from ast import literal_eval

sys.path.insert(0, '.')
sys.path.insert(0, 'glossextractionengine.mod')
sys.path.insert(0, 'glossextractionengine.mod/saved_models')


#class to train the model and generate the classifier
class BaseModeler(object):
    def __init__(self,**kwargs):
        # **kwargs is a dictionary
        # look for feature_set_collection to update appropriate attribute
        if kwargs.has_key("feature_set_location"):
            self.feature_set_location = kwargs["feature_set_location"]
        else:
            self.feature_set_location = None

        # attribute to hold entity object- can be classifier or named entity recognizer or relationship extractor
        self.entity = None

    # method to create the list of feature vectors for all instances
    # it can be used for reading both training and test feature vectors
    # returns: list of (feature_dict, category) tuples
    def get_feature_collection(self):
        if not self.feature_set_location is None:
            _train_feature_collection = []
            _feature_set_file = open(self.feature_set_location,"r")

            for feature_dict_category_tuple in _feature_set_file:
                feature_dict_category_tuple = literal_eval(feature_dict_category_tuple)

                # unpack and do literal eval to restore datastructure
                _feature_dict,_category = feature_dict_category_tuple
                _feature_dict = literal_eval(_feature_dict)
                # _category = literal_eval(_category)
                # pack again to form tuple
                feature_dict_category_tuple=(_feature_dict,_category)

                _train_feature_collection.append(feature_dict_category_tuple)

            return _train_feature_collection
        else:
            return None

    # method to save the trained model
    def save_model(self,**kwargs):
        # look for name for saving the model
        if kwargs.has_key("name"):
            self.model_saved_name = kwargs["name"]
        else:
            self.model_saved_name = self.__class__.__name__

        if kwargs.has_key("location"):
            _location = kwargs["location"] + "/"+ self.model_saved_name
        else:
            _location = self.model_saved_name

        if not os.path.exists(kwargs["location"]):
            os.system("mkdir "+kwargs["location"])

        _pobj = open(_location,"wb")
        # save the entity as pickle file with name provided in param
        pickle.dump(self.entity, _pobj)
        _pobj.close()

    # method to load the model from pickle file
    # it updates the self.entity attribute once it loads the model from pickle file
    def load_model(self,**kwargs):
        # look for name for saving the model
        if kwargs.has_key("name"):
            self.model_saved_name = kwargs["name"]
        else:
            self.model_saved_name = self.__class__.__name__

        if kwargs.has_key("location"):
            _location = kwargs["location"] + "/"+ self.model_saved_name
        else:
            _location = self.model_saved_name

        _pobj = open(_location,"rb")
        self.entity = pickle.load(_pobj)

    # method to train the model
    # must be overriden in derived implementation
    def train(self,**kwargs):
        pass

    # method to classify the test set whose feature set collection is given as param
    # must be overriden in derived implementation
    def test(self,**kwargs):
        pass

    def classify(self, test_feature_dict):
        result_category = self.entity.classify(test_feature_dict)
        return result_category