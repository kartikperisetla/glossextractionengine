__author__ = 'kartik'

import sys,os
sys.path.insert(0, 'glossextractionengine.mod')

from lib.utils.arg_parser import ArgParser
from lib.modeler.pos_context_sequence_modeler import POSContextSequenceModeler

# class that provides interface to modeling
class ModelingStub:
    def __init__(self):
        self.arg_obj = ArgParser()

    # method that checks if required parameters are there or not
    # returns False if the required params are missing
    # returns True if all the required params are provided
    def check_params(self):
        print "modeler checking:",self.arg_obj.args
        if not self.arg_obj.args.has_key("feature_set_location"):
            return False
        else:
            return True
    # method to show error message
    def show_help(self):
        print ":( not enough params"
        print "usage: python modeler_interface.py -feature_set_location <feature_set_file_location> -model_name <model_name_to_save_as>"
        print "==or=="
        print "usage: python modeler_interface.py -feature_set_location <feature_set_location_directory>"
        exit()

    # start the modeling using the feature set
    def model(self):
        self.arg_obj.parse(sys.argv)

        if not self.check_params():
            self.show_help()

        _feature_set_location = self.arg_obj.args["feature_set_location"]

        if os.path.isfile(_feature_set_location):
            # if given a file path and not provided the model name to save as
            if not self.arg_obj.args.has_key("model_name"):
                self.show_help()

            _model_name = self.arg_obj.args["model_name"]
            _instance = POSContextSequenceModeler(feature_set_location = _feature_set_location)
            _instance.train()
            _instance.save_model(name=_model_name,location="trained_models")

            print "ModelingStub: modeling done for given feature set file."

        if os.path.isdir(_feature_set_location):
            print "ModelingStub: looking into feature set directory..."

            # filter only feature set files with .txt extension
            file_list = [fn for fn in os.listdir(_feature_set_location) if fn.endswith(('.txt'))]

            for _file in file_list:
                _path = _feature_set_location+"/"+_file

                _coll = _file.split(".")

                _model_name = _coll[0]+".model"

                _instance = POSContextSequenceModeler(feature_set_location = _path)
                _instance.train()
                print "ModelingStub: trained the model.about to save."
                _instance.save_model(name=_model_name,location="trained_models")
                print "ModelingStub: modeling done for:",_file

            print "ModelingStub: modeling done for all files in directory provided."


m= ModelingStub()
m.model()