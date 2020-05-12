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

Licensing
---------
ghau is distributed under the MIT License.