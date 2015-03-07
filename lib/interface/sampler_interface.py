#!/usr/bin/python

__author__ = 'kartik'

import sys
sys.path.insert(0, 'glossextractionengine.mod')

from lib.sampler.random_sampler import RandomSampler
from lib.utils.dynamic_class_loader import DynamicClassLoader

_prefix = 'glossextractionengine/lib/interface'

# class to do sampling
class SamplingInterface:

    def sample(self):
        if len(sys.argv)<5:
            print ":( not enough params"
            print " usage: python sample_interface.py <sampler_implementation> <positive_source_file> <negative_source_file> <train_set_size> <test_set_size>"
            return

        sampler_implementation = sys.argv[1]
        positive_source_file = sys.argv[2]
        negative_source_file = sys.argv[3]
        train_set_size = sys.argv[4]
        test_set_size = sys.argv[5]

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


