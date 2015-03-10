__author__ = 'kartik'

import os,re,time,shutil

# class for do sampling
class BaseSampler:
    def __init__(self, positive_dataset_file, negative_dataset_file,set_size=None):
        print "BaseSampler:init"
        self.max_positive = self.count_records(positive_dataset_file)
        self.max_negative = self.count_records(negative_dataset_file)
        self.positiveSource = positive_dataset_file
        self.negativeSource = negative_dataset_file
        os.system("rm -rf  Train")
        os.system("rm -rf  Test")

        pass

    def count_records(self,file):
        file_obj = open(file,"r")
        count_lines = len(file_obj.readlines())
        file_obj.close()
        return count_lines

    # method to generate indices for random sampling
    def generateIndices(self, max_limit, num_elements):
        # Must be defined in derived implementation
        pass

    # method to get positive samples
    def getPositiveSamples(self, indices):
        pass

    # method to get negative samples
    def getNegativeSamples(self, indices):
        pass

    # method to do sampling by picking given indices
    # params:
    # indices: collection of indexes to pick positive and negative samples for this sampling transaction
    def doSampling(self, positive_indices, negative_indices):
        self.getPositiveSamples(positive_indices)
        self.getNegativeSamples(negative_indices)

    # method to generate training set
    def generateTrainingSet(self, positive_indices, negative_indices):
        self.doSampling( positive_indices, negative_indices)

    # method to generate training set
    def generateTestSet(self, positive_indices, negative_indices):
        self.doSampling( positive_indices, negative_indices)

    # method that removes the tags with training instances from this format: '<class> <tag> | <definition>' to bring to format : '<class> | <definition>''
    def prepareTaglessTrainSet(self):
        shutil.copyfile("Train/train_set","Train/train_set_w_tags")
        f=open("Train/train_set_w_tags","r")
        buff=f.read()
        f.close()
        buff2=re.sub("'.*? \|", '|', buff)
        os.remove("Train/train_set")
        n_f=open("Train/train_set","w")
        n_f.write(buff2)
        n_f.close()

    # method for bounded wait
    def waitFor(self, path):
        while not (os.path.exists(path)):
            print "waiting for ",path
            time.sleep(10)
        return

    def execute(self,  list_of_cmd):
        import subprocess
        for cmd in list_of_cmd:
            print ">",cmd
            result = subprocess.check_output(cmd, shell=True)
            print result


    def merge_files(self,source_list,target):
        _target=open(target,"w")
        for f_name in source_list:
            file =open(f_name,"r")
            _target.write(file.read())
        _target.close()

    # method to prepare training dataset
    def prepareTrainSet(self, train_positive_index_list, train_negative_index_list):
        print "preparing train set"
        self.generateTrainingSet(train_positive_index_list, train_negative_index_list)

        self.waitFor("pos_samples")
        shutil.move("pos_samples","Train/")

        self.waitFor("neg_samples")
        shutil.move("neg_samples","Train/")

        self.waitFor("Train/pos_samples")
        self.waitFor("Train/neg_samples")

        self.merge_files(["Train/pos_samples","Train/neg_samples"],"Train/train_set")

        self.waitFor("Train/train_set")
        self.prepareTaglessTrainSet()

    # method to prepare labeled test dataset
    def prepareLabeledTest(self):
        self.waitFor("Test/test_set")
        shutil.copyfile("Test/test_set","Test/labeled_test")

        self.waitFor("Test/labeled_test")
        f=open("Test/labeled_test","r")
        buff=f.read()
        f.close()
        buff1=re.sub(".*? \|", '|', buff)
        buff2=re.sub("'.*? \|", '|', buff)

        os.remove("Test/test_set")
        n_f=open("Test/test_set","w")
        n_f.write(buff1)
        n_f.close()

        o_f=open("Test/labeled_test_wo_tag","w")
        o_f.write(buff2)
        o_f.close()

    # method to prepare test dataset
    def prepareTestSet(self, test_positive_index_list, test_negative_index_list):
        print "preparing test set"
        self.generateTestSet(test_positive_index_list, test_negative_index_list)

        self.waitFor("pos_samples")
        shutil.move("pos_samples","Test/")


        self.waitFor("neg_samples")
        shutil.move("neg_samples","Test/")


        self.waitFor("Test/pos_samples")
        self.waitFor("Test/neg_samples")
        self.merge_files(["Test/pos_samples","Test/neg_samples"],"Test/test_set")

        self.prepareLabeledTest()

    def generateDatasets(self, train_set_size, test_set_size):
        train_set_size=int(train_set_size)/2
        test_set_size=int(test_set_size)/2
        os.system("rm -rf Train")
        os.system("rm -rf Test")
        
        os.system("mkdir Train")
        os.system("mkdir Test")

        print "os is at:",os.getcwd()


        train_positive_index_list = self.generateIndices(self.max_positive, train_set_size)
        train_negative_index_list = self.generateIndices(self.max_negative, train_set_size)

        test_positive_index_list = self.generateIndices(self.max_positive, test_set_size)
        test_negative_index_list = self.generateIndices(self.max_negative, test_set_size)

        self.prepareTrainSet(train_positive_index_list, train_negative_index_list)
        self.prepareTestSet(test_positive_index_list, test_negative_index_list)

