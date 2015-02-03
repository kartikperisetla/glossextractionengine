#!/usr/bin/python
__author__ = 'kartik'

import os,sys

class PackageHandler:
    def __init__(self):
        print "PackageHandler:init"
        if os.path.exists("glossextractionengine.mod"):
            os.system("rm -rf glossextractionengine.mod")


    def create_package(self):
        os.chdir("../")
        os.system("tar cf glossextractionengine.mod * --exclude '.*'")
        print "PackageHandler:create_package: package created!"


if __name__=="__main__":
    p = PackageHandler()
    p.create_package()