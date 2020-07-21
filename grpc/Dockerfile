# Execution environment with gRPC
FROM alpine:3.12.0

ARG GRPC_VERSION

LABEL maintainer="obokaiwele <https://github.com/obokaiwele>"

RUN apk update \
    # Install build dependecies
    && apk add --no-cache --virtual build-dependecies \
        autoconf \
        automake \
        build-base \
        gflags-dev \
        git \
        libtool \
        linux-headers \
    # Install gRPC from source
    && git clone --recursive -b $GRPC_VERSION https://github.com/grpc/grpc /grpc \
        && cd /grpc/third_party/protobuf \
        && ./autogen.sh \
        && ./configure \
        && make \
        && make check \
        && make install \
        && ldconfig /grpc \
    && cd /grpc \
        && make \
        && make install \
    # Install gRPC CLI
    && git submodule update --init \
        && make grpc_cli \
        && cp /grpc/bins/opt/grpc_cli /usr/local/bin/ \
    # Cleanup build dependecies
    && apk del build-dependecies \
    && rm -rf /grpc
