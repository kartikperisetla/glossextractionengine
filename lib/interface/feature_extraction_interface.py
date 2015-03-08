__author__ = 'kartik'

import sys,os,time
sys.path.insert(0, 'glossextractionengine.mod')

from lib.utils.arg_parser import ArgParser

_prefix = 'glossextractionengine/lib/interface'

# Usage:
# python feature_extraction_interface.py <dataset_location> <train_set_size> <test_set_size>

class FeatureExtractionInterface:

    def __init__(self, data_location=None):
        self.arg_obj = ArgParser()

        self.data_location = data_location
        self.sampler = None
        self.feature_extraction_mapper = None
        self.feature_extraction_reducer = None
        self.mapper_param = None
        self.reducer_param = None
        self.training_set_size = None
        self.test_set_size = None



    # method that checks if required parameters are there or not
    # returns False if the required params are missing
    # returns True if all the required params are provided
    def check_params(self):
        if not self.arg_obj.args.has_key("fe_mapper") or  not self.arg_obj.args.has_key("fe_reducer") or not self.arg_obj.args.has_key("train_dataset") or not self.arg_obj.args.has_key("train_size") or not self.arg_obj.args.has_key("test_size") :
            return False
        else:
            return True

    # method that invokes sampling- it assumes that positive instances file is named 'positive_instances' and negative instances file is named 'negative_instances'
    def invoke_sampling(self):
        self.check_params()
        # do sampling

        # using default sampler if not provided sampler in param list
        if not self.arg_obj.args.has_key("sampler"):
            _sampler = "lib.sampler.random_sampler.RandomSampler"
        else:
            _sampler = self.arg_obj.args["sampler"]

        _cmd = "python "+_prefix+"/"+"sampler_interface.py "+self.arg_obj.get_string()
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

        _cmd = "hadoop jar /home/hadoop/contrib/streaming/hadoop-streaming-1.0.3.jar -input /user/hadoop/feature_extraction_input -mapper '"+ self.feature_extraction_mapper

        # use parameters for mapper job if they are provided
        if not self.mapper_param is None:
            _cmd = _cmd + self.mapper_param

        _cmd = _cmd + "' -file "+ self.feature_extraction_mapper +" -reducer '"+ self.feature_extraction_reducer

        # use parameters for reducer job if they are provided
        if not self.reducer_param is None:
            _cmd = _cmd + self.reducer_param

        _cmd = _cmd + "' -file "+ self.feature_extraction_reducer +" -file glossextractionengine.mod -output /user/hadoop/feature_extraction_output -jobconf mapred.job.name='GlossExtractionEngine:FeatureExtraction'"

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

        _instance = FeatureExtractionInterface()
        _instance.arg_obj.parse(sys.argv)
        print _instance.arg_obj.args

        if not _instance.check_params():
            print ":( not enough params"
            print "usage: python feature_extraction_interface.py -fe_mapper <feature_extraction_mapper> -fe_mapper_params  <mapper_params> -fe_reducer <feature_extraction_reducer> -fe_reducer_params <reducer_params> -train_dataset <dataset_location> -train_size <train_set_size> -test_size <test_set_size>"
            exit()

        # set mapper
        _instance.feature_extraction_mapper = _instance.arg_obj.args["fe_mapper"]

        # get mapper params if provided
        if _instance.arg_obj.args.has_key("fe_mapper_params"):
            # set mapper param
            _instance.mapper_param = _instance.arg_obj.args["fe_mapper_params"]

        # set reducer
        _instance.feature_extraction_reducer = _instance.arg_obj.args["fe_reducer"]

        # get reducer params if provided
        if _instance.arg_obj.args.has_key("fe_reducer_params"):
            # set reducer param
            _instance.reducer_param = _instance.arg_obj.args["fe_reducer_params"]

        # get other param
        _data_location = _instance.arg_obj.args["train_dataset"]
        training_set_size = _instance.arg_obj.args["train_size"]
        test_set_size = _instance.arg_obj.args["test_size"]

        _instance.data_location = _data_location
        _instance.training_set_size = training_set_size
        _instance.test_set_size = test_set_size
        _instance.launch()