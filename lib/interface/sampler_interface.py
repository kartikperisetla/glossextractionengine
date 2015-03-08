#!/usr/bin/python

__author__ = 'kartik'

import sys
sys.path.insert(0, 'glossextractionengine.mod')


from lib.sampler.random_sampler import RandomSampler
from lib.utils.dynamic_class_loader import DynamicClassLoader
from lib.utils.arg_parser import ArgParser

_prefix = 'glossextractionengine/lib/interface'

# class to do sampling
class SamplingInterface:
    def __init__(self):
        self.arg_obj = ArgParser()

    # method that checks if required parameters are there or not
    # returns False if the required params are missing
    # returns True if all the required params are provided
    def check_params(self):
        print "sampler checking:",self.arg_obj.args
        if not self.arg_obj.args.has_key("sampler") or not self.arg_obj.args.has_key("positive") or not self.arg_obj.args.has_key("negative") or not self.arg_obj.args.has_key("train_size") or not self.arg_obj.args.has_key("test_size"):
            return False
        else:
            return True

    def sample(self):
        self.arg_obj.parse(sys.argv)
        print self.arg_obj.args

        if not self.check_params():
            print ":( not enough params"
            print " usage: python sample_interface.py -sampler <sampler_implementation> -positive <positive_source_file> -negative <negative_source_file> -train_size <train_set_size> -test_size <test_set_size>"
            return

        sampler_implementation = self.arg_obj.args["sampler"]
        positive_source_file = self.arg_obj.args["positive"]
        negative_source_file = self.arg_obj.args["negative"]
        train_set_size = self.arg_obj.args["train_size"]
        test_set_size = self.arg_obj.args["test_size"]

        # this dynamically loads the concrete implementation of sampler
        _dyn_cls_loader = DynamicClassLoader()
        _class_placeholder = _dyn_cls_loader.load(sampler_implementation)
        print "SamplingInterface:Instantiating:",_class_placeholder

        # instantiating the sampler
        _instance = _class_placeholder(positive_source_file, negative_source_file)

        _instance.generateDatasets(train_set_size, test_set_size)

        print "SamplingStub: sampling done."

s = SamplingInterface()
s.sample()


