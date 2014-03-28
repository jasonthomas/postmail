#!/bin/env python

import sys
import requests
import hashlib
import base64
import os
from optparse import OptionParser
from ConfigParser import SafeConfigParser


# config file should be ini format
def configure(env, config_file=None):
    if not config_file:
        config_file = ['/etc/postmail',
                       os.path.expanduser('~/.postmail')]
    config = {}
    conf = SafeConfigParser()

    if conf.read(config_file):
        config['auth_token'] = conf.get(env, 'auth_token')
        config['end_point'] = conf.get(env, 'end_point')
        config['save_email'] = conf.getboolean(env, 'save_email')
        config['save_path'] = conf.get(env, 'save_path')
    else:
        print 'No configuration found'

    return config


def get_hash(content):
    return hashlib.md5(content).hexdigest()


def save_email(save_path, content):
    email_file = '%s/%s' % (save_path, get_hash(content))
    with open(email_file, 'w') as fp:
        fp.write(content)


def post_mail(endpoint, save_path, content):

    encode = base64.standard_b64encode(content)
    email = {'body': encode}

    try:
        r = requests.post(endpoint, data=email)

    # if there is a http connection or timeout issue, have postfix try again.
    except requests.ConnectionError as c:
        print 'ConnectionError: %s' % c
        sys.exit(75)
    except requests.Timeout as t:
        print 'Timeout:m %s' % t
        sys.exit(75)

    # if respose code is not equal to 201, print headers to log, bounce.
    if r.status_code != 201:
        print r.text
        print r.headers
        save_email(save_path, content)
        sys.exit(78)


def main(raw_email):
    parser = OptionParser(usage="usage: %prog [options]")
    parser.add_option("-e", "--environment",
                      default='dev',
                      type='string',
                      help="Environment you want to deploy to")

    (options, args) = parser.parse_args()

    config = configure(options.environment)

    if config['save_email']:
        print "yya"
        save_email(config['save_path'], raw_email)

    post_mail(config['end_point'], config['save_path'],  raw_email)

if __name__ == '__main__':
    main(sys.stdin.read())
