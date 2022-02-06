# Import an official image of Ubuntu
FROM ubuntu:20.04

# Updating and installing essential stuff
RUN apt-get update
RUN apt-get -y install wget
RUN apt-get -y install python
RUN apt-get -y install git
RUN apt-get -y install build-essential
RUN apt-get -y install nano
RUN apt-get -y install pip
RUN pip3 install pandas

# Installing kraken2
WORKDIR /root/
RUN git clone https://github.com/DerrickWood/kraken2.git
WORKDIR /root/kraken2
RUN ./install_kraken2.sh .
RUN cp /root/kraken2/kraken2 /usr/bin/
RUN cp /root/kraken2/kraken2-build /usr/bin/
RUN cp /root/kraken2/kraken2-inspect /usr/bin/

# Download kraken2 databases
RUN wget ftp://ftp.ccb.jhu.edu/pub/data/kraken2_dbs/16S_Silva138_20200326.tgz
RUN wget ftp://ftp.ccb.jhu.edu/pub/data/kraken2_dbs/16S_RDP11.5_20200326.tgz
RUN wget ftp://ftp.ccb.jhu.edu/pub/data/kraken2_dbs/16S_Greengenes13.5_20200326.tgz
RUN wget -q ftp://ftp.ccb.jhu.edu/pub/data/kraken2_dbs/old/minikraken2_v1_8GB_201904.tgz
RUN tar -xzvf 16S_Silva138_20200326.tgz
RUN tar -xzvf 16S_RDP11.5_20200326.tgz
RUN tar -xzvf 16S_Greengenes13.5_20200326.tgz
RUN tar -xzvf minikraken2_v1_8GB_201904.tgz
RUN rm 16S_Greengenes13.5_20200326.tgz 
RUN rm 16S_RDP11.5_20200326.tgz
RUN rm 16S_Silva138_20200326.tgz
RUN rm minikraken2_v1_8GB_201904.tgz

# Setup env
WORKDIR /root/
ADD run_classifier.py /usr/bin/
ADD test.tar.gz /root