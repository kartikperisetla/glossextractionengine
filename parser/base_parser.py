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
    # module_name: name of the module where filter class is present
    # filter_class: name of the filter class
    # sentence: sentence on which to apply given filter
    # returns the boolean response whether given sentence satisfies given filter rules
    def apply_filter(self, module_name, filter_class, sentence, min_length):
        if not self.filter_collection is None:
            key = module_name+":"+filter_class
            # look if requested filter is present in filter collection provided by StartupContext
            if self.filter_collection.has_key(key):
                 # lookup filter instance
                _filter_instance = self.filter_collection[key]
                # return the filter response for given sentence
                return _filter_instance.filter(sentence)




