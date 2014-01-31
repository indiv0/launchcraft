import os
import errno
import shutil
import subprocess

import json

import util


# The home directory will be different on Linux and Windows.
if os.getenv('APPDATA') is not None:
    home = os.getenv('APPDATA')
elif os.name == 'posix':
    home = os.path.join(os.path.expanduser("~"), 'Library', 'Application Support', 'minecraft')
else:
    home = os.path.expanduser("~")

BASE_DIR = os.getcwd()
MINECRAFT_DIR = os.path.join(home, '.minecraft')
VERSIONS_DIR = os.path.join(MINECRAFT_DIR, 'versions')
MOD_DIR = os.path.join(MINECRAFT_DIR, 'mods')

if __name__ == '__main__':
    print('This script will ask you yes or no questions.')
    print('Any answers in square brackets (e.g. [1.7.2]), or that are capitalized (e.g. [Y/n]) are the default answers, and will be selected when you press enter.')
    util.print_separator()

    version = raw_input('Which version of Minecraft would you like to use? [1.7.2]:').lower()
    if version == '':
        version = '1.7.2'

    if version not in util.DATA:
        print("Invalid version selected.")
        util.exit()

    util.MODS = util.DATA[version]

    JAR_DIR = os.path.join(VERSIONS_DIR, version)

    FORGE_VERSION = '{}-Forge{}'.format(version, util.MODS['forge']['version'])
    FORGE_DIR = os.path.join(VERSIONS_DIR, FORGE_VERSION)

    print('Entering directory "{}".'.format(MINECRAFT_DIR))
    try:
        os.chdir(MINECRAFT_DIR)
    except:
        print('Failed to enter minecraft directory, please install minecraft first.')
        util.exit()
    util.print_separator()

    # Set the directory to which the custom profile will be installed.
    profile_name = raw_input('What would you like to call the profile being created? [indiv0]: ').lower()
    if profile_name == '':
        profile_name = 'indiv0'
    PROFILE_DIR = os.path.join(VERSIONS_DIR, profile_name)
    print('Creating profile {}'.format(profile_name))

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
            util.exit()
    util.print_separator()

    forge = util.query_yes_no('Would you like to use Forge?', default='no')
    if forge:
        if os.path.exists(FORGE_DIR):
            print('The required Forge version has been detected on your system.')
            message = 'reinstall'
        else:
            print('The required Forge version has not been detected on your system.')
            message = 'install'
        # Ask the user whether or not they need Forge.
        if util.query_yes_no('Do you need to {} Forge?'.format(message), default='no'):
            forge = util.MODS['forge']
            name = forge['name']
            version = forge['version']
            jarName = 'forge.jar'

            if os.name == 'nt':
                os.chdir(BASE_DIR)

            # Download the Forge installer.
            print('Downloading {} version {}'.format(name, version))
            util.downloadFile(forge['url'], jarName)

            if os.name == 'nt':
                print('You must now run the {} that has been downloaded to your Launchcraft directory.'.format(jarName))
                util.exit()
            else:
                # Run the installer so the user can install Forge.
                print('You will now be asked to install Forge version {}.'.format(version))
                with open(os.devnull, 'w') as devnull:
                    subprocess.call('java -jar {}'.format(jarName), shell=True, stdout=devnull)

                os.remove(jarName)
    util.print_separator()

    JAR_FILE = os.path.join(PROFILE_DIR, '{}.jar'.format(profile_name))
    JSON_FILE = os.path.join(PROFILE_DIR, '{}.json'.format(profile_name))

    if forge:
        print('Using Forge {} as the base for the profile'.format(util.MODS['forge']['version']))
        if not os.path.exists(MOD_DIR):
            os.makedirs(MOD_DIR)

        util.INSTALLED_MODS.append('forge')
        JAR_DIR = FORGE_DIR
        print('Creating new profile directory.')
        shutil.copytree(FORGE_DIR, PROFILE_DIR)
        print('Renaming Forge jar.')
        shutil.move(os.path.join(PROFILE_DIR, '{}.jar'.format(FORGE_VERSION)), JAR_FILE)
        SOURCE_JSON_FILE = '{}.json'.format(FORGE_VERSION)

        print('Entering newly created profile directory.')
        os.chdir(PROFILE_DIR)
    else:
        print('Using Minecraft {} as the base for the profile'.format(version))
        # Create the profile directory.
        try:
            print('Creating new profile directory.')
            os.makedirs(PROFILE_DIR)
        except OSError as ex:
            print(ex)
            print('Failed to create new profile directory, exiting...')
            util.exit()

        print('Entering newly created profile directory.')
        os.chdir(PROFILE_DIR)

        print('Downloading "{0}.jar" and "{0}.json".'.format(version))
        util.downloadFile('https://s3.amazonaws.com/Minecraft.Download/versions/{0}/{0}.jar'.format(version), '{}.jar'.format(profile_name))
        util.downloadFile('https://s3.amazonaws.com/Minecraft.Download/versions/{0}/{0}.json'.format(version), '{}.json'.format(version))
        SOURCE_JSON_FILE = '{}.json'.format(version)

    print('Creating "{}.json".'.format(profile_name))
    with open('{}'.format(SOURCE_JSON_FILE), "r") as file:
        data = json.load(file)
    data['id'] = profile_name
    with open(JSON_FILE, "w") as file:
        json.dump(data, file, indent=4)

    print('Deleting "{}".'.format(SOURCE_JSON_FILE))
    os.remove(SOURCE_JSON_FILE)
    util.print_separator()

    print('Installing mods.')
    print('')
    for mod in util.MODS:
        modData = util.MODS[mod]
        skip = False

        conflicts = [i for i in modData['conflicts'] if i in util.INSTALLED_MODS]

        if mod == 'forge':
            continue

        # Do not install forge-dependant mods if Forge is not installed.
        if 'forge' in modData['deps'] and 'forge' not in util.INSTALLED_MODS:
            print('Skipping {} due to missing Forge'.format(modData['name']))
            skip = True
        # Skip conflicting mods
        elif conflicts:
            conflicting_mods = ""
            for i in conflicts:
                conflicting_mods += util.MODS[i]['name'] + ", "
            print('Skipping {} because it conflicts with {}'.format(modData['name'], conflicting_mods[:-2]))
            skip = True

        if skip:
            print('')
            continue

        util.installDep(mod, JAR_FILE)
        print('')

    util.removeMETAINF(JAR_FILE)
    util.print_separator()

    print('Completed successfully!')
    util.exit()

    try:
        input('Press any key to exit...')
    except:
        pass
