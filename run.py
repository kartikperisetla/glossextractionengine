__author__ = 'kartik'

import sys,os

SAMPLING = "sampling"
FEATURE_EXTRACTION = "extract_features"
MODELING = "modeling"
DEFAULT = "default"

# class to do sampling
class InterfaceWrapper:

    def run(self):
        print sys.argv
        if len(sys.argv)<2:
            print ":( not enough params"
            print "usage: python run.py <operation_name> <parameters for operation>"
            print "******supported operations******"
            print "(1) operation name: sampling"," parameters: <positive_source_file> <negative_source_file> <train_set_size> <test_set_size>"

            print "(2) operation name: extract_features"," parameters: <dataset_location> <train_set_size> <test_set_size>"

            return

        if sys.argv[1] == SAMPLING:
            self.run_sampling()

        if sys.argv[1] == FEATURE_EXTRACTION:
            self.run_feature_extraction()

        if sys.argv[1]==MODELING:
            self.run_modeling()

        if sys.argv[1]==DEFAULT:
            self.run_default_flow()

    # method to run default behavior- here framework handles everything- sampling, feature extraction, modeling
    # user just needs to provide required paramers
    def run_default_flow(self):
        pass

    # method to run sampling
    def run_sampling(self):
        if len(sys.argv)<6:
                print "sampling: not enough params"
                print " usage: python run.py sampling <positive_source_file> <negative_source_file> <train_set_size> <test_set_size>"

        else:
            # launch sampling
            args_list = sys.argv[2:]
            _cmd = "python sample_interface.py "+' '.join(args_list)
            print "cmd: ",_cmd
            self.invoke(_cmd)
            pass

    # method to run feature extraction
    def run_feature_extraction(self):
        if len(sys.argv)<5:
                print "extract_features: not enough params"
                print " usage: python run.py extract_features <dataset_location> <train_set_size> <test_set_size>"
        else:
            # launch feature extraction here
            args_list = sys.argv[2:]
            _cmd = "python feature_extraction_interface.py "+' '.join(args_list)
            print "cmd: ",_cmd
            self.invoke(_cmd)
            pass

    # method to run modeling
    def run_modeling(self):
        if len(sys.argv)<3:
                print "modeling: not enough params"
                print " usage: python run.py modeling <feature_set_file_location> <model_name_to_save_as>"
                print "or"
                print " usage: python modeler_interface.py <feature_set_location_directory>"
        else:
            # launch sampling
            args_list = sys.argv[2:]
            _cmd = "python modeler_interface.py "+' '.join(args_list)
            print "cmd: ",_cmd
            self.invoke(_cmd)
            pass


    def invoke(self, cmd):
        os.system(cmd)


i = InterfaceWrapper()
i.run()