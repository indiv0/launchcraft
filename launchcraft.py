import os
import errno
import sys
import shutil

import json

import config
import util


# The home directory will be different on Linux and Windows.
if os.getenv('APPDATA') is not None:
    home = os.getenv('APPDATA')
else:
    home = os.path.expanduser("~")

BASE_DIR = os.getcwd()
MINECRAFT_DIR = os.path.join(home, '.minecraft')
VERSIONS_DIR = os.path.join(MINECRAFT_DIR, 'versions')
JAR_DIR = os.path.join(VERSIONS_DIR, config.VERSION)

if __name__ == '__main__':
    util.installForge()

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
        os.makedirs(PROFILE_DIR)
    except OSError as ex:
        print(ex)
        print('Failed to create new profile directory, exiting...')
        sys.exit(1)

    PROFILE_DIR = os.path.join(VERSIONS_DIR, config.PROFILE_NAME)

    print('Entering newly created profile directory.')
    os.chdir(PROFILE_DIR)

    print('Downloading "{0}.jar" and "{0}.json".'.format(config.VERSION))
    util.downloadFile('https://s3.amazonaws.com/Minecraft.Download/versions/{0}/{0}.jar'.format(config.VERSION), '{}.jar'.format(config.PROFILE_NAME))
    util.downloadFile('https://s3.amazonaws.com/Minecraft.Download/versions/{0}/{0}.json'.format(config.VERSION), '{}.json'.format(config.VERSION))

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
        util.installJar(config.MODS[mod], JAR_FILE)
    util.removeMETAINF(JAR_FILE)

    print('Completed successfully!')
    try:
        input("Press any key to exit...")
    except:
        pass
