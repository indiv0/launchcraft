
import subprocess
import launcher

if __name__ == '__main__':
    minecraft_launcher = launcher.Launcher()
    subprocess.call(minecraft_launcher.getExecutableString(), shell=True)
    minecraft_launcher.stop()
