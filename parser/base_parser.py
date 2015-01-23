__author__ = 'kartik'

from abc import ABCMeta, abstractmethod
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
    def save_definitions(self, buffer):
        self.def_file_object = open(self.def_file_name, "a")
        self.def_file_object.write(buffer.encode('utf-8'))
        self.def_file_object.close()


    # method to save the buffer content to non definitions
    def save_non_definitions(self, buffer):
        self.non_def_file_object = open(self.non_def_file_name, "a")
        self.non_def_file_object.write(buffer.encode('utf-8'))
        self.non_def_file_object.close()



