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

Windows
-------

In order to be able to use `PyInstaller` on Windows (to package the script as a `.exe`), you must also get `[pywin32](http://sourceforge.net/projects/pywin32)`.

Setup
=====

Linux
-----

Setup the development environment:

    make venv

Windows
-------

Install the dependencies for this script:

    pip install -r requirements

Create a virtualenv:

    virtualenv --python=python.exe venv

Activate the virtualenv:

    venv\Scripts\activate.bat

Copy `cacert.pem` from `venv\Lib\python2.7\site-packages\certifi\cacert.pem` to the application's root directory.


Package
=======

Windows
-------

Execute `pyinstaller` to package the script:

    pyinstaller launchcraft.spec

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

Run the packaged/supplied Launchcraft executable.

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


