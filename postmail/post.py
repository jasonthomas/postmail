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


raw_email = sys.stdin.read()

if config.save_email == True:
    save_email(raw_email)

#email = {'body': raw_email}
email = {'bod1y': raw_email}

try:
    r = requests.post(config.end_point, data=email)

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
    save_email(raw_email)
    sys.exit(78)
