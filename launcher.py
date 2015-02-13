__author__ = 'kartik'

import sys,os,time

if __name__=="__main__":
    if len(sys.argv)<4:
        print ":( not enough params"
        print "usage: python launcher.py <dataset_location> <train_set_size> <test_set_size>"
        # print sys.argv
    else:
        _data_location = sys.argv[1]
        training_set_size = sys.argv[2]
        test_set_size = sys.argv[3]

        # do sampling
        _cmd = "python glossextractionengine/samplingStub.py "+_data_location+"/positive_instances "+_data_location+"/negative_instances "+ str(training_set_size)+" "+str(test_set_size)
        os.system(_cmd)
        time.sleep(5)

        # remove training directory on HDFS
        _cmd = "hadoop fs -rmr /user/hadoop/train"
        os.system(_cmd)
        time.sleep(5)

        # remove output directory on HDFS
        _cmd = "hadoop fs -rmr /user/hadoop/output"
        os.system(_cmd)
        time.sleep(5)

        # load new training data on HDFS
        _cmd = "hadoop fs -put Train/train_set_w_tags /user/hadoop/train/"
        os.system(_cmd)
        time.sleep(10)

        # start feature extraction
        _cmd = "hadoop jar /home/hadoop/contrib/streaming/hadoop-streaming-1.0.3.jar -input /user/hadoop/train -mapper glossextractionengine/lib/mapreduce/feature_extraction_flow_mapper.py -file glossextractionengine/lib/mapreduce/feature_extraction_flow_mapper.py -reducer glossextractionengine/lib/mapreduce/feature_extraction_flow_reducer.py -file glossextractionengine/lib/mapreduce/feature_extraction_flow_reducer.py -file glossextractionengine.mod -output /user/hadoop/output"
        os.system(_cmd)
        time.sleep(5)
        print "completed hadoop job..."

        _cmd = "hadoop fs -getmerge /user/hadoop/output ./"+str(training_set_size)+"_output.txt"
        os.system(_cmd)
        print "saved output: "+str(training_set_size)+"_output.txt"


