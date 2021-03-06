#!/usr/bin/python
__author__ = 'kartik'

import random
import linecache

from lib.sampler.base_sampler import BaseSampler
from lib.utils.regex_handler import RegexHandler

# class for generating train and test dataset using random sampling
class MagicSampler(BaseSampler):

    # method to generate indices for random sampling
    def generateIndices(self,max_limit,num_elements):
        result=random.sample(range(1,max_limit),num_elements)
        return result


    # method to get positive samples
    def getPositiveSamples(self, indices):
        buff=""
        r = RegexHandler()
        _fh = open("pos_samples","w")
        _fh.close()
        for index in indices:
            line = linecache.getline(self.positiveSource,index)
            line = r.get_clean_line_for_sampling(line)
            buff = line+"\n"
            positive_sampling=open("pos_samples","a")
            positive_sampling.write(buff)
            positive_sampling.close()


    # method to get negative samples
    def getNegativeSamples(self, indices):
        buff=""
        r = RegexHandler()
        _fh = open("neg_samples","w")
        _fh.close()
        for index in indices:
            line = linecache.getline(self.negativeSource,index)
            line = r.get_clean_line_for_sampling(line)
            buff = line+"\n"
            negative_sampling=open("neg_samples","a")
            negative_sampling.write(buff)
            negative_sampling.close()