__author__ = 'kartik'

import sys,os
from lib.modeler.pos_context_sequence_modeler import POSContextSequenceModeler

# class that provides interface to modeling
class ModelingStub:

    # start the modeling using the feature set
    def model(self):
        if len(sys.argv)<2:
            print ":( not enough params"
            print "usage: python modeler_interface.py <feature_set_file_location> <model_name_to_save_as>"
            print "==or=="
            print "usage: python modeler_interface.py <feature_set_location_directory>"
            return

        _feature_set_location = sys.argv[1]

        if os.path.isfile(_feature_set_location):
            if len(sys.argv)<3:
                print ":( not enough params"
                print "usage: python modeler_interface.py <feature_set_file_location> <model_name_to_save_as>"
                print "==or=="
                print "usage: python modeler_interface.py <feature_set_location_directory>"
                return

            _model_name = sys.argv[2]
            _instance = POSContextSequenceModeler(feature_set_location = _feature_set_location)
            _instance.train()
            _instance.save_model(name=_model_name,location="Saved_Models")

            print "ModelingStub: modeling done for given feature set file."

        if os.path.isdir(_feature_set_location):
            print "ModelingStub:looking into feature set directory..."
            file_list = os.listdir(_feature_set_location)
            for _file in file_list:
                _path = _feature_set_location+"/"+_file
                _model_name = _file+".model"

                _instance = POSContextSequenceModeler(feature_set_location = _path)
                _instance.train()
                print "ModelingStub:trained the model.about to save."
                _instance.save_model(name=_model_name,location="Saved_Models")
                print "ModelingStub:modeling done for:",_file


            print "ModelingStub: modeling done for all files in directory provided."


m= ModelingStub()
m.model()
