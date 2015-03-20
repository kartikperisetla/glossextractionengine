#!/usr/bin/python
import sys
import re
import cStringIO
# add library to path
sys.path.insert(0, 'glossextractionengine.mod')
__author__ = 'kartik'

# class that provides basic functionality for all components that come in the framework flow
class BaseFlowComponent(object):
    def __init__(self):
        # print "BaseFlowComponent:init"
        # for holding list of feature extractors
        self.feature_extractor_collection = []
        self.refresh()

    def refresh(self):
        # for holding list of tuples returned from extract_features
        self.tuple_collection = {}

    # method to register the feature extractor
    def register_feature_extractor(self, feature_extractor_instance):
        if not feature_extractor_instance is None:
            self.feature_extractor_collection.append(feature_extractor_instance)

    # method to apply feature extractors one by one and update the feature dict
    # param : instance form which features will be extracted
    # return : list of tuples ; [(<feature_dict>, <category>, <word>, <sentence>)]
    def get_features(self, instance):
        # each feature extractor returns <feature_dict>,<category>,<word>,<sentence>

        for fe_object in self.feature_extractor_collection:
            # feat_dict,cat,wrd = fe_object.extract_features(instance)

            _tuple_instance_collection = fe_object.extract_features(instance)

            if isinstance(_tuple_instance_collection,list):
                for _tuple_instance in _tuple_instance_collection:
                    self.update_tuple(_tuple_instance)
            else:
                self.update_tuple(_tuple_instance_collection)

        # return the list of tuples
        result = list(self.tuple_collection.values())
        self.refresh()
        return result

    # method to update the required properties
    def update_tuple(self, tuple_instance):
        if not tuple_instance is None:
            print>>sys.stderr," update_tuple:got tuple_instance:",tuple_instance
            new_feat_dict,new_cat,new_wrd,new_sentence = tuple_instance
            # if valid feature dictionary
            if not new_feat_dict is None:
                # check if tuple corresponding to the given word already exists in the tuple collection
                if self.tuple_collection.has_key(new_wrd):
                    existing_tuple = self.tuple_collection.get(new_wrd)
                    existing_fe_dict, existing_cat, exiting_wrd, existing_sentence = existing_tuple
                    # update the feature dictionary within the tuple with feature dictionary from new given tuple provided as param
                    existing_fe_dict.update(new_feat_dict)
                    # update the dict as well
                    self.tuple_collection[new_wrd] = (existing_fe_dict, existing_cat, exiting_wrd, existing_sentence)
                    print>>sys.stderr," updated tuple became:",self.tuple_collection[new_wrd]
                    if existing_cat is None:
                        existing_cat = new_cat
                else:
                    self.tuple_collection[new_wrd] = tuple_instance
