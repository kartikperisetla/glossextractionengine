#!/usr/bin/python
__author__ = 'kartik'

import random
import linecache

from lib.sampler.base_sampler import BaseSampler
from lib.utils.regex_handler import RegexHandler


class RandomSampler(BaseSampler):

    # method to generate indices for random sampling
    def generateIndices(self,max_limit,num_elements):
        result=random.sample(range(1,max_limit),num_elements);
        return result


    # method to get positive samples
    def getPositiveSamples(self, indices):
        buff=""
        r = RegexHandler()

        for index in indices:
            line = linecache.getline(self.positiveSource,index)
            line = r.get_clean_line_for_sampling(line)

            if line.strip()=="":
                print "+ve blank at:",index
            else:
                buff=buff+line+"\n"

        positive_sampling=open("pos_samples","w")
        positive_sampling.write(buff)
        positive_sampling.close()
        print "gen +ve samples:",len(indices)

    # method to get negative samples
    def getNegativeSamples(self, indices):
        buff=""
        r = RegexHandler()

        for index in indices:
            line = linecache.getline(self.negativeSource,index)
            line = r.get_clean_line_for_sampling(line)

            if line.strip()=="":
                print "-ve blank at:",index
            else:
                buff=buff+line+"\n"


        buff=buff[:-1]
        negative_sampling=open("neg_samples","w")
        negative_sampling.write(buff)
        negative_sampling.close()
        print "gen -ve samples:",len(indices)