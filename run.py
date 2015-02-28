__author__ = 'kartik'

import sys

SAMPLING = "sampling"
FEATURE_EXTRACTION = "extract_features"
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
            if len(sys.argv)<6:
                print "sampling: not enough params"
                print " usage: python run.py sampling <positive_source_file> <negative_source_file> <train_set_size> <test_set_size>"
                return
            else:
                # launch sampling
                args_list = sys.argv[2:]
                _cmd = "python sample_interface.py "+' '.join(args_list)
                print "cmd: ",_cmd
                pass

        if sys.argv[1] == FEATURE_EXTRACTION:
            if len(sys.argv)<5:
                print "extract_features: not enough params"
                print " usage: python run.py extract_features <dataset_location> <train_set_size> <test_set_size>"
                return
            else:
                # launch feature extraction here
                args_list = sys.argv[2:]
                _cmd = "python feature_extraction_interface.py "+' '.join(args_list)
                print "cmd: ",_cmd
                pass


i = InterfaceWrapper()
i.run()