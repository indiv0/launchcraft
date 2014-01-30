import os
import sys
import shutil

import zipfile
import requests

import config


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


# Fix certifi dependency.
# Stolen and adpated from <http://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile>
def resource_path(relative):
    return os.path.join(getattr(sys, '_MEIPASS', os.path.abspath(".")), relative)

cert_path = resource_path('cacert.pem')


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


def downloadFile(url, filename):
    r = requests.get(url, verify=cert_path)
    output = open(filename, 'wb')
    output.write(r.content)


def installForge():
    if not query_yes_no('Do you need Forge?', default='no'):
        return

    forge = config.MODS['forge']
    name = forge['name']

    #if not query_yes_no("Install {}?".format(name)):
    #    return

    #tempDir = 'jar_temp'
    jarName = 'forge.jar'

    #if not os.path.exists(tempDir):
    #    os.makedirs(tempDir)

    #os.chdir(tempDir)

    print('Downloading {} version {}'.format(name, forge['version']))
    downloadFile(forge['url'], jarName)

    print('You will now be asked to install the Forge client.')

    #print('Downloading {} version {}'.format(name, mod['version']))
    #downloadFile(mod['url'], jarName)
    #print('Installing {} into the minecraft.jar'.format(name))
    #with open(os.devnull, 'w') as devnull, RedirectStdStreams(stdout=devnull, stderr=devnull), zipfile.ZipFile(jarName, 'r') as zin, zipfile.ZipFile(jar, 'a') as zout:
    #    for n in zin.namelist():
    #        zout.writestr(n, zin.open(n).read())

    #os.chdir('..')
    #shutil.rmtree(tempDir)


def installJar(mod, jar):
    name = mod['name']

    if not query_yes_no("Install {}?".format(name)):
        return


    tempDir = 'jar_temp'
    jarName = 'mod.jar'

    if not os.path.exists(tempDir):
        os.makedirs(tempDir)

    os.chdir(tempDir)

    print('Downloading {} version {}'.format(name, mod['version']))
    downloadFile(mod['url'], jarName)
    print('Installing {} into the minecraft.jar'.format(name))
    with open(os.devnull, 'w') as devnull, RedirectStdStreams(stdout=devnull, stderr=devnull), zipfile.ZipFile(jarName, 'r') as zin, zipfile.ZipFile(jar, 'a') as zout:
        for n in zin.namelist():
            zout.writestr(n, zin.open(n).read())

    os.chdir('..')
    shutil.rmtree(tempDir)


def removeMETAINF(jar):
    print('Removing META-INF from {}'.format(jar))

    new_jar = jar + 'new'

    with open(os.devnull, 'w') as devnull, RedirectStdStreams(stdout=devnull, stderr=devnull), zipfile.ZipFile(jar, 'r') as zin, zipfile.ZipFile(new_jar, 'w') as zout:
        for item in zin.infolist():
            buffer = zin.read(item.filename)
            if (item.filename[:8] != 'META-INF'):
                zout.writestr(item, buffer)
    os.remove(jar)
    os.rename(new_jar, jar)
