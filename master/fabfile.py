from fabric.api import *
from fabric.contrib.files import exists, append

__author__ = 'asafh'

env.user = 'username'
env.password = 'password'
mesos = 'mesos-0.25.0'
cluster_name = 'test'
mesos_path = '/root/{0}'.format(mesos)
zookeeper_path = mesos_path+'/build/3rdparty/zookeeper-3.4.5'

@parallel
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


def configure_zookeeper(ip_list, server_index):
    print server_index
    ip_list = ip_list.split(" ")
    sudo('rm -rf /tmp/zookeeper')
    run('mkdir -p /tmp/zookeeper')
    append('/tmp/zookeeper/myid', text=server_index)
    sudo('cp {0}/conf/zoo_sample.cfg {0}/conf/zoo.cfg'.format(zookeeper_path))
    for index, ip in enumerate(ip_list, start=1):
        line = "server.{0}={1}:2888:3888".format(index, ip)
        append('{0}/conf/zoo.cfg'.format(zookeeper_path), text=line, use_sudo=True)


def start_zookeeper():
    sudo(zookeeper_path+'/bin/zkServer.sh start')



def run_zookeeper():
    sudo(zookeeper_path+'/bin/zkCli.sh -server 127.0.0.1:2181 -cmd create /mesos mesos')
    sudo(zookeeper_path+'/bin/zkCli.sh -server 127.0.0.1:2181 -cmd ls /')


def start_cluster(ip_list):
    ip_list = ip_list.split(" ")
    zk = ""
    for ip in ip_list:
        zk += ip+":2181,"
    sudo('mkdir -p -m 777 /var/lib/mesos')
    cmd = mesos_path+"/build/bin/mesos-master.sh  --cluster=" +cluster_name \
                    " --ip=0.0.0.0" \
                    " --work_dir=/var/lib/mesos" \
                    " --log_dir=/tmp/mesos_log" \
                    " --zk=zk://{0}/mesos" \
                    " --quorum=2".format(zk)
    command = 'nohup %s </var/log/mesos >/tmp/mesos_master.log 2>&1 &' % cmd
    sudo(command, pty=False)
    print


def install_marthon(ip_list):
    print "installing marthon"
    run('wget -N http://downloads.mesosphere.com/marathon/v0.11.1/marathon-0.11.1.tgz')
    run('tar -zxf marathon-0.11.1.tgz')
    cmd1 = 'export MESOS_NATIVE_JAVA_LIBRARY={}/build/src/.libs/libmesos.so'.format(mesos_path)
    zk = ""
    ip_list = ip_list.split(" ")
    for ip in ip_list:
        zk += ip+":2181,"
    zk = zk[:-1]
    cmd = 'marathon-0.11.1/bin/start --master zk://{0},/mesos --zk zk://{0}/marathon --event_subscriber http_callback'.format(zk)
    cmd2 = 'nohup %s > /var/log/mesos &' % cmd
    sudo(cmd1 + ' ; ' + cmd2)
