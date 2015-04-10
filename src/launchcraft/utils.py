"""
launchcraft.utils
~~~~~~~~~~~~~~~~~

:copyright: (c) 2014-2015 by Nikita Pekin.
:license: GPL-3.0, see LICENSE for more details.
"""
from __future__ import absolute_import

import os
import sys
import shutil

import zipfile
import requests
from clint.textui import progress

import launchcraft


# Fix certifi dependency.
# Stolen and adpated from <http://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile>
def resource_path(relative):
    return os.path.join(getattr(sys, '_MEIPASS', os.path.abspath(".")), relative)

cert_path = resource_path('cacert.pem')

INSTALLED_MODS = []
MODS = []


class RedirectStdStreams(object):
    def __init__(self, stdout=None, stderr=None):
        self._stdout = stdout or sys.stdout
        self._stderr = stderr or sys.stderr

    def __enter__(self):
        self.old_stdout, self.old_stderr = sys.stdout, sys.stderr
        self.old_stdout.flush()
        self.old_stderr.flush()
        sys.stdout, sys.stderr = self._stdout, self._stderr

    def __exit__(self, exc_type, exc_value, traceback):
        self._stdout.flush()
        self._stderr.flush()
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr


# Taken from <http://stackoverflow.com/questions/3041986/python-command-line-yes-no-input>
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' (or 'y' or 'n').\n")


def print_ask_options(optionList):
    numberedMods = []
    for index, option in enumerate(x for x in optionList if x != 'forge'):
        print('{} - {}'.format(index + 1, optionList[option]['name']))
        numberedMods.append(option)
    print('---------------')
    print('[1 2 3 etc... {all}]')
    answer = ''
    while not answer:
        answer = raw_input('-->')
        if answer == 'all':
            return numberedMods
        else:
            answer = answer.split()
        if all((x.isdigit() for x in answer)):
            answer = [int(x) for x in answer]
        else:
            answer = ''
    return (mods for mods in numberedMods if numberedMods.index(mods) + 1 in answer)


def download_file(url, filename):
    r = requests.get(url, stream=True, verify=cert_path)
    with open(filename, 'wb') as f:
        total_length = int(r.headers.get('content-length'))
        for chunk in progress.bar(r.iter_content(chunk_size=1024), expected_size=(total_length / 1024) + 1):
            if chunk:
                f.write(chunk)
                f.flush()


def install_dep(key, jar, query=True):
    # Forge is not installed via the normal dependency method.
    if key is 'forge':
        return

    # If the mod is already installed, no need to install it again.
    if key in INSTALLED_MODS:
        return

    mod = MODS['mods'][key]
    name = mod['name']

    depends_on_forge = False

    print('Installing {} dependencies.'.format(name))
    for dep in mod['deps']:
        if dep == 'forge':
            depends_on_forge = True
        install_dep(dep, jar, False)

        # If the requested mod depends on Forge and Forge is not installed, the installation fails.
        if dep not in INSTALLED_MODS:
            print('Unable to install required dependency "{}"'.format(dep))
            exit()

    if depends_on_forge:
        install_forge_mod(key, jar)
    else:
        install_jar(key, jar)


def install_jar(key, jar):
    mod = MODS['mods'][key]
    name = mod['name']

    tempDir = 'jar_temp'
    jarName = 'mod.jar'

    if not os.path.exists(tempDir):
        os.makedirs(tempDir)

    os.chdir(tempDir)

    print('Downloading {} version {}'.format(name, mod['version']))
    download_file(mod['url'], jarName)
    print('Installing {} into the minecraft.jar'.format(name))
    with open(os.devnull, 'w') as devnull, RedirectStdStreams(stdout=devnull, stderr=devnull), zipfile.ZipFile(jarName, 'r') as zin, zipfile.ZipFile(jar, 'a') as zout:
        for n in zin.namelist():
            zout.writestr(n, zin.open(n).read())

    os.chdir('..')
    shutil.rmtree(tempDir)

    INSTALLED_MODS.append(key)


def install_forge_mod(key, jar):
    mod = MODS['mods'][key]
    name = mod['name']
    version = mod['version']
    url = mod['url']

    current = os.getcwd()

    os.chdir(launchcraft.MOD_DIR)

    print('Downloading {} version {}'.format(name, version))
    download_file(url, '{}-{}.{}'.format(key, version, url[-3:]))

    os.chdir(current)

    INSTALLED_MODS.append(key)


def install_resource_pack(key):
    mod = MODS['resourcepacks'][key]
    name = mod['name']
    version = mod['version']
    url = mod['url']

    current = os.getcwd()

    os.chdir(launchcraft.RESOURCEPACK_DIR)

    print('Downloading {} version {}'.format(name, version))
    download_file(url, '{}-{}.{}'.format(key, version, url[-3:]))

    os.chdir(current)


def install_shader_pack(key):
    mod = MODS['shaderpacks'][key]
    name = mod['name']
    version = mod['version']
    url = mod['url']

    current = os.getcwd()

    os.chdir(launchcraft.SHADERPACK_DIR)

    print('Downloading {} version {}'.format(name, version))
    download_file(url, '{}-{}.{}'.format(key, version, url[-3:]))

    os.chdir(current)


def remove_metainf(jar):
    print('Removing META-INF from {}'.format(jar))

    new_jar = jar + 'new'

    with open(os.devnull, 'w') as devnull, RedirectStdStreams(stdout=devnull, stderr=devnull), zipfile.ZipFile(jar, 'r') as zin, zipfile.ZipFile(new_jar, 'w') as zout:
        for item in zin.infolist():
            buffer = zin.read(item.filename)
            if (item.filename[:8] != 'META-INF'):
                zout.writestr(item, buffer)
    os.remove(jar)
    os.rename(new_jar, jar)


def exit(exit=1):
    try:
        input('Press any key to exit...')
    except:
        pass
        sys.exit(exit)


def print_separator():
    print('###############################################################')
