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

    # method to show help message
    def show_help(self):
        print ":( not enough params"
        print "usage: python run.py -operation <operation_name> <parameters for operation>"
        print "******supported operations******"
        print "(1) operation name: sampling"," parameters: -sampler <sampler_implementation> -positive <positive_source_file> -negative <negative_source_file> -train_size <train_set_size> -test_size <test_set_size>"

        print "(2) operation name: extract_features"," parameters: -fe_mapper <feature_extraction_mapper> -fe_mapper_params  <mapper_params> -fe_reducer <feature_extraction_reducer> -fe_reducer_params <reducer_params> -train_dataset  <dataset_location> -train_size <train_set_size> -test_size <test_set_size>"

        print "(3) operation name: modeling","\n-->parameters when using single feature set file: -feature_set_location <feature_set_file_location> -model_name <model_name_to_save_as>","\n-->parameters when using directory containing feature set files: -feature_set_location <feature_set_location_directory>"

        print "(4) operation name: classification"," parameters: -cl_mapper <classification_mapper> -cl_mapper_params <mapper_params> -cl_reducer <classification_reducer> -cl_reducer_params <reducer_params> -test_dataset <dataset_location> -model <model_file>"

        exit()

    def run(self):
        # print sys.argv
        self.arg_obj.parse(sys.argv)
        print self.arg_obj.args

        if not self.arg_obj.args.has_key("operation"):
            self.show_help()

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
        _cmd = "python "+_prefix+"/"+"sampler_interface.py " + self.arg_obj.get_string()
        print "cmd: ",_cmd
        self.invoke(_cmd)
        pass

    # method to run feature extraction
    def run_feature_extraction(self):
        # launch feature extraction here
        _cmd = "python "+_prefix+"/"+"feature_extraction_interface.py " + self.arg_obj.get_string()
        print "cmd: ",_cmd
        self.invoke(_cmd)
        pass

    # method to run modeling
    def run_modeling(self):
        # launch modeling
        args_list = sys.argv[2:]
        _cmd = "python "+_prefix+"/"+"modeler_interface.py " + self.arg_obj.get_string()
        print "cmd: ",_cmd
        self.invoke(_cmd)
        pass

    # method to run the classification
    def run_classification(self):
        # launch classification
        args_list = sys.argv[2:]
        _cmd = "python "+_prefix+"/"+"classification_interface.py " + self.arg_obj.get_string()
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