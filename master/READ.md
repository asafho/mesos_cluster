#!bin/sh

#update os packages
sudo apt-get update


#remove all java files
sudo apt-get remove openjdk-6-jre default-jre default-jre-headless

#install java 8
sudo add-apt-repository ppa:openjdk-r/ppa
sudo apt-get install openjdk-8-jdk
sudo update-alternatives --config java
sudo update-alternatives --config javac
java -version


# Install Mesos dependencies.
sudo apt-get install -y autoconf libtool build-essential python-dev python-boto
sudo apt-get install -y libcurl4-nss-dev libsasl2-dev maven libapr1-dev libsvn-dev libz-dev


#download and install mesos
mesos=mesos-0.25.0
cd ~
wget http://www.apache.org/dist/mesos/0.25.0/$mesos.tar.gz
tar -zxf $mesos.tar.gz
cd $mesos
mkdir build
cd build
../configure

#In order to speed up the build and reduce verbosity of the logs,
# you can append -j <number of cores> V=0 to make
make -j 2 V=0
# Run test suite. make check
# Install (Optional). #make -j 2 V=0 install

# Run ZooKeeper
# http://mesos.apache.org/documentation/latest/high-availability/
cd ~/$mesos/build/3rdparty/zookeeper-3.4.5
cp conf/zoo_sample.cfg conf/zoo.cfg
#append master servers to config file
echo server.1=10.0.40.55:2888:3888 >> conf/zoo.cfg
echo server.2=10.0.40.218:2888:3888 >> conf/zoo.cfg
echo server.3=10.0.40.160:2888:3888 >> conf/zoo.cfg

#configure ID for each master
mkdir -p /tmp/zookeeper
id=1 #increment index for each master
echo id >> /tmp/zookeeper/myid

# start Zookeeper
bin/zkServer.sh start

# login to Zookeeper
cd ~/$mesos/build/3rdparty/zookeeper-3.4.5
bin/zkCli.sh -server 127.0.0.1:2181