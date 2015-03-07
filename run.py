__author__ = 'kartik'

import sys,os,os.path
sys.path.insert(0,".")
_prefix = 'glossextractionengine/lib/interface'

SAMPLING = "sampling"
FEATURE_EXTRACTION = "extract_features"
MODELING = "modeling"
CLASSIFICATION = "classification"
DEFAULT = "default"

from lib.utils.arg_parser import ArgParser

# class to do sampling
class InterfaceWrapper:
    def __init__(self):
        self.arg_obj = ArgParser()

    def run(self):
        # print sys.argv
        self.arg_obj.parse(sys.argv)
        print self.arg_obj.args

        if not self.arg_obj.args.has_key("operation"):
            print ":( not enough params"
            print "usage: python run.py -operation <operation_name> <parameters for operation>"
            print "******supported operations******"
            print "(1) operation name: sampling"," parameters: -sampler <sampler_implementation> -positive <positive_source_file> -negative <negative_source_file> -train_size <train_set_size> -test_size <test_set_size>"

            print "(2) operation name: extract_features"," parameters: <dataset_location> <train_set_size> <test_set_size>"

            return

        if self.arg_obj.args["operation"] == SAMPLING:
            self.run_sampling()

        if self.arg_obj.args["operation"] == FEATURE_EXTRACTION:
            self.run_feature_extraction()

        if self.arg_obj.args["operation"] == MODELING:
            self.run_modeling()

        if self.arg_obj.args["operation"] == CLASSIFICATION:
            self.run_classification()

        if self.arg_obj.args["operation"] == DEFAULT:
            self.run_default_flow()

    # method to run sampling
    def run_sampling(self):
        # launch sampling
        _cmd = "python "+_prefix+"/"+"sampler_interface.py "+"-sampler " +self.arg_obj.args["sampler"]+" -positive "+self.arg_obj.args["positive"]+" -negative "+self.arg_obj.args["negative"]+" -train_size " +self.arg_obj.args["train_size"] +" -test_size " +self.arg_obj.args["test_size"]
        print "cmd: ",_cmd
        self.invoke(_cmd)
        pass

    # method to run feature extraction
    def run_feature_extraction(self):
        if len(sys.argv)<5:
                print "extract_features: not enough params"
                print " usage: python run.py extract_features <feature_extraction_mapper> <mapper_params> <feature_extraction_reducer> <reducer_params> <dataset_location> <train_set_size> <test_set_size>"
        else:
            # launch feature extraction here
            args_list = sys.argv[2:]
            _cmd = "python "+_prefix+"/"+"feature_extraction_interface.py "+' '.join(args_list)
            print "cmd: ",_cmd
            self.invoke(_cmd)
            pass

    # method to run modeling
    def run_modeling(self):
        if len(sys.argv)<3:
                print "modeling: not enough params"
                print " usage: python run.py modeling <feature_set_file_location> <model_name_to_save_as>"
                print "or"
                print " usage: python run.py modeling <feature_set_location_directory>"
        else:
            # launch sampling
            args_list = sys.argv[2:]
            _cmd = "python "+_prefix+"/"+"modeler_interface.py "+' '.join(args_list)
            print "cmd: ",_cmd
            self.invoke(_cmd)
            pass

    # method to run the classification
    def run_classification(self):
        if len(sys.argv)<3:
                print "classification: not enough params"
                print " usage: python run.py modeling <dataset_location> <model_file>"
        else:
            # launch classification
            args_list = sys.argv[2:]
            _cmd = "python "+_prefix+"/"+"classification_interface.py "+' '.join(args_list)
            print "cmd: ",_cmd
            self.invoke(_cmd)
            pass

    # method to run default behavior- here framework handles everything- sampling, feature extraction, modeling
    # user just needs to provide required parameters
    # this runs: sampling->feature extraction->modeling
    def run_default_flow(self):
        if len(sys.argv)<5:
                print "default: not enough params"
                #                       0       1       2                   3               4               5
                print " usage: python run.py default <train_dataset_location> <sampling_train_set_size> <sampling_test_set_size> <test_dataset_location> <model_name>"
        else:
            # launch feature extraction
            args_list = sys.argv[2:5]
            _cmd = "python "+_prefix+"/"+"feature_extraction_interface.py "+' '.join(args_list)
            print "cmd: ",_cmd
            self.invoke(_cmd)

            # if feature extraction was successful then proceed for modeling
            if os.path.exists("./feature_set_for_modeling"):
                print "Launching modeler with extracted feature set..."
                # launch modeling with default feature set location as input to modeler
                _cmd = "python "+_prefix+"/"+"modeler_interface.py ./feature_set_for_modeling"
                self.invoke(_cmd)
            else:
                print "unable to find the directory 'feature_set_for_modeling'"

            # if the modeling was successful then proceed for classification
            if os.path.exists("./trained_models"):
                print "Launching classification with trained model from ./trained_models"
                # launch classification
                args_list = sys.argv[5:]
                _cmd = "python "+_prefix+"/"+"classification_interface.py "+' '.join(args_list)
                self.invoke(_cmd)
            else:
                print "unable to find the directory 'trained_models'"

    # method to invoke the commands
    def invoke(self, cmd):
        os.system(cmd)

i = InterfaceWrapper()
i.run()