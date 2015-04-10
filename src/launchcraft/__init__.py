"""
launchcraft
~~~~~~~~~~~

:copyright: (c) 2014-2015 by Nikita Pekin.
:license: GPL-3.0, see LICENSE for more details.
"""
from __future__ import absolute_import

try:
    VERSION = __import__('pkg_resources') \
        .get_distribution('launchcraft').version
except Exception as e:
    VERSION = 'unknown'


def get_version():
    return VERSION
