FROM ubuntu:22.04

ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y \
    git \
    make \
    autotools-dev \
    autoconf \
    libtool \
    g++ \
    ant \
    gperf \
    openjdk-8-jdk \
    freeglut3-dev \
    libxi-dev \
    libxml2-utils \
    libxmu-dev

# PLEXIL
ENV PLEXIL_HOME=/plexil
RUN git clone https://github.com/plexil-group/plexil.git plexil --branch releases/plexil-6
WORKDIR /plexil
RUN make ipc
RUN make tools -j


# PLEXIL5
RUN apt-get install -y curl unzip libgmp-dev libz-dev

ENV BOOTSTRAP_HASKELL_NONINTERACTIVE=true
ENV BOOTSTRAP_HASKELL_GHC_VERSION=9.6.7
ENV BOOTSTRAP_HASKELL_INSTALL_NO_STACK=true
RUN curl --proto '=https' --tlsv1.2 -sSf https://get-ghcup.haskell.org | sh
ENV PATH="/root/.ghcup/bin/:${PATH}"

## Cabal & Python prefetch
RUN apt install -y python3.10-venv
RUN cabal update
RUN mkdir /bootstrap

COPY python /bootstrap/python
WORKDIR /bootstrap/python
RUN python3 -m venv .venv        \
    && . .venv/bin/activate      \
    && pip install --upgrade pip \
    && cd plexilv-cli            \
    && pip install .[dev]

COPY plexilog /bootstrap/plexilog
WORKDIR /bootstrap/plexilog
RUN cabal build --only-dependencies

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