__author__ = 'kartik'

import sys,os,time
_prefix = 'glossextractionengine/lib/interface'

sys.path.insert(0, 'glossextractionengine.mod')

from lib.utils.arg_parser import ArgParser

# class to invoke the classification task
class ClassificationInterface:

    # params:
    # data_location: location where test dataset is located on local filesystem
    # model_file: path to model file to be used for classification
    def __init__(self, data_location=None, model_file=None):
        self.arg_obj = ArgParser()
        # this is the local location where test dataset is located
        self.data_location = data_location
        self.model_file = model_file
        self.classification_mapper = None
        self.classification_reducer = None
        self.mapper_param = None
        self.reducer_param = None

    # method to show help message
    def show_help(self):
        print ":( not enough params"
        print "usage: python classification_interface.py -cl_mapper <classification_mapper> -cl_mapper_params <mapper_params> -cl_reducer <classification_reducer> -cl_reducer_params <reducer_params> -test_dataset <dataset_location> -model <model_file>"
        exit()

    # method to check if all the necessary parameters are provided
    def check_params(self):
        # mapper and reducer params might be optional- thus they are not required
        if not self.arg_obj.args.has_key("test_dataset") or not self.arg_obj.args.has_key("model") or not self.arg_obj.args.has_key("cl_mapper") or not self.arg_obj.args.has_key("cl_reducer"):
            self.show_help()

    # method to remove the dataset directory on HDFS
    def remove_dataset_dir_on_hdfs(self):
        self.check_params()
        # remove classification input directory on HDFS
        _cmd = "hadoop fs -rmr /user/hadoop/classification_input"
        os.system(_cmd)
        time.sleep(5)

    # method to remove the classification output directory on HDFS
    def remove_output_dir_on_hdfs(self):
        self.check_params()
        # remove output directory on HDFS
        _cmd = "hadoop fs -rmr /user/hadoop/classification_output"
        os.system(_cmd)
        time.sleep(5)

    # method to load test dataset from local filesystem to HDFS
    def load_data_set_on_hdfs(self):
        self.check_params()
        # load test data on HDFS
        _cmd = "hadoop fs -put "+self.data_location+" /user/hadoop/classification_input/"
        os.system(_cmd)
        time.sleep(10)

    # method to start the classification job
    def start_classification_job(self):
        self.check_params()
        print "Launching map-reduce classification task..."

        # start classification
        # _cmd = "hadoop jar /home/hadoop/contrib/streaming/hadoop-streaming-1.0.3.jar -input /user/hadoop/classification_input -mapper glossextractionengine/lib/mapreduce/malt_parsed_feature_extraction_flow_mapper.py -file glossextractionengine/lib/mapreduce/malt_parsed_feature_extraction_flow_mapper.py -reducer 'glossextractionengine/lib/mapreduce/malt_parsed_feature_extraction_flow_reducer.py "+self.model_file+"' -file glossextractionengine/lib/mapreduce/malt_parsed_feature_extraction_flow_reducer.py -file glossextractionengine.mod -output /user/hadoop/classification_output -file trained_models/" + self.model_file + " -jobconf mapred.job.name='GlossExtractionEngine:Classification'"

        _cmd = "hadoop jar /home/hadoop/contrib/streaming/hadoop-streaming-1.0.3.jar -input /user/hadoop/classification_input -mapper '"+ self.classification_mapper

        if self.arg_obj.args.has_key("model"):
            _cmd = _cmd +" " +self.model_file

        if self.arg_obj.args.has_key("cl_mapper_params"):
            _cmd = _cmd + " " + self.mapper_param

        _cmd = _cmd + "' -file "+ self.classification_mapper +" -reducer '"+ self.classification_reducer

        if self.arg_obj.args.has_key("model"):
            _cmd = _cmd + " " +self.model_file

        if self.arg_obj.args.has_key("cl_reducer_params"):
            _cmd = _cmd + " " + self.reducer_param

        _cmd = _cmd + "' -file "+ self.classification_reducer + " -file glossextractionengine.mod -output /user/hadoop/classification_output -file " + self.model_file + " -jobconf mapred.job.name='GlossExtractionEngine:Classification'"

        print _cmd
        os.system(_cmd)
        time.sleep(5)
        print "classification task completed."

    # method to export output of classification task form HDFS to local filesystem
    def export_output_from_hdfs(self):
        self.check_params()

        # create the output directory for classification job
        if not os.path.exists("classification_output"):
            os.system("mkdir classification_output")

        # get the merged output from HDFS
        _cmd = "hadoop fs -getmerge /user/hadoop/classification_output ./classification_output/classification_output.txt"
        os.system(_cmd)
        print "Saved output[Classification output] at : ./classification_output/classification_output.txt"

    # method to launch the classification task
    def launch(self):
        self.check_params()
        self.remove_dataset_dir_on_hdfs()
        self.remove_output_dir_on_hdfs()
        self.load_data_set_on_hdfs()
        # start the feature extraction job
        self.start_classification_job()
        self.export_output_from_hdfs()


if __name__=="__main__":

    _instance = ClassificationInterface()
    _instance.arg_obj.parse(sys.argv)
    _instance.check_params()

    _instance.data_location = _instance.arg_obj.args["test_dataset"]
    _instance.model_file = _instance.arg_obj.args["model"]

    _instance.classification_mapper = _instance.arg_obj.args["cl_mapper"]
    if _instance.arg_obj.args.has_key("cl_mapper_params"):
        _instance.mapper_param = _instance.arg_obj.args["cl_mapper_params"]

    _instance.classification_reducer = _instance.arg_obj.args["cl_reducer"]

    if _instance.arg_obj.args.has_key("cl_reducer_params"):
        _instance.reducer_param = _instance.arg_obj.args["cl_reducer_params"]

    _instance.launch()
