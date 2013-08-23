#!/bin/env python

import sys
import requests
from postmail import config, configure

configure()
email = sys.stdin.read()
r = requests.post(config.end_point, data=email)
