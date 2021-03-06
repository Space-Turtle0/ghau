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
- **Automatic Reboots**: Optionally automatically reboot into the newer program after update installation. Supports rebooting into a python script, executable, or a custom run command!
- **Authentication**: Authenticate with the Github API to recieve a larger rate limit and access to your private repositories.
  - Do not store your API token in a public location. Use environmental variables.
- **Download assets or source code**: Choose between downloading the source code or an uploaded asset!
## State of Package
Before you go any further I would like to leave a notice here regarding the current state of the package.

This package was originally a script I used in other projects, so some behaviour currently may be a bit... odd for your typical package.

The API is going to be unstable at the moment until I get things sorted out. Thanks! <3

See my current To-Do list for the package below:
### To-Do
- Add proper tests (gotta figure out this one)
- Improve on asset and version detection.
- Improve developer environment detection.
- Implement Python's `logging` module.
- Extend Whitelist to protect files during extraction of downloaded zips.
- Cleanup & Code Optimization
## Example
```py
import ghau
#other imports

update = ghau.Update(version="v0.0.1", repo="InValidFire/ghau")
update.update()
# rest of program code
```
## Documentation (WIP)
Read the documentation at [Read The Docs](https://ghau.readthedocs.io/en/latest/index.html)
## Requirements
This script utilizes [PyGithub](https://github.com/PyGithub/PyGithub) for its Github interactions, [wcmatch](https://github.com/facelessuser/wcmatch) for its file filtering, and [requests](https://github.com/psf/requests) for file downloads. All three can be found in the requirements.txt file in this repository.
## Contributing
See something you think you can do better? Perhaps a bug I missed? Or even a new feature implementation? All you have to do is fork this repository, make the edits, then open a pull request explaining the changes you made. Thanks for contributing! <3
