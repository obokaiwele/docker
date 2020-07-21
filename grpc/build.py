#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################################################
# Author: Obe Okaiwele
# Purpose: Build gRPC (https://grpc.io/) as a Docker container
########################################################################################

import ruamel.yaml
import requests
import argparse
import logging
import sys
import subprocess

logging.basicConfig(level=logging.DEBUG, format='%(asctime)-15s %(relativeCreated)7d %(threadName)s %(processName)-10s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
yaml = ruamel.yaml.YAML(typ='rt')


def load(path):
    """Load YAML file"""
    with open(path, 'r') as stream:
        try:
            return yaml.load(stream)
        except ruamel.yaml.YAMLError as error:
            logging.error('Failed to load yml data: ', error)
            return {}

def save(path, data):
    """Save YAML file"""
    with open(path, 'w') as stream:
        try:
            yaml.dump(data, stream)
        except ruamel.yaml.YAMLError as error:
            logging.error('Failed to save yml data: ', error)


def releases(url='https://api.github.com/repos/grpc/grpc/releases'):
    """Get Set of all gRPC releases. Alternatively check http://grpc.io/release for latest release"""
    resp = requests.get(url)
    data = resp.json()
    versions = [item['tag_name'] for item in data]
    return versions


def set_version(path, version):
    config = load(path)
    config['services']['grpc']['build']['args']['GRPC_VERSION'] = version
    save(path, config)


def build():
    command = 'sudo docker-compose -p grpc up --build'
    subprocess.check_call(command, shell=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--grpc', help='gRPC version to build. Defaults to latest version')
    parser.add_argument('-p', '--path', default='docker-compose.yml', help='Path to docker-compose.yml')
    args = parser.parse_args()

    versions = releases()
    if args.grpc:
        if args.grpc not in versions:
            logging.warn('{} is not a recent release: '.format(args.grpc))
            # sys.exit(1)
    else:
        args.grpc = versions[0]

    # Set version as needed
    set_version(args.path, args.grpc)

    # Build image
    build()


if __name__ == '__main__':
    main()
