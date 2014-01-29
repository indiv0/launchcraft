launchcraft
===========

A python script to automate the installation of my preferred minecraft setup.

Prerequisites
=============

* Linux
* zip
* python 2.7
  * virtualenv
  * setuptools

Installation
============

Ensure you have run minecraft at least once and installed version `1.7.2`.

    make venv

Then update `config.py` if required.

Running
=======

Use the following command to create the Minecraft profile:

    make

Launch minecraft, then select the profile `indiv0`.

To-Do
=====

* Make script platform-independent
* Remove dependency on initial Minecraft installation


