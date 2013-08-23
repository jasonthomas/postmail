import os
from ConfigParser import SafeConfigParser

from . import config


def configure(config_file=None):
    if not config_file:
        config_file = ['/etc/postmail',
                       os.path.expanduser('~/.postmail')]

    conf = SafeConfigParser()
    if conf.read(config_file):
        config.auth_token = conf.get('postmail', 'auth_token')
        config.end_point = conf.get('postmail', 'end_point')
