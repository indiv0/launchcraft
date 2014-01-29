import json
import config
import requests
import os
import shutil
import errno
import sys
import zipfile


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


def downloadFile(url, filename):
    r = requests.get(url, verify=cert_path)
    output = open(filename, 'wb')
    output.write(r.content)


def installJar(mod, jar):
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
    os.remove(jarName)

    os.chdir('..')


def removeMETAINF(jar):
    print('Removing META-INF from {}'.format(jar))

    new_jar = jar + 'new'

    with open(os.devnull, 'w') as devnull, RedirectStdStreams(stdout=devnull, stderr=devnull), zipfile.ZipFile(jar, 'r') as zin, zipfile.ZipFile(new_jar, 'w') as zout:
        for item in zin.infolist():
            buffer = zin.read(item.filename)
            if (item.filename[:8] != 'META-INF'):
                zout.writestr(item, buffer)
    #with zipfile.ZipFile(jar, 'w') as zfile:
    #    zfile.remove('META-INF/')
    #with open(os.devnull, 'w') as devnull:
    #    subprocess.call('zip -d {} META-INF/*'.format(jar), shell=True, stdout=devnull)
    os.remove(jar)
    os.rename(new_jar, jar)

from os.path import expanduser
home = expanduser("~")

BASE_DIR = os.getcwd()
MINECRAFT_DIR = os.path.join(home, '.minecraft')
VERSIONS_DIR = os.path.join(MINECRAFT_DIR, 'versions')
JAR_DIR = os.path.join(VERSIONS_DIR, config.VERSION)

print('Entering directory "{}".'.format(MINECRAFT_DIR))
try:
    os.chdir(MINECRAFT_DIR)
except:
    print('Failed to enter minecraft directory, please install minecraft first.')
    sys.exit(1)

PROFILE_DIR = VERSIONS_DIR + '/{}'.format(config.PROFILE_NAME)

try:
    shutil.rmtree(PROFILE_DIR)
    print('Removed old profile directory.')
except OSError as ex:
    if ex.errno == errno.ENOENT:
        print('No old profile directory found.')
    else:
        print(ex)
        print('Failed to remove old profile directory, exiting...')
        sys.exit(1)

try:
    print('Creating new profile directory.')
    shutil.copytree(JAR_DIR, PROFILE_DIR)
except OSError as ex:
    if ex.errno == errno.ENOENT:
        print('Base profile dir not found. Please download minecraft version {} and run it at least once.'.format(config.VERSION))
        sys.exit(1)
    else:
        print(ex)
        print('Failed to create new profile directory, exiting...')
        sys.exit(1)

PROFILE_DIR = os.path.join(VERSIONS_DIR, config.PROFILE_NAME)

print('Entering newly created profile directory.')
os.chdir(PROFILE_DIR)

print('Downloading "{0}.jar" and "{0}.json".'.format(config.VERSION))
downloadFile('https://s3.amazonaws.com/Minecraft.Download/versions/{0}/{0}.jar'.format(config.VERSION), '{}.jar'.format(config.PROFILE_NAME))
downloadFile('https://s3.amazonaws.com/Minecraft.Download/versions/{0}/{0}.json'.format(config.VERSION), '{}.json'.format(config.VERSION))

print('Renaming jar file.')
#os.rename('{}.jar'.format(config.VERSION), '{}.jar'.format(config.PROFILE_NAME))

JAR_FILE = os.path.join(PROFILE_DIR, '{}.jar'.format(config.PROFILE_NAME))

print('Creating "{}.json".'.format(config.PROFILE_NAME))
with open('{}.json'.format(config.VERSION), "r") as file:
    data = json.load(file)
data['id'] = config.PROFILE_NAME
with open('{}.json'.format(config.PROFILE_NAME), "w") as file:
    json.dump(data, file, indent=4)

print('Deleting "{}.json".'.format(config.VERSION))
os.remove('{}.json'.format(config.VERSION))

print('Installing mods.')
for mod in config.MODS:
    installJar(config.MODS[mod], JAR_FILE)
removeMETAINF(JAR_FILE)

print('Completed successfully!')
