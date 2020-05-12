Introduction
============

ghau is a python library aimed to provide easy automatic updates utilizing Github Releases.
Its goal is to make adding update capabilities to programs you release much, much easier.

This package is currently in development, so its API may change drastically with each update.
If you have any suggestions, questions, or bug reports. Please open an issue at <https://github.com/InValidFire/ghau/issues>

Tutorial
--------

First create an instance of the Data class::

	import ghau
	
	VERSION = "v0.0.1"
	REPO = "InValidFire/ghau"
	update = ghau.Update(version=VERSION, repo=REPO)

Then to check for updates and install if necessary, simply do the following::

	update.update()
	

Configuration
-------------
The :class:`~ghau.Update` class has a lot of configuration options to tailor the update process for your needs.
Examples of how each option is configured can be seen here:

Downloading pre-releases::

	import ghau
	
	VERSION = "v0.0.1"
	REPO = "InValidFire/ghau"
	update = ghau.Update(version=VERSION, repo=REPO, pre-releases=True)
	update.update()
	
Cleaning installation directory w/ whitelist::

	import ghau
	
	VERSION = "v0.0.1"
	REPO = "InValidFire/ghau"
	
	#when cleaning is enabled it will install updates to a fresh directory.
	update = ghau.Update(version=VERSION, repo=REPO, clean=True)
	
	# these methods will add the specified files/folders to the whitelist
	# whitelisted files are protected from deletion during cleaning.
	update.wl_folder("data/", "tests/")
	update.wl_file("README.md")
	
	update.update()

Downloading Assets::

	import ghau
	
	VERSION = "v0.0.1"
	REPO = "InValidFire/ghau"
	
	#not setting the asset will tell ghau to download the first asset it comes across.
	ASSET = "program.exe"
	
	update = ghau.Update(version=VERSION, repo=REPO, download="asset", asset=ASSET)
	update.update()
	
Rebooting after updates::

	import ghau
	
	VERSION = "v0.0.1"
	REPO = "InValidFire/ghau"
	
	# rebooting to a python script
	REBOOT = ghau.python("main.py")
	
	#rebooting to an executable
	REBOOT = ghau.exe("program.exe")
	
	#rebooting using some other command
	REBOOT = ghau.cmd("some other command")
	
	update = ghau.Update(version=VERSION, repo=REPO, reboot=REBOOT)
	update.update()

Authenticating w/ Github API::

	import os
	import ghau
	VERSION = "v0.0.1"
	REPO = "InValidFire/ghau"
	
	# we store our tokens in an environmental variable in this example.
	# this protects it from being compromized, keep your tokens secure.
	TOKEN = os.environ['GAPI']
	
	update = ghau.Update(version=VERSION, repo=REPO, auth=TOKEN)
	update.update()

Update Loops
------------
Something that can happen if the programmer doesn't keep the version parameter
in :class:`ghau.Update` consistent with the release version on Github is an Update Loop.

For example, you release an update "v1.1.0" on Github Releases, but you have "v1.0.0" given to
the Update class for that release. This will cause ghau to constantly install updates as it
wants the two numbers to match.

These update loops can be prevented in two ways:

1. Ensure before you release an update that the two numbers will match.
2. Using :func:`ghau.python`, :func:`ghau.exe`, or :func:`ghau.cmd` to build the reboot command you use.

These functions will add a parameter that ghau will detect on the next boot, telling it to stop
the update process.

Whitelisting
------------
If you choose to clean a directory before installing an update, you have the option to protect 
certain files or directories through a whitelist. Every instance of the :class:`ghau.Update` class 
has a whitelist and may be added to it using methods :meth:`ghau.Update.wl_folder`, 
and :meth:`ghau.Update.wl_file`::

	import ghau
	
	update = ghau.Update(version="v0.0.1", repo="InValidFire/ghau", clean=True)
	update.wl_file("data.csv")
	update.wl_folder("data/")
	update.update()

Licensing
---------
ghau is distributed under the MIT License.