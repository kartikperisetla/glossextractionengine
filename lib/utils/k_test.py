__author__ = 'kartik'

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-a", help="help a params")
args = parser.parse_args()
print args
if args.a == 'magic.name':
    print 'You nailed it!'