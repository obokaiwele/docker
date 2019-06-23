import ruamel.yaml
import requests
import argparse
import logging
import sys
import subprocess
import json

logging.basicConfig(level=logging.DEBUG, format='%(asctime)-15s %(relativeCreated)7d %(threadName)s %(processName)-10s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

yaml = ruamel.yaml.YAML(typ='rt')


def load(path):
    """Load docker-compose.yml """
    with open(path, 'r') as stream:
        try:
            return yaml.load(stream)
        except ruamel.yaml.YAMLError as error:
            logging.error('Failed to load yml data: ', error)
            return {}

def save(path, data):
    """Save docker-compose.yml"""
    with open(path, 'w') as stream:
        try:
            yaml.dump(data, stream)
        except ruamel.yaml.YAMLError as error:
            logging.error('Failed to save yml data: ', error)


def latest(url='http://grpc.io/release'):
    """Get latest gRPC version"""
    resp = requests.get(url)
    return resp.text.strip()


def releases(url='https://api.github.com/repos/grpc/grpc/releases'):
    """Get Set of all gRPC releases"""
    resp = requests.get(url)
    data = resp.json()
    versions = set([item['tag_name'] for item in data])
    return versions


def set_version(path, version):
    config = load(path)
    config['services']['ubuntu']['environment']['GRPC_VERSION'] = version
    save(path, config)


def build(path):
    command = 'sudo docker-compose up --build'
    subprocess.check_call(command, shell=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-V', '--version', help='gRPC verion to build. Defaults to latest version')
    parser.add_argument('-c', '--config', default='docker-compose.yml', help='path to docker-compose.yml file')
    args = parser.parse_args()

    if args.version:
        if args.version not in releases():
            logging.error('{} is not a valid release: '.format(args.version))
            sys.exit(1)
    else:
        args.version = latest()

    # Set version as needed
    set_version(args.config, args.version)

    # Build image
    build(args.config)

 