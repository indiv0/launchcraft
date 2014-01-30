import os
import sys
import shutil

import zipfile
import requests

import launchcraft

DATA = requests.get('http://nikitapek.in/static/versions.json').json()
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


def installDep(key, jar, query=True):
    # Forge is not installed via the normal dependency method.
    if key is 'forge':
        return

    # If the mod is already installed, no need to install it again.
    if key in INSTALLED_MODS:
        return

    mod = MODS[key]
    name = mod['name']

    # If it is not a dependency and the user does not want the mod, do not install it.
    if query and not query_yes_no("Install {}?".format(name)):
        return

    depends_on_forge = False

    print('Installing {} dependencies.'.format(name))
    for dep in mod['deps']:
        if dep == 'forge':
            depends_on_forge = True
        installDep(dep, jar, False)

        # If the requested mod depends on Forge and Forge is not installed, the installation fails.
        if dep not in INSTALLED_MODS:
            print('Unable to install required dependency "{}"'.format(dep))
            exit()

    if depends_on_forge:
        installForgeMod(key, jar, query)
    else:
        installJar(key, jar, query)


def installJar(key, jar, query=True):
    mod = MODS[key]
    name = mod['name']

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

    INSTALLED_MODS.append(key)


def installForgeMod(key, jar, query=True):
    mod = MODS[key]
    name = mod['name']
    version = mod['version']

    current = os.getcwd()

    os.chdir(launchcraft.MOD_DIR)

    print('Downloading {} version {}'.format(name, version))
    downloadFile(mod['url'], '{}-{}.zip'.format(key, version))

    os.chdir(current)

    INSTALLED_MODS.append(key)


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


def exit():
    try:
        input("Press any key to exit...")
    except:
        pass
