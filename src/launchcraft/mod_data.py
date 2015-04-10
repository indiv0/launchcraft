"""
launchcraft.mod_data
~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2014-2015 by Nikita Pekin.
:license: GPL-3.0, see LICENSE for more details.
"""
from __future__ import absolute_import

import requests

DATA = requests.get('https://raw.github.com/Indiv0/launchcraft/master/versions.json').json()

# import pkg_resources
# with pkg_resources.resource_stream('launchcraft', 'data/versions.json') as f:
#     import json
#     DATA = json.load(f)


def get_mod_data():
    return DATA
