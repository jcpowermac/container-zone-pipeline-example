#!/usr/bin/python

import yaml
import sys
import argparse


def create_jenkins(buildconfig):
    jenkinsfile = """
    node {
        stage('build') {
            openshiftBuild(buildConfig: '%s', showBuildLogs: 'true')
        }
    }
    """ % buildconfig

    bcdict = {
        'apiVersion': 'v1',
        'kind': 'BuildConfig',
        'metadata': {
            'annotations': {},
            'labels': {'name': 'sample-pipeline'},
            'name': 'sample-pipeline'},
        'spec': {
            'strategy': {
                'jenkinsPipelineStrategy': {
                    'jenkinsfile': jenkinsfile,
                    'type': 'JenkinsPipeline'},
                'triggers': [
                    {'github': {'secret': 'secret101'}, 'type': 'GitHub'},
                    {'generic': {'secret': 'secret101'}, 'type': 'Generic'}
                ]
            }
        }
    }

    return bcdict


def load_yaml(filename):
    try:
        if filename is "-":
            stream = sys.stdin
        else:
            stream = open(filename, 'r')

        with stream as f:
            o = yaml.load(f)
    except Exception as e:
        print e.message
        sys.exit(1)

    return o


def create_list(*listitems):

    kubelist = {
        'apiVersion': 'v1',
        'kind': 'List',
        'items': listitems
    }
    return kubelist


def modify_existing_bc(exregbc, args):
    exregbc['metadata']['labels']['build'] = args.buildconfig
    exregbc['metadata']['name'] = args.buildconfig

    output_spec = {
        'to': {
            'kind': 'DockerImage',
            'name': args.docker
        },
        'pushSecret': {
            'name': args.pushsecret
        }
    }
    exregbc['spec']['triggers'] = {}
    exregbc['spec']['output'] = output_spec
    return exregbc


def create_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', dest='filename', required=True)
    parser.add_argument('-b', '--buildconfig', dest='buildconfig', required=True)
    parser.add_argument('-d', '--docker', dest='docker', required=True)
    parser.add_argument('-p', '--pushsecret', dest='pushsecret', required=True)
    return parser.parse_args()


def main():

    try:
        args = create_cli_args()
        exregbc = load_yaml(args.filename)

        buildconfig = modify_existing_bc(exregbc, args)
        jenkinsbc = create_jenkins(args.buildconfig)

        kubelist = create_list(jenkinsbc, buildconfig)

        print yaml.dump(kubelist, default_flow_style=False)
    except Exception as e:
        print e.message


if __name__ == '__main__':
    main()
