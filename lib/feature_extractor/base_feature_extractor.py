#!/usr/bin/python

class BaseFeatureExtractor:
    def __init__(self):
        pass

    # method that takes instance as input and returns feature vector and optional category label
    def extract_features(self, instance):
        # Must be overriden in derived classes
        pass

    # method to extract features from a collection of instances
    # params:
    # list_of_instances: list containing instances
    # returns: list of feature vector and optional category label
    def extract_features_from_set(self, list_of_instances):
        if not list_of_instances is None:
            result = []
            for instance in list_of_instances:
                response = self.extract_features(instance)
                result.append(response)
            return result
        return None

    # method to apply transformation
    # params:
    # transformation_collection: list of transformation objects that will be applied on given text
    # text: text on which transformation is to be applied
    def apply_transformation(self, transformation_collection, instance):
        if not transformation_collection is None:
            for _transformation_instance in transformation_collection:
                text = _transformation_instance.transform(text=instance)
            return text
        else:
            return None