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

Instructions
============

Windows [compilation](https://github.com/Indiv0/launchcraft/wiki/Windows----Compilation) and [installation](https://github.com/Indiv0/launchcraft/wiki/Windows---Running) instructions are available in the wiki.

Linux [instructions](https://github.com/Indiv0/launchcraft/wiki/Linux) are also available on the wiki.

Forge
-----

If you choose to use Forge/FML you **MUST** add the following to `JVM Arguments` in your profile after running the script:

    -Dfml.ignoreInvalidMinecraftCertificates=true -Dfml.ignorePatchDiscrepancies=true

To-Do
=====

* Remove dependency on initial Minecraft installation


