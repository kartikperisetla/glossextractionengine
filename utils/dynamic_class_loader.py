__author__ = 'kartik'

import importlib

# class that dynamically loads a class at runtime
class DynamicClassLoader:
    def __init__(self):
        print "DynamicClassLoader:init"
        pass

    # method that takes class name whose class is to be loaded
    # param: fullClassName- includes package and module name as well
    def load(self, fullClassName):
        _collection = fullClassName.split(".")
        if len(_collection)==3:
            pkg_mod_name = '.'.join(_collection[0:2])   # combining package and module name

        if len(_collection)==2:
            pkg_mod_name = '.'.join(_collection[0:1])   # taking only module name

        module = importlib.import_module(pkg_mod_name)
        _class_placeholder = getattr(module, _collection[2])
        return _class_placeholder