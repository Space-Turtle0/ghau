# GHAU
Github Auto Update package available to use for all public Github Repositories. 

**Currently in development.**

## Goal
The goal of this repository is to create a flexible package that can easily be implemented into any python project allowing for automatic updates through GitHub Releases. 

Basically I got tired of building update scripts for every program I made.
## Features
- **UPDATE**: Automatically update distributed copies of any public GitHub repository using GitHub Releases.
- **Clean Directory**: Option to install to a clean directory after update.
	- Whitelist files you don't want deleted during this process.
- **Pre-Releases**: Choose to include pre-releases in updates.
- **Developer Mode detection**: If the package detects a .git folder with files inside, it will automatically abort the update process to protect the file structure during development.
- **Automatic Reboots**: Optionally reboot to a file or executable by supplying a command.
## State of Package
Before you go any further I would like to leave a notice here regarding the current state of the package.

This package was originally a script I used in other projects, so some behaviour currently may be a bit... odd for your typical package.

The API is going to be unstable at the moment until I get things sorted out. Thanks! <3

See my current To-Do list for the package below:
### To-Do
- Build proper documentation for user accessible functions
- Upload to PyPi
- Add proper tests (gotta figure out this one)
- Improve on asset and version detection.
- Make more functions open? *thinkin about this*
- Cleanup & Code Optimization
## Example
```py
import ghau
#other imports

data = ghau.Data(version="v0.0.1", repo="InValidFire/ghau")
ghau.checkForUpdates(data)
# rest of program code
```

## Setup Explained
The above example shows an *extremely* simple implementation. 

There are quite a few options available in the ghau.Data class to further configure your update installation should you wish to use them.

| Parameter    | Description                                                                                                                                                                                                                                                                                                                                                                         |
|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| version      | The current version number of the program to check against Github Releases. Default is None.                                                                                                                                                                                                                                                                                        |
| repo         | The repository to check for updates against. Default is None.                                                                                                                                                                                                                                                                                                                       |
| pre-releases | Download and install pre-releases. Default is False.                                                                                                                                                                                                                                                                                                                                |
| ratemin      | The minimum amount of rates left before the update process will halt. <br>This is to protect you from going over the Github API limit. Default is 30                                                                                                                                                                                                                                |
| clean        | Clean the working directory before installing the a new update. Default is False.<br><br>Behavior: <br>True - Will delete all files not protected by the whitelist before installing.<br>False - Will overwrite old files with the downloaded files as it is installed.                                                                                                             |
| reboot       | The command you would like to run for rebooting after an update.<br><br>I have added a few functions to make syntax here easier python(), exe(), and cmd().<br>It can also accept normal strings. <br><br>If no value is given it will not reboot, instead just exiting the program.<br>Default is None.                                                                            |
| whitelist    | List containing entries you would like to exclude from the cleaning process.<br><br>Each item should be a dictionary with the following syntax:<br>{"pattern": bool}<br><br>pattern = pattern to search for files/directories to protect.<br>bool = True if looking for folders, False if looking for files.<br>You can also use is_folder, and is_file to make this syntax easier. |
| auth         | Token used to authenticate with the Github API. Useful to increase the rate limit.<br><br>Unauthorized gets 60 requests an hour, while authorized gets 5000 requests an hour.<br><br>Do NOT store your token directly here. Use environmental variables please.                                                                                                                     |
| debug        | Receive debug messages during the update process. Default is False.                                                                                                                                                                                                                                                                                                                 |
| download     | "zip" if downloading source code, "asset" if downloading a binary.<br><br>Default is "zip"                                                                                                                                                                                                                                                                                          |
| asset        | The name of the asset to download. Used only if downloading assets.           
## Functions
The following describes all user facing functions within this package
### checkForUpdates
Checks for updates and installs if one is found using the given data.
```py
checkForUpdates()
```
#### Example
```py
import ghau

data = ghau.Data(version="v0.0.1", repo="InValidFire/ghau")

ghau.checkForUpdates(data)
# continue program
```
### whitelistTest
```py
whitelistTest(whitelist: list)
```
Preload the whitelist using the given list and return what is not protected. Useful when configuring your whitelist.
#### Example
```py
import ghau

whitelist = [{"*/data": ghau.is_folder}]
ghau.whiteliistTest(whitelist)
# continue program
```
## Requirements
This script utilizes [PyGithub](https://github.com/PyGithub/PyGithub) for its Github interactions, [wcmatch](https://github.com/facelessuser/wcmatch) for its file filtering, and [requests](https://github.com/psf/requests) for file downloads. All three can be found in the requirements.txt file in this repository.
## Contributing
See something you think you can do better? Perhaps a bug I missed? Or even a new feature implementation? All you have to do is fork this repository, make the edits, then open a pull request explaining the changes you made. Thanks for contributing! <3