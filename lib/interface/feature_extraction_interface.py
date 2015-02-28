__author__ = 'kartik'

import sys,os,time


_prefix = 'glossextractionengine/lib/interface'

# Usage:
# python feature_extraction_interface.py <dataset_location> <train_set_size> <test_set_size>

class FeatureExtractionLauncher:

    def __init__(self, data_location):
        self.data_location = data_location
        self.training_set_size = None
        self.test_set_size = None

    def check_params(self):
        if self.data_location is None or self.training_set_size is None or self.test_set_size is None:
            print "You need to specify data_location, training_set_size and test_set_size before invoking any operation."
            exit()

    def invoke_sampling(self):
        self.check_params()
        # do sampling
        _cmd = "python "+_prefix+"/"+"sampler_interface.py "+self.data_location+"/positive_instances "+self.data_location+"/negative_instances "+ str(self.training_set_size)+" "+str(self.test_set_size)
        os.system(_cmd)
        time.sleep(5)

    def remove_dataset_dir_on_hdfs(self):
        self.check_params()
        # remove training directory on HDFS
        _cmd = "hadoop fs -rmr /user/hadoop/feature_extraction_input"
        os.system(_cmd)
        time.sleep(5)

    def remove_output_dir_on_hdfs(self):
        self.check_params()
        # remove output directory on HDFS
        _cmd = "hadoop fs -rmr /user/hadoop/feature_extraction_output"
        os.system(_cmd)
        time.sleep(5)

    def load_data_set_on_hdfs(self):
        self.check_params()
        # load new training data on HDFS
        _cmd = "hadoop fs -put Train/train_set_w_tags /user/hadoop/feature_extraction_input/"
        os.system(_cmd)
        time.sleep(10)

    def start_feature_extraction_job(self):
        self.check_params()
        print "Launching map-reduce feature extraction task..."
        # start feature extraction
        _cmd = "hadoop jar /home/hadoop/contrib/streaming/hadoop-streaming-1.0.3.jar -input /user/hadoop/feature_extraction_input -mapper glossextractionengine/lib/mapreduce/feature_extraction_flow_mapper.py -file glossextractionengine/lib/mapreduce/feature_extraction_flow_mapper.py -reducer glossextractionengine/lib/mapreduce/feature_extraction_flow_reducer.py -file glossextractionengine/lib/mapreduce/feature_extraction_flow_reducer.py -file glossextractionengine.mod -output /user/hadoop/feature_extraction_output"
        os.system(_cmd)
        time.sleep(5)
        print "feature extraction task completed."


    def export_output_from_hdfs(self):
        self.check_params()
        if not os.path.exists("feature_set_for_modeling"):
            os.system("mkdir feature_set_for_modeling")

        _cmd = "hadoop fs -getmerge /user/hadoop/feature_extraction_output ./feature_set_for_modeling/"+str(self.training_set_size)+"_output.txt"
        os.system(_cmd)
        print "Saved output[Feature set for modeling] at : feature_set_for_modeling/"+str(self.training_set_size)+"_output.txt"

    # method to perform sequence of operations before launching a map-reduce job for feature extraction
    def launch(self):
        self.check_params()
        # interact with sampling interface for sampling
        self.invoke_sampling()
        self.remove_dataset_dir_on_hdfs()
        self.remove_output_dir_on_hdfs()
        self.load_data_set_on_hdfs()
        # start the feature extraction job
        self.start_feature_extraction_job()
        self.export_output_from_hdfs()


if __name__=="__main__":
    if len(sys.argv)<4:
        print ":( not enough params"
        print "usage: python feature_extraction_interface.py <dataset_location> <train_set_size> <test_set_size>"
        # print sys.argv
    else:
        _data_location = sys.argv[1]
        training_set_size = sys.argv[2]
        test_set_size = sys.argv[3]

        l = FeatureExtractionLauncher(data_location=_data_location)
        l.training_set_size = training_set_size
        l.test_set_size = test_set_size
        l.launch()