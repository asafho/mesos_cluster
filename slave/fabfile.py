from fabric.api import *
from fabric.contrib.files import exists

__author__ = 'asafh'

env.user = 'username'
env.password = 'password'
mesos = 'mesos-0.25.0'
mesos_path = '/root/{0}'.format(mesos)
zookeeper_path = mesos_path+'/build/3rdparty/zookeeper-3.4.5'

def prepare():
    print "remove old java versions"
    sudo('apt-get remove openjdk-6-jre default-jre default-jre-headless')
    print "update os packages"
    sudo('apt-get update')
    install_java()
    install_packages()


def install_packages():
    packages = 'autoconf libtool build-essential python-dev python-boto libcurl4-nss-dev libsasl2-dev maven libapr1-dev libsvn-dev libz-dev docker.io'
    sudo('apt-get install -y {}'.format(packages))

def install_java():
    sudo('add-apt-repository -y ppa:openjdk-r/ppa')
    sudo('apt-get install -y openjdk-8-jdk')
    sudo('java -version')

@parallel
def install_mesos():
    print "installing mesos"
    if exists(mesos_path):
        sudo('rm -rf {}'.format(mesos_path))
    with cd('/root'):
        sudo('wget -N http://www.apache.org/dist/mesos/0.25.0/{0}.tar.gz'.format(mesos))
        sudo('tar -zxf {}.tar.gz'.format(mesos))
    with cd(mesos_path):
        sudo('mkdir -p build')
        with cd('build'):
            sudo('../configure')
            sudo('make -j 2 V=0')


def add_slave(masters_ip_list):
    zk = ""
    ip_list = masters_ip_list.split(" ")
    for ip in ip_list:
        zk += ip+":2181,"
    sudo('rm -rf /tmp/mesos/meta/slaves/latest')
    cmd = "{0}/build/bin/mesos-slave.sh " \
          "--master=zk://{1}/mesos " \
          "--containerizers=docker,mesos " \
          "--resources='ports:[1-30000]' " \
          "--executor_shutdown_grace_period=60secs --docker_stop_timeout=50secs " \
          "--hostname={2}".format(mesos_path, zk, env.host)
    command = 'nohup %s &> /tmp/mesos_slave.log &' % cmd
    sudo(command)