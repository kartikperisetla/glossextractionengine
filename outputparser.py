'''
Created on Apr 2, 2015

@author: kartik
'''

import os,sys
import pickle, ast

class OutputParser:
    def __init__(self, model_filepath, output_directory_path):
        print "OutputParser:init"
        self.model_path = model_filepath
        self.output_directory_path = output_directory_path + "/classification_output.txt"
        _pobj = open(model_filepath,"rb")
        self.classifier = pickle.load(_pobj)
    
    def get_report(self, output_directory_path):
        output_directory_path = output_directory_path +"/"
        # add report generation part here
        
    def get_instance_count(self, threshold_score):
        
        file_obj = open(self.output_directory_path,"r")
        cnt = 0
        for line in file_obj:
            output_tuple = ast.literal_eval(line)
            word, result, feature_dict,line, pos_prob = output_tuple
            if float((pos_prob*100)) >= float(threshold_score):
                cnt+=1
#                 print word," ",pos_prob*100
#         print "instances with >=",threshold_score," is ",str(cnt)
        print threshold_score,"\t",str(cnt)
        return cnt
        
if __name__=="__main__":
    if len(sys.argv)<3:
        print " usage:outputparser.py <model_file_path> <output_directory_path> <threshold_score>"
        exit()
    
    model_path = sys.argv[1]
    output_path = sys.argv[2]
    op = OutputParser(model_path, output_path)
    for i in range(60,101,1):
        threshold_score = i
        op.get_instance_count(threshold_score)