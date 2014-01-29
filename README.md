launchcraft
===========

A python script to automate the installation of my preferred minecraft setup.

Prerequisites
=============

* pyinstaller
  * upx
* python 2.7
  * virtualenv
  * setuptools

Setup
=====

Install the depenencies for this script with:

    make venv

Package
=======

Windows
-------

Linux
-----

Ensure the working directory is clean:

    make clean

Package the app with `pyinstaller`:

    make

Install
=======

Ensure you have installed the Minecraft launcher.

Windows
-------

Run the packaged/supplied `launchcraft.exe` executable.

Linux
-----

### Script:

Update `config.py` as needed.

Use the following command to create the Minecraft profile:

    make run

### Executable:

Run the packaged/supplied `launchcraft` executable.

Play
====

Launch minecraft.

Select your minecraft profile, enter `Edit Profile`.

Change `Use Version:` to `release indiv0`.

Save the profile.

Enjoy the game!

To-Do
=====

* Make script platform-independent
* Remove dependency on initial Minecraft installation


