__author__ = 'kartik'


# class that dynamically loads a class at runtime
class DynamicClassLoader:
    def __init__(self):
        print "DynamicClassLoader:init"
        pass

    # method that takes class name whose class is to be loaded
    # param: fullClassName- includes package and module name as well
    def load(self, fullClassName):
        _collection = fullClassName.split(".")
        fully_qualified_path = '.'.join(_collection[:-1]) # everything except last item
        module_name = _collection[-2:][0]
        class_name = _collection[-1] # last item
        module = __import__(fully_qualified_path,{},{},class_name)
        _class_placeholder = getattr(module, class_name)

        return _class_placeholder