"""
launchcraft.constants
~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2014-2015 by Nikita Pekin.
:license: GPL-3.0, see LICENSE for more details.
"""
from __future__ import absolute_import

import pkg_resources
import os
import sys

# The home directory will be different on Linux and Windows.
if sys.platform == 'win32' or sys.platform == 'cygwin':
    MINECRAFT_DIR = os.path.join(os.getenv('APPDATA'), '.minecraft')
elif sys.platform == 'darwin':
    MINECRAFT_DIR = os.path.join(os.path.expanduser("~"), 'Library', 'Application Support', 'minecraft')
else:
    MINECRAFT_DIR = os.path.join(os.path.expanduser("~"), '.minecraft')

# Fix certifi dependency.
CERT_PATH = pkg_resources.resource_filename('launchcraft', 'data/cacert.pem')

BASE_DIR = os.getcwd()
VERSIONS_DIR = os.path.join(MINECRAFT_DIR, 'versions')
MOD_DIR = os.path.join(MINECRAFT_DIR, 'mods')
RESOURCEPACK_DIR = os.path.join(MINECRAFT_DIR, 'resourcepacks')
SHADERPACK_DIR = os.path.join(MINECRAFT_DIR, 'shaderpacks')
