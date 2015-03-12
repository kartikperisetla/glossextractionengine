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
        print '*'*100
        print "Run got arguments:",self.arg_obj.args
        print '*'*100

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
        print '*'*100
        print "run: Invoking Sampling:\n",_cmd
        print '*'*100
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
        _cmd = "python "+_prefix+"/"+"modeler_interface.py " + self.arg_obj.get_string()
        print '*'*100
        print "run: Invoking Modeling:\n",_cmd
        print '*'*100
        self.invoke(_cmd)
        pass

    # method to run the classification
    def run_classification(self):
        # launch classification
        _cmd = "python "+_prefix+"/"+"classification_interface.py " + self.arg_obj.get_string()
        print '*'*100
        print "run: Invoking Classification:\n",_cmd
        print '*'*100
        self.invoke(_cmd)
        pass


    # method to check if all the necessary parameters are provided for default flow
    def check_params(self):
        # this checks for all params required to execute the default flow of the framework
        # mapper and reducer params might be optional- thus they are not required
        if not self.arg_obj.args.has_key("fe_mapper") or not self.arg_obj.args.has_key("fe_reducer") or not self.arg_obj.args.has_key("train_dataset") or not self.arg_obj.args.has_key("train_size") or not self.arg_obj.args.has_key("test_size") or not self.arg_obj.args.has_key("cl_mapper") or not self.arg_obj.args.has_key("cl_reducer") :
            self.show_help()

    # method to run default behavior- here framework handles everything- sampling, feature extraction, modeling
    # user just needs to provide required parameters
    # this runs: sampling->feature extraction->modeling
    def run_default_flow(self):
        self.check_params()

        # launch feature extraction
        self.run_feature_extraction()

        # if feature extraction was successful then proceed for modeling
        if os.path.exists("./feature_set_for_modeling"):
            print "Launching modeler with extracted feature set..."
            self.run_modeling()
            # if model was successfully generated, set the model parameter for classification flow
            self.arg_obj.args["model"] = "trained_models/"+str(self.arg_obj.args["train_size"])+"_output.model"
        else:
            print "unable to find the directory 'feature_set_for_modeling'"

        # if the modeling was successful then proceed for classification
        if os.path.exists("./trained_models"):
            print "Launching classification with trained model from ./trained_models"
            # launch classification
            self.run_classification()
        else:
            print "unable to find the directory 'trained_models'"

    # method to invoke the commands
    def invoke(self, cmd):
        os.system(cmd)

i = InterfaceWrapper()
i.run()