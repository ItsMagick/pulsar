    FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get install -y --no-install-recommends \
    autoconf \
    automake \
    build-essential \
    ca-certificates \
    git \
    graphviz \
    libarchive-dev \
    libconfig-dev \
    libgraphviz-dev \
    libnet1 \
    libnet1-dev \
    libnids-dev \
    libnids1.21 \
    libpcap-dev \
    libpcap0.8 \
    libtool \
    libz-dev \
    python3 \
    python3-dev \
    python3-graphviz \
    python3-levenshtein \
    python3-numpy \
    python3-pip \
    python3-progressbar \
    r-base \
    wireshark

RUN useradd -ms /bin/bash pulsar
ENV PATH=/home/pulsar/.local/bin:$PATH
USER pulsar

RUN cd /home/pulsar && git clone --depth=1 https://github.com/rieck/derrick
RUN cd /home/pulsar && git clone --depth=1 https://github.com/rieck/sally

RUN cd /home/pulsar/derrick && \
    ./bootstrap && \
    ./configure && \
    make && \
    make check

RUN cd /home/pulsar/sally && \
    ./bootstrap && \
    ./configure && \
    make && \
    make check

USER root
RUN cd /home/pulsar/derrick && make install
RUN cd /home/pulsar/sally && make install

USER pulsar
RUN mkdir -p /home/pulsar/R/x86_64-pc-linux-gnu-library/3.6
RUN R -e 'install.packages("PRISMA",lib="/home/pulsar/R/x86_64-pc-linux-gnu-library/3.6")'
# RUN cd /home/pulsar && git clone --depth=1 https://github.com/tammok/PRISMA.git pulsar/modules/PRISMA
# RUN cd /home/pulsar && git clone --depth=1 https://github.com/hgascon/pulsar.git
# RUN cd /home/pulsar/pulsar && python3 pulsar.py --help

WORKDIR /pwd
