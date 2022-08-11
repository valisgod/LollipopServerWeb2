FROM python:3.6.8-slim
ARG port

MAINTAINER val

USER root
COPY . /LollipopServerWeb2
WORKDIR /LollipopServerWeb2

# install base tools 
RUN rm /bin/sh && ln -s /bin/bash /bin/sh \
    && apt update \
    && apt install -y wget \
    && apt install -y curl
#&& apt install -y git \
#&& apt install -y sudo \
#&& curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash \
#&& apt install -y git-lfs \
#&& git lfs install


## manually download submodule since heroku doesn't handle it well
#RUN chgrp -R 0 /LollipopServerWeb2 \
#    && chmod -R g=u /LollipopServerWeb2 \
#    && rm -r AlgContract \
#    && apt -y install openssh-client \
#    && mkdir -p /root/.ssh \
#    && ssh-keygen -q -t rsa -N '' -f /root/.ssh/id_rsa \
#    && ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts \
#    && git clone -b web2server git@github.com:lollipop-dao/AlgContract.git

# install python dep
RUN pip install pip --upgrade \
    && pip install requests==2.22.0 \
    && pip install numpy==1.18.5 \
    && pip install tensorflow==2.2.0 \
    && pip install protobuf==3.11.2 \
    && pip install sklearn==0.0 \
    && pip install jieba==0.42.1 \
    && pip install json-rpc==1.13.0 \
    && pip install schedule==1.1.0 \
    && pip install pandas==0.22 \
    && pip install SQLAlchemy==1.3.18 \
    && pip install PyMySQL==0.9.3

EXPOSE $PORT
#CMD python -m http.server $PORT 
CMD ./heroku_run.sh $PORT
