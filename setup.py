#!/usr/bin/env python
"""
Launchcraft
===========

Launchcraft is a script to automate the installation of common Minecraft mods,
resourcepacks, and shaderpacks. It also handles the installation of Forge and
Forge-related mods. It's main focus is in reducing the amount of time it takes
to prepare and install all of the related components for Minecraft mods.

:copyright: (c) 2014-2015 by Nikita Pekin.
:license: GPL-3.0, see LICENSE for more details.
"""
from setuptools import setup, find_packages

dev_requires = [
    'flake8>=2.4,<2.5',
]

tests_require = [
    'pytest-cov>=1.4',
    'pytest-timeout',
    'python-coveralls',
]


install_requires = [
    'clint>=0.4,<0.5',
    'PyInstaller>=2.1,<2.2',
    'requests>=2.6,<2.7',
]

setup(
    name='launchcraft',
    version='1.1.0',
    description='A script to automate the installation of common Minecraft mods',
    url='https://github.com/indiv0/launchcraft',
    author='Nikita Pekin',
    author_email='contact@nikitapek.in',
    license='GPL-3.0',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    zip_safe=False,
    install_requires=install_requires,
    extras_require={
        'tests': tests_require,
        'dev': dev_requires,
    },
)
