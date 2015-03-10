#!/usr/bin/python
__author__ = 'kartik'

prefix = "0000"

for i in range(10):
    _cmd = "hadoop fs -get /user/bkisiel/sentences-nodocids/clueweb09-noextra-new-gz/part-m-"+prefix+str(i)+".gz ."
    print _cmd

prefix ="000"
for i in range(10,100 ):
    _cmd = "hadoop fs -get /user/bkisiel/sentences-nodocids/clueweb09-noextra-new-gz/part-m-"+prefix+str(i)+".gz ."
    print _cmd

prefix ="00"
for i in range(10,640 ):
    _cmd = "hadoop fs -get /user/bkisiel/sentences-nodocids/clueweb09-noextra-new-gz/part-m-"+prefix+str(i)+".gz ."
    print _cmd