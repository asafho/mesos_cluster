import os
import json
from master import setup as master
from slave import setup as slave
from argparse import (ArgumentParser,
                      RawTextHelpFormatter)

__author__ = 'asafh'

masters_ip_list = []
slaves_ip_list = []

class ArgParser(ArgumentParser):

    def __init__(self):
        description = 'New mesos master parameters.'
        super(ArgParser, self).__init__(description=description,
                                        formatter_class=RawTextHelpFormatter)
    def parse_args(self):
        self.add_argument('-slaves', '--slaves',
                          action='store_true',
                          dest='slaves',
                          default=False,
                          help='setup mesos slaves')
        self.add_argument('-masters', '--masters',
                          action='store_true',
                          dest='masters',
                          default=False,
                          help='setup mesos masters')
        return super(ArgParser, self).parse_args()


if __name__ == '__main__':
    print "mesos setup"
    args = ArgParser().parse_args()
    args = vars(args)

    with open(os.path.join(os.path.dirname(__file__))+"/mesos.json") as data_file:
        data = json.load(data_file)
    slaves_ip_list = data['slaves']
    masters_ip_list = data['masters']
    print "masters:"
    print masters_ip_list
    print "slaves:"
    print slaves_ip_list

    if args['masters']:
        master.run(masters_ip_list)

    if args['slaves']:
        slave.run(masters_ip_list, slaves_ip_list)


    print "complete"