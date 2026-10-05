FROM ubuntu:22.04

ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y \
    ant \
    autoconf \
    autotools-dev \
    freeglut3-dev \
    g++ \
    git \
    gperf \
    libtool \
    libxi-dev \
    libxml2-utils \
    libxmu-dev \
    make \
    openjdk-8-jdk \
    python3.10-venv \
    unzip

# PLEXIL
ENV PLEXIL_HOME=/plexil
RUN git clone https://github.com/plexil-group/plexil.git plexil --branch releases/plexil-6
WORKDIR /plexil
RUN make ipc
RUN make tools -j

# Python setup
RUN mkdir /bootstrap
COPY python /bootstrap/python
WORKDIR /bootstrap/python
RUN python3 -m venv .venv        \
    && . .venv/bin/activate      \
    && pip install --upgrade pip \
    && cd plexilv-cli            \
    && pip install .[dev]

## Maude
ENV MAUDE_PATH=/MaudeLinux64
ENV PATH="$MAUDE_PATH:${PATH}"
ENV MAUDE_LIB="$MAUDE_PATH"
RUN mkdir -p ${MAUDE_PATH}
WORKDIR ${MAUDE_PATH}
COPY Maude-3.5.1-linux-x86_64.zip Maude.zip
RUN unzip Maude.zip \
    && rm Maude.zip \
    && chmod +x $MAUDE_PATH/maude \
    && ln -s $MAUDE_PATH/maude /usr/local/bin/maude

WORKDIR /