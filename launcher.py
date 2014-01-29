import json
import config
import requests
import getpass
import os
import tempfile
import shutil
import errno
import subprocess
import sys

from os.path import expanduser
home = expanduser("~")

BASE_DIR = os.getcwd()
MINECRAFT_DIR = os.path.join(home, '.minecraft')
VERSIONS_DIR = os.path.join(MINECRAFT_DIR, 'versions')
JAR_DIR = os.path.join(VERSIONS_DIR, config.VERSION)

try:
    print('Entering directory "{}"...'.format(MINECRAFT_DIR))
    os.chdir(MINECRAFT_DIR)

    try:
        shutil.rmtree(VERSIONS_DIR + '/indiv0')
        print('Removed old profile directory...')
    except OSError as ex:
        if ex.errno == errno.ENOENT:
            print('No old profile directory found...')
        else:
            print(ex)
            print('Failed to remove old profile directory, exiting...')

    print('Creating new profile directory...')
    shutil.copytree(JAR_DIR, VERSIONS_DIR + '/indiv0')

    PROFILE_DIR = os.path.join(MINECRAFT_DIR, 'indiv0')
except ValueError:
    pass
