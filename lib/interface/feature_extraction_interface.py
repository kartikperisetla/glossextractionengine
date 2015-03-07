__author__ = 'kartik'

import sys,os,time

_prefix = 'glossextractionengine/lib/interface'

# Usage:
# python feature_extraction_interface.py <dataset_location> <train_set_size> <test_set_size>

class FeatureExtractionInterface:

    def __init__(self, data_location=None):
        self.data_location = data_location
        self.sampler = None
        self.feature_extraction_mapper = None
        self.feature_extraction_reducer = None
        self.mapper_param = None
        self.reducer_param = None
        self.training_set_size = None
        self.test_set_size = None

    # method that checks if required parameters are there or not
    def check_params(self):
        if self.data_location is None or self.training_set_size is None or self.test_set_size is None or self.feature_extraction_mapper is None or self.feature_extraction_reducer is None or self.mapper_param is None or self.reducer_param is None:
            print "You need to specify data_location, training_set_size and test_set_size before invoking any operation."
            exit()

    # method that invokes sampling- it assumes that positive instances file is named 'positive_instances' and negative instances file is named 'negative_instances'
    def invoke_sampling(self):
        self.check_params()
        # do sampling
        _cmd = "python "+_prefix+"/"+"sampler_interface.py "+self.sampler+"  "+self.data_location+"/positive_instances "+self.data_location+"/negative_instances "+ str(self.training_set_size)+" "+str(self.test_set_size)
        os.system(_cmd)
        time.sleep(5)

    # method that removes the dataset directory on HDFS
    def remove_dataset_dir_on_hdfs(self):
        self.check_params()
        # remove training directory on HDFS
        _cmd = "hadoop fs -rmr /user/hadoop/feature_extraction_input"
        os.system(_cmd)
        time.sleep(5)

    # method that removes the output directory on HDFS
    def remove_output_dir_on_hdfs(self):
        self.check_params()
        # remove output directory on HDFS
        _cmd = "hadoop fs -rmr /user/hadoop/feature_extraction_output"
        os.system(_cmd)
        time.sleep(5)

    # method that loads the dataset into HDFS
    def load_data_set_on_hdfs(self):
        self.check_params()
        # load new training data on HDFS
        _cmd = "hadoop fs -put Train/train_set_w_tags /user/hadoop/feature_extraction_input/"
        os.system(_cmd)
        time.sleep(10)

    # method that starts the feature extraction job
    def start_feature_extraction_job(self):
        self.check_params()
        print "Launching map-reduce feature extraction task..."
        # start feature extraction
        # _cmd = "hadoop jar /home/hadoop/contrib/streaming/hadoop-streaming-1.0.3.jar -input /user/hadoop/feature_extraction_input -mapper glossextractionengine/lib/mapreduce/feature_extraction_flow_mapper.py -file glossextractionengine/lib/mapreduce/feature_extraction_flow_mapper.py -reducer glossextractionengine/lib/mapreduce/feature_extraction_flow_reducer.py -file glossextractionengine/lib/mapreduce/feature_extraction_flow_reducer.py -file glossextractionengine.mod -output /user/hadoop/feature_extraction_output -jobconf mapred.job.name='GlossExtractionEngine:FeatureExtraction'"

        _cmd = "hadoop jar /home/hadoop/contrib/streaming/hadoop-streaming-1.0.3.jar -input /user/hadoop/feature_extraction_input -mapper '"+ self.feature_extraction_mapper + self.mapper_param +"' -file "+ self.feature_extraction_mapper +" -reducer '"+ self.feature_extraction_reducer + self.reducer_param +"' -file "+ self.feature_extraction_reducer +" -file glossextractionengine.mod -output /user/hadoop/feature_extraction_output -jobconf mapred.job.name='GlossExtractionEngine:FeatureExtraction'"
        os.system(_cmd)
        time.sleep(5)
        print "feature extraction task completed."

    # method that exports the result of feature extraction from HDFS to local file system
    def export_output_from_hdfs(self):
        self.check_params()

        # create the output directory for featuer extraction job
        if not os.path.exists("feature_set_for_modeling"):
            os.system("mkdir feature_set_for_modeling")

        # remove previous version of the feature set file in the output directory
        if os.path.exists("./feature_set_for_modeling/"+str(self.training_set_size)+"_output.txt"):
            print "FeatureExtractionInterface: File already exists.. removing it :","./feature_set_for_modeling/"+str(self.training_set_size)+"_output.txt"
            os.remove("./feature_set_for_modeling/"+str(self.training_set_size)+"_output.txt")

        # get the merged output from HDFS
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
    if len(sys.argv)<7:
        print ":( not enough params"
        print "usage: python feature_extraction_interface.py <feature_extraction_mapper> <mapper_params> <feature_extraction_reducer> <reducer_params> <dataset_location> <train_set_size> <test_set_size>"

    else:
        _instance = FeatureExtractionInterface()
        # set mapper
        _instance.feature_extraction_mapper = sys.argv[1]
        # set mapper param
        _instance.mapper_param = sys.argv[2]

        # set reducer
        _instance.feature_extraction_reducer = sys.argv[3]
        # set reducer param
        _instance.reducer_param = sys.argv[4]

        # get other param
        _data_location = sys.argv[5]
        training_set_size = sys.argv[6]
        test_set_size = sys.argv[7]

        _instance.data_location = _data_location
        _instance.training_set_size = training_set_size
        _instance.test_set_size = test_set_size
        _instance.launch()