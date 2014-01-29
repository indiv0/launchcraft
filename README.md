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

Uninstalling Forge mods must be done *manually* by deleting the unneeded mods from `.minecraft/mods/`.

Shader Mod
----------

If you install SEUS Shaders, you must also use get a shaderpack like [SEUS v10.0 Standard](http://download687.mediafire.com/yoqg3739pj6g/je8gjk8atytbmh5/SEUS+v10.0+Standard.zip) from [here](http://www.minecraftforum.net/topic/1544257-164shaders-mod-v221-updated-by-karyonix/) and place it in `.minecraft/shaderpacks/`, without extracting the `.zip`.

To-Do
=====

* Remove dependency on initial Minecraft installation


