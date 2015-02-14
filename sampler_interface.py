#!/usr/bin/python

__author__ = 'kartik'

import sys
from lib.sampler.random_sampler import RandomSampler

# class to do sampling
class SamplingStub:

    def sample(self):
        if len(sys.argv)<5:
            print " usage: python SamplingStub.py <positive_source_file> <negative_source>file> <train_set_size> <test_set_size>"
            return

        positive_source_file = sys.argv[1]
        negative_source_file = sys.argv[2]
        train_set_size = sys.argv[3]
        test_set_size = sys.argv[4]

        _instance = RandomSampler(positive_source_file, negative_source_file)
        _instance.generateDatasets(train_set_size, test_set_size)

        print "SamplingStub: sampling done."


s= SamplingStub()
s.sample()


