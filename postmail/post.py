#!/bin/env python

import sys
import requests
import hashlib
from postmail import config, configure

configure()

def get_hash(content):
    return hashlib.md5(content).hexdigest()


def save_email(content):
    email_file = '%s/%s' % (config.save_path, get_hash(content))
    with open(email_file, 'w') as fp:
        fp.write(content)


content = sys.stdin.read()

if config.save_email:
    save_email(content)

email = {'body': content}

r = requests.post(config.end_point, data=email)
print r.text
print r.headers
print  (r.status_code == requests.codes.ok)
