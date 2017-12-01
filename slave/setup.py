import json
import os
from fabric.tasks import execute
import fabfile as fab

__author__ = 'asafh'

masters_ip_list = []
slaves_ip_list = []

def update_os_packages():
    execute(fab.prepare, hosts=slaves_ip_list)


def configure_mesos():
    execute(fab.install_mesos, hosts=slaves_ip_list)

def add_slave():
    execute(fab.add_slave, "{0}".format(" ".join(masters_ip_list)), hosts=slaves_ip_list)



def run(masters, slaves):
    global masters_ip_list
    global slaves_ip_list
    masters_ip_list = masters
    slaves_ip_list = slaves
    print "setup new mesos SLAVES"
    update_os_packages()
    configure_mesos()
    add_slave()
