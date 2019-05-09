# Execution environment with gRPC
FROM ubuntu:18.04

ENV GRPC_VERSION v1.20.0

LABEL maintainer="obokaiwele <https://github.com/obokaiwele>"

RUN apt-get update && \
    apt-get upgrade -y && \
    # Install development tools
    apt-get install -y \
      autoconf \
      automake \
      build-essential \
      curl \
      gcc \
      git \
      libgflags-dev \
      libtool \
      make \
      net-tools \
      pkg-config \
      unzip \
      vim && \
    # Install gRPC from source
    cd / && \
      git clone --recursive -b $GRPC_VERSION https://github.com/grpc/grpc && \
      cd grpc/third_party/protobuf && \
      ./autogen.sh && \
      ./configure && \
      make && \
      make check && \
      make install && \
      ldconfig && \
      cd ../../ && \
        make && \
        make install && \
    # Install gRPC CLI
    cd /grpc && \
      git submodule update --init && \
      make grpc_cli && \
      ln -s /grpc/bins/opt/grpc_cli /bin/grpc_cli
