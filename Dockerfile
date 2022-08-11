FROM ubuntu:18.04

MAINTAINER val

# install base tools 
RUN rm /bin/sh && ln -s /bin/bash /bin/sh \
    && apt-get update \
    && apt-get install -y wget \
    && apt-get install -y curl

# install python env
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh
ENV PATH="${PATH}:/root/miniconda3/bin/"
RUN conda --version \
    && conda create -y --name python36 python=3.6.8 \
    && source activate \
    && conda deactivate \
    && conda activate python36 \
    && pip3 install requests==2.22.0 \
    && pip3 install numpy==1.18.5 \
    && pip3 install tensorflow==2.2.0 \
    && pip3 install sklearn==0.0 \
    && pip3 install jieba==0.42.1 \
    && pip3 install json-rpc==1.13.0 \
    && pip3 install schedule==1.1.0 \
    && pip3 install pandas==0.22
