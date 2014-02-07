launchcraft
===========

A python script to automate the installation of my preferred minecraft setup.

Benefits
========

* Rapid, controlled installation of latest Forge, Minecraft, mods, resourcepacks, shaderpacks
* Written in Python
* Cross-platform ([OS X](http://i.imgur.com/EmUsLrs.gif), Windows, Linux)
* Open-source
* Frequently updead
* Open to input regarding included packs and additional features

Download
========

Get the latest downloads from the [releases](https://github.com/Indiv0/launchcraft/releases) page.

Usage
=====

Preparation
-----------

Install the Minecraft launcher, and run it at least once.

Launchcraft
-----------

Run your Launchcraft executable.

Choose your version:

![](http://i.imgur.com/tuc61jX.gif)

Name your new profile:

![](http://i.imgur.com/BBXF62I.gif)

Choose whether or not you want to install Forge (we'll assume you do):

![](http://i.imgur.com/8KhziRD.gif)

The program will search for the required Forge Client version.
Whether or not it finds it, it will give you the option to (re)install it:

![](http://i.imgur.com/NxZxPTZ.gif)

**Note:** On Linux, the Forge Client installer will download and open automatically.
On Windows and OS X the program will download the jar into the same directory Launchcraft is in, but Launchcraft will exit and you will have to install it manually. After you have installed it manually, run Launchcraft again and repeat the previous steps (but don't install Forge Client again).

The program will then ask you to install mods, and guide ask you which ones you want. It will not allow you to install incompatible or conflicting mods:

![](http://i.imgur.com/bb7d6fm.gif)

**Note:** REI's Minimap does NOT currently work with Forge.

The program will automatically delete the META-INF folder from the newly created jar.

You will now be asked if you want to install texture packs:

![](http://i.imgur.com/CUmooKP.gif)

Then you will be asked to install shaders:

![](http://i.imgur.com/Ywlz6tR.gif)

That's it for the Launchcraft portion!

Completion
----------

Launch Minecraft.

Create a new Minecraft profile.

Change `Use Version:` to `release indiv0`.

If you chose to use Forge, you **MUST** add the following to `JVM Arguments` in your profile:

    -Dfml.ignoreInvalidMinecraftCertificates=true -Dfml.ignorePatchDiscrepancies=true

Save the profile.

Enjoy the game!

Notes
=====

Forge
-----

Uninstalling Forge mods must be done *manually* by deleting the unneeded mods from `.minecraft/mods/`.

Forge mods installed by Launchcraft **will conflict** with mods installed manually. Be sure to remove any conflicting mods.

REI's Minimap
-------------

The latest version of REI's Minimap is **not compatible** with Forge.

Compile
=======
* [Windows](https://github.com/Indiv0/launchcraft/wiki/Windows----Compilation)
* [Linux](https://github.com/Indiv0/launchcraft/wiki/Linux)
* [OS X](https://github.com/Indiv0/launchcraft/wiki/OSX-Compile)

Testimonials
============

* `fucktacular` - /u/franknbrry

* `Dis cool.` - /u/jehtak3
