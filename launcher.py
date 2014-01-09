import json
import config
import requests
import getpass
import os
import tempfile
import shutil
import subprocess

from os.path import expanduser
home = expanduser("~")

BASE_DIR = os.getcwd()
MINECRAFT_DIR = '{0}/.minecraft'.format(home)
JAR_DIR = '{0}/versions/{1}'.format(MINECRAFT_DIR, config.VERSION)
LIB_DIR = '{0}/libraries'.format(MINECRAFT_DIR)
ASSETS_DIR = '{0}/assets'.format(MINECRAFT_DIR)


class Launcher:
    classpath = ''
    natives_dir = ''
    temp = ''

    def __init__(self):
        self.setupTempDir()
        self.getDeps()

    def getDeps(self):
        json_file = open('{0}/{1}.json'.format(JAR_DIR, config.VERSION))
        deps = json.load(json_file)
        libraries = deps['libraries']

        natives = 'natives-linux'

        for lib in libraries:
            for lib_name, library in lib.iteritems():
                if lib_name == 'extract':
                    continue
                elif lib_name == 'natives':
                    continue
                elif lib_name == 'rules':
                    continue

                packages = library.split(':')[0]
                name = library.split(':')[-2]

                if name == 'twitch-platform':
                    name = 'twitch'
                elif name == 'twitch-external-platform':
                    continue

                packages = packages.replace('.', '/')
                VERSION = library.split(':')[-1]
                jar_name = '{0}-{1}'.format(name, VERSION)

                if name == 'lwjgl-platform' or name == 'jinput-platform':
                    jar_name = jar_name + '-{0}'.format(natives)

                library = ':{0}/{1}/{2}/{3}/{4}.jar'.format(LIB_DIR, packages, name, VERSION, jar_name)

                self.classpath += library

    def setupTempDir(self):
        print('Setting up temp dir')

        try:
            current = os.getcwd()
            self.temp = tempfile.mkdtemp()
            print("Temp dir: {0}".format(self.temp))
            os.chdir(self.temp)
        except:
            print('Failed to setup temporary directory')
            return

        self.natives_dir = '{0}/natives'.format(self.temp)
        shutil.copy('{0}/{1}.jar'.format(JAR_DIR, config.VERSION), '{0}/{1}.jar'.format(self.temp, config.VERSION))

        self.installOptifine()
        self.installReisMinimap()
        self.removeMETAINF()

        shutil.copytree('{0}/natives'.format(BASE_DIR), '{0}/natives'.format(self.temp))
        self.classpath = '{0}/{1}.jar'.format(self.temp, config.VERSION)

        os.chdir(current)

    def installOptifine(self):
        if not os.path.exists('optifine'):
            os.makedirs('optifine')

        os.chdir('optifine')

        print('Downloading Optifine')
        self.downloadFile(config.OPTIFINE_LINK, 'optifine.jar')
        print('Installing Optifine into the minecraft.jar')
        subprocess.call('jar xf optifine.jar', shell=True)
        os.remove('optifine.jar')
        subprocess.call('zip -rT ../{0}.jar *'.format(config.VERSION), shell=True)

        os.chdir('..')
        shutil.rmtree('optifine')

    def installReisMinimap(self):
        if not os.path.exists('reis'):
            os.makedirs('reis')

        os.chdir('reis')

        print('Downloading Rei\'s Minimap')
        self.downloadFile(config.REIS_MINIMAP_LINK, 'rei.jar')
        print('Installing Rei\'s Minimap into the minecraft.jar')
        subprocess.call('jar xf rei.jar', shell=True)
        os.remove('rei.jar')
        subprocess.call('zip -rT ../{0}.jar *'.format(config.VERSION), shell=True)

        os.chdir('..')
        shutil.rmtree('reis')

    def removeMETAINF(self):
        print('Removing META-INF from minecraft.jar')

        subprocess.call('7z d -tzip {0}.jar META-INF/'.format(config.VERSION), shell=True)

    def getExecutableString(self):
        print('Authenticating...')

        java_args = '-Xms{0} -Xmx{1} -Djava.library.path={2}'.format(config.MIN_RAM, config.MAX_RAM, self.natives_dir)

        password = getpass.getpass()

        resp = self.auth(config.USERNAME, password)

        try:
            cause = resp['cause']
            if cause == u'UserMigratedException':
                resp = self.auth(config.EMAIL, password)
        except:
            pass

        try:
            auth_user = resp['selectedProfile']['name']
            auth_accessToken = resp['accessToken']
            auth_uuid = resp['selectedProfile']['id']
        except KeyError:
            print('Failed!')
            return ''

        executable = '{0} {1} -cp "{2}" {3} --username {4} --version {5} --gameDir {6} --assetsDir {7} --assetsIndex {5} --uuid {8} --accessToken {9} --userProperties {10} --userType mojang'.format(config.JAVA, java_args, self.classpath, config.MINECRAFT_CLASS, auth_user, config.VERSION, MINECRAFT_DIR, ASSETS_DIR, auth_uuid, auth_accessToken, '{}')

        print(executable)

        return executable

    def auth(self, username, password):
        url = 'https://authserver.mojang.com/authenticate'
        payload = {'agent': {'name': 'Minecraft', 'version': 1}, 'username': username, 'password': password}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

        r = requests.post(url, data=json.dumps(payload), headers=headers)
        accountdata = json.loads(r.text)

        return accountdata

    def downloadFile(self, url, filename):
        r = requests.get(url)
        output = open(filename, 'wb')
        output.write(r.content)

    def stop(self):
        shutil.rmtree(self.temp)
