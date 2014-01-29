import os
import errno
import sys
import shutil
import subprocess

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

FORGE_VERSION = '{}-Forge{}'.format(config.VERSION, config.MODS['forge']['version'])
FORGE_DIR = os.path.join(VERSIONS_DIR, FORGE_VERSION)
MOD_DIR = os.path.join(MINECRAFT_DIR, 'mods')

if __name__ == '__main__':
    print('Entering directory "{}".'.format(MINECRAFT_DIR))
    try:
        os.chdir(MINECRAFT_DIR)
    except:
        print('Failed to enter minecraft directory, please install minecraft first.')
        sys.exit(1)

    # Set the directory to which the custom profile will be installed.
    profile_name = raw_input('What would you like to call this profile? [indiv0]: ').lower()
    if profile_name == '':
        profile_name = 'indiv0'
    PROFILE_DIR = os.path.join(VERSIONS_DIR, profile_name)

    # Delete the old profile directory so we can start from scratch.
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

    # Ask the user whether or not they need Forge.
    if util.query_yes_no('Do you need to (re)install Forge?', default='no'):
        forge = config.MODS['forge']
        name = forge['name']
        version = forge['version']
        jarName = 'forge.jar'

        # Download the Forge installer.
        print('Downloading {} version {}'.format(name, version))
        util.downloadFile(forge['url'], jarName)

        # Run the installer so the user can install Forge.
        print('You will now be asked to install Forge version {}.'.format(version))
        with open(os.devnull, 'w') as devnull:
            subprocess.call('java -jar {}'.format(jarName), shell=True, stdout=devnull)

        os.remove(jarName)

    JAR_FILE = os.path.join(PROFILE_DIR, '{}.jar'.format(profile_name))
    JSON_FILE = os.path.join(PROFILE_DIR, '{}.json'.format(profile_name))

    # If the Forge directory exists, then we consider Forge to be installed, and we use Forge.
    if os.path.exists(FORGE_DIR) and util.query_yes_no('Forge has been found on your system. Would you like to use it?', default='no'):
        if not os.path.exists(MOD_DIR):
            os.makedirs(MOD_DIR)

        util.INSTALLED_MODS.append('forge')
        JAR_DIR = FORGE_DIR
        shutil.copytree(FORGE_DIR, PROFILE_DIR)
        shutil.move(os.path.join(PROFILE_DIR, '{}.jar'.format(FORGE_VERSION)), JAR_FILE)
        SOURCE_JSON_FILE = '{}.json'.format(FORGE_VERSION)

        print('Entering newly created profile directory.')
        os.chdir(PROFILE_DIR)
    else:
        # Create the profile directory.
        try:
            print('Creating new profile directory.')
            os.makedirs(PROFILE_DIR)
        except OSError as ex:
            print(ex)
            print('Failed to create new profile directory, exiting...')
            sys.exit(1)

        print('Entering newly created profile directory.')
        os.chdir(PROFILE_DIR)

        print('Downloading "{0}.jar" and "{0}.json".'.format(config.VERSION))
        util.downloadFile('https://s3.amazonaws.com/Minecraft.Download/versions/{0}/{0}.jar'.format(config.VERSION), '{}.jar'.format(profile_name))
        util.downloadFile('https://s3.amazonaws.com/Minecraft.Download/versions/{0}/{0}.json'.format(config.VERSION), '{}.json'.format(config.VERSION))
        SOURCE_JSON_FILE = '{}.json'.format(config.VERSION)

    print('Creating "{}.json".'.format(profile_name))
    with open('{}'.format(SOURCE_JSON_FILE), "r") as file:
        data = json.load(file)
    data['id'] = profile_name
    with open(JSON_FILE, "w") as file:
        json.dump(data, file, indent=4)

    print('Deleting "{}".'.format(SOURCE_JSON_FILE))
    os.remove(SOURCE_JSON_FILE)

    print('Installing mods.')
    for mod in config.MODS:
        # Do not install forge-dependant mods if Forge is not installed.
        if 'forge' in config.MODS[mod]['deps'] and 'forge' not in util.INSTALLED_MODS:
            continue

        util.installDep(mod, JAR_FILE)

    util.removeMETAINF(JAR_FILE)

    print('Completed successfully!')
    try:
        input("Press any key to exit...")
    except:
        pass
