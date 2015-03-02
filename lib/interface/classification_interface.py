__author__ = 'kartik'

import sys,os,time
_prefix = 'glossextractionengine/lib/interface'

# class to invoke the classification task
class ClassificationInterface:

    # params:
    # data_location: location where test dataset is located on local filesystem
    # model_file: path to model file to be used for classification
    def __init__(self, data_location, model_file):
        # this is the local location where test dataset is located
        self.data_location = data_location
        self.model_file = model_file

    # method to check if all the necessary parameters are provided
    def check_params(self):
        if self.data_location is None or self.model_file is None :
            print "You need to specify data_location, model file before invoking any operation."
            exit()

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
        _cmd = "hadoop jar /home/hadoop/contrib/streaming/hadoop-streaming-1.0.3.jar -input /user/hadoop/classification_input -mapper glossextractionengine/lib/mapreduce/malt_parsed_feature_extraction_flow_mapper.py -file glossextractionengine/lib/mapreduce/malt_parsed_feature_extraction_flow_mapper.py -reducer glossextractionengine/lib/mapreduce/malt_parsed_feature_extraction_flow_reducer.py -file glossextractionengine/lib/mapreduce/malt_parsed_feature_extraction_flow_reducer.py -file glossextractionengine.mod -output /user/hadoop/classification_output -file" + self.model_file + " -jobconf mapred.job.name='GlossExtractionEngine:Classification"
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
    if len(sys.argv)<3:
        print ":( not enough params"
        print "usage: python classification_interface.py <dataset_location> <model_file>"
        # print sys.argv
    else:
        _dataset_location = sys.argv[1]
        _model_file = sys.argv[2]

        c = ClassificationInterface(data_location=_dataset_location, model_file=_model_file)
        c.launch()
