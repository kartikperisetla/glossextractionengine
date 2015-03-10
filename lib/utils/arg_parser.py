__author__ = 'kartik'

class ArgParser(object):
    def __init__(self):
        self.args = {}

    def parse(self, lst):
        for index, item in enumerate(lst):
            if "-" in item:
                _act_param = item.replace("-","")
                if len(lst)<=index+1:
                    print "ArgParser:Error:No value provided for param: ",_act_param
                    exit()

                self.args[_act_param]= lst[index+1]

    def get_string(self):
        str = ""
        for key,val in self.args.iteritems():
            str = str+" -"+key+" "+val
        return str