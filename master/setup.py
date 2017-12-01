from fabric.tasks import execute
import fabfile as fab
__author__ = 'asafh'

masters_ip_list = []


def update_os_packages():
    execute(fab.prepare, hosts=masters_ip_list)


def configure_mesos():
    execute(fab.install_mesos, hosts=masters_ip_list)


def configure_zookeeper():
    for index, ip in enumerate(masters_ip_list, start=1):
        execute(fab.configure_zookeeper, "{0}".format(" ".join(masters_ip_list)), str(index), host='{0}'.format(ip))
    for ip in masters_ip_list:
        execute(fab.start_zookeeper, host='{0}'.format(ip))
    for ip in masters_ip_list:
        execute(fab.run_zookeeper, host='{0}'.format(ip))


def start_cluster():
    execute(fab.start_cluster, "{0}".format(" ".join(masters_ip_list)), hosts=masters_ip_list)


def install_marathon():
    execute(fab.install_marthon, "{0}".format(" ".join(masters_ip_list)), hosts=masters_ip_list)

def run(servers_list):
    print "setup new mesos Masters"
    global masters_ip_list
    masters_ip_list = servers_list
    update_os_packages()
    configure_mesos()
    configure_zookeeper()
    start_cluster()
    install_marathon()
