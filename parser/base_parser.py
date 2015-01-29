__author__ = 'kartik'

import threading

# Base class for Readers
# Allows concrete implementations to read from various sources of data and generate train and test instances

DEF_TAG = "def"
NON_DEF_TAG = "non-def"
FILE_EXT = ".txt"

class BaseParser(threading.Thread):
    # This should not be overriden by derived class
    # if overriden, make sure to call base class's init
    def __init__(self, *kargs):
        threading.Thread.__init__(self)

        print "\nBaseParser:init"
        self.custom_init(*kargs)

        self.name = type(self).__name__
        self.def_file_name = DEF_TAG +"-"+ self.name + FILE_EXT
        self.non_def_file_name = NON_DEF_TAG +"_"+ self.name + FILE_EXT

        # hold the file objects
        self.def_file_object = open(self.def_file_name, "w")
        self.non_def_file_object = open(self.non_def_file_name,"w")

        # creates new files
        self.close_files()

        # filters for definitional sentences
        self.filters_for_definitions = []
        # transformations for definitional sentences
        self.transformations_for_definitions = []

        # filter for non-definitional sentences
        self.filters_for_non_definitions = []
        # transformations for non-definitional sentences
        self.transformations_for_non_definitions = []


    # method for custom initializer
    def custom_init(self, *kargs):
        # CAN BE OVERRIDEN BY DERIVED CLASS
        pass

    # method to close open files
    def close_files(self):
        self.def_file_object.close()
        self.non_def_file_object.close()

    # method to save the buffer content to definitions
    # params:
    # buffer: raw string buffer to be saved on disk
    def save_definitions(self, buffer):
        if not buffer is None :
            self.def_file_object = open(self.def_file_name, "a")
            self.def_file_object.write(buffer)
            self.def_file_object.close()


    # method to save the buffer content to non definitions
    # params:
    # buffer: raw string buffer to be saved on disk
    def save_non_definitions(self, buffer):
        if not buffer is None :
            self.non_def_file_object = open(self.non_def_file_name, "a")
            self.non_def_file_object.write(buffer)
            self.non_def_file_object.close()

    # method to apply filter
    # params:
    # filter_collection: list of filter object that will be applied on given sentence
    # sentence: sentence on which to apply given filter
    # returns the boolean response whether given sentence satisfies given filter rules
    def apply_filter(self, filter_collection, sentence):
        if not filter_collection is None:
            for _filter_instance in filter_collection:
                response = _filter_instance.filter(sentence)
                if response is False:
                    return False

            # passed all filters
            return True


    # method to apply transformation
    # params:
    # transformation_collection: list of transformation objects that will be applied on given text
    # text: text on which transformation is to be applied
    def apply_transformation(self, transformation_collection, text):
        if not transformation_collection is None:
            for _transformation_instance in transformation_collection:
                text = _transformation_instance.transform(text)

            return text
        else:
            return None



