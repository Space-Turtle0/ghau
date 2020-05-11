#  Copyright (c) 2020.  Elizabeth Housden
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
#  associated documentation files (the "Software"), to deal in the Software without restriction, including
#  without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the
#  following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial
#  portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
#  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
#  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
#  CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
#  OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#
import os
import sys
import subprocess

import ghau.errors as ge
import ghau.files as gf
from github import Github, RateLimitExceededException, UnknownObjectException, GitRelease
is_folder = True  # Friendly names to use with building whitelists
is_file = False


def _find_release_asset(release: GitRelease, asset: str, debug: bool) -> str:  # TODO: asset detection using regex
    """Return the requested asset's download url from the given release.
    If no asset is requested, it will return the first one it comes across."""
    al = release.get_assets()
    if len(al) == 0:  # if there are no assets, abort.
        raise ge.NoAssetsFoundError(release.tag_name)
    if asset is None:  # if no specific asset is requested, download the first it finds.
        return al[0].browser_download_url
    for item in al:  # otherwise, look for the specific asset requested.
        if item.name == asset:
            gf.message("Found asset {} with URL: {}".format(item.name, item.browser_download_url), debug)
            return item.browser_download_url
        raise ge.ReleaseAssetError(release.tag_name, asset)  # no asset found by requested name? abort.


def _update_check(local, online):  # TODO Improve update detection, if it's newer, version number, etc.
    """Compares the given versions, returns True if the values are different."""
    x = True if online != local else False
    return x


def _load_release(repo: str, pre_releases: bool, auth) -> GitRelease:
    """Returns the latest release (or pre_release if enabled) for the loaded repository"""
    g = Github(auth)
    try:
        if g.get_repo(repo).get_releases().totalCount == 0:  # no releases found
            raise ge.ReleaseNotFoundError(repo)
        if pre_releases:
            return g.get_repo(repo).get_releases()[0]
        elif not pre_releases:
            for release in g.get_repo(repo).get_releases():
                if not release.prerelease:
                    return release
                raise(ge.ReleaseNotFoundError(repo))
    except RateLimitExceededException:
        reset_time = g.rate_limiting_resettime
        raise ge.GitHubRateLimitError(reset_time)
    except UnknownObjectException:
        raise ge.RepositoryNotFoundError(repo)


def _run_cmd(command: str):
    """Run the given command and close the python interpreter.
    If no command is given, it will just close."""
    if command is None:  # closes program without reboot if no command is given.
        sys.exit()
    if sys.platform == "win32":  # windows needs special treatment
        data = command.split()
        subprocess.Popen(data)
        sys.exit()
    else:
        subprocess.Popen(command)
        sys.exit()


def python(file: str) -> str:  # used by users to reboot to the given python file in the working directory.
    """Builds the command required to run the given python file if it is in the current working directory.

    Useful for building the command to place in ghau.Data.reboot"""
    if file.endswith(".py"):
        executable = sys.executable
        file_path = os.path.join(os.getcwd(), file)
        return "{} {} -ghau".format(executable, file_path)
    else:
        raise ge.FileNotScriptError(file)


def exe(file: str) -> str:  # added for consistency. Boots file in working directory.
    """Added for consistency with ghau.python.

    This will ensure the file run is an .exe file and run it if it is in the current working directory."""
    if file.endswith(".exe"):
        return "{} -ghau".format(file)
    else:
        raise ge.FileNotExeError(file)


def cmd(command: str) -> str:  # same as exe
    """Added for consistency with ghau.python.

    This will simply return the given string with the loop prevention argument."""
    return "{} -ghau".format(command)


def whitelist_test(whitelist: list):
    """Test the whitelist and output what isn't protected."""
    pl = gf.load_whitelist(whitelist)
    if len(pl) == 0:
        gf.message("Everything is protected by your whitelist", True)
    else:
        gf.message("Whitelist will not protect the following: ", True)
        for path in pl:
            gf.message(path, True)


def whitelist_add(whitelist: list, pattern: str, folder: bool):
    """Programmatically add item to the given whitelist."""
    whitelist.append({pattern, folder})


def whitelist_remove(whitelist: list, pattern: str):
    """Programmatically remove item from the given whitelist."""
    for item in whitelist:
        for key in item:
            if key == pattern:
                whitelist.remove(item)


class Update:
    """Main data class used to determine ghau update behavior.

    :param version: local version to check against online versions.
    :type version: str
    :param repo: github repository to check for updates in. Must be publicly accessible unless you are using a Github Token.
    :type repo: str
    :param pre-releases: accept pre-releases as valid updates, defaults to False.
    :type pre-releases: bool, optional
    :param reboot: command intended to reboot the program after a successful update installs.
    :type reboot: str, optional
    :param clean: clean directory before installing updates, defaults to False.
    :type clean: bool, optional
    :param whitelist: list of file/directory patterns to determine protection from directory cleaning, defaults to None. The list should contain dictionaries with the following structure {pattern: bool}.
        Pattern is the query to determine file protection, and the bool is True if you're refering to a folder, and False if you're referring to a file.
    :type whitelist: list, optional
    :param download: the type of download you wish to use for updates. Either "zip" (source code) or "asset" (uploaded files), defaults to "zip".
    :type download: str, optional
    :param asset: name of asset to download when set to "asset" mode.
    :type asset: str, optional.
    :param auth: authentication token used for accessing the Github API, defaults to None.
    :type auth: str, optional
    :param ratemin: minimum amount of API requests left before updates will stop, defaults to 20. Maximum is 60/hr for unauthorized requests.
    :type ratemin: int, optional.
    :param debug: receive debug messages regarding the update process, defaults to False.
    :type debug: bool, optional.
    """
    def __init__(self, version: str, repo: str, pre_releases: bool = False,
                 reboot: str = None, clean: bool = False, whitelist: list = None, download: str = "zip",
                 asset: str = None, auth: str = None, ratemin: int = 20, debug: bool = False):
        self.auth = auth  # auth token used to increase Github API rate limit
        self.ratemin = ratemin  # minimum amount of rates before updates stop
        self.debug = debug  # debug messages
        self.version = version  # current software version (same as Github Tag)
        self.repo = repo  # repo downloading from
        self.pre_releases = pre_releases  # download pre-releases?
        self.clean = clean  # fully clean directory before install?
        self.whitelist = whitelist  # files protected from deletion when clean is True
        self.reboot = reboot  # command used to reboot after install
        self.download = download  # download type, either 'zip' or 'asset'
        self.asset = asset  # name of asset to download

    def check_for_updates(self):
        try:
            ge.argtest(sys.argv, "-ghau")
            ge.devtest()
            ge.ratetest(self.ratemin, self.auth)
            latest_release = _load_release(self.repo, self.pre_releases, self.auth)
            do_update = _update_check(self.version, latest_release.tag_name)
            if do_update:
                wl = gf.load_whitelist(self.whitelist)
                gf.clean_files(wl, self.clean, self.debug)
                if self.download == "zip":
                    gf.download(latest_release.zipball_url, "update.zip", self.debug)
                    gf.extract_zip("update.zip")
                    gf.message("Updated from {} to {}".format(self.version, latest_release.tag_name), True)
                    _run_cmd(self.reboot)
                    sys.exit()
                if self.download == "asset":
                    asset_link = _find_release_asset(latest_release, self.asset, self.debug)
                    gf.download(asset_link, self.asset, self.debug)
                    gf.message("Updated from {} to {}".format(self.version, latest_release.tag_name), True)
                    _run_cmd(self.reboot)
                    sys.exit()
                else:
                    raise ge.InvalidDownloadTypeError(self.download)
            else:
                gf.message("No update required.", True)
        except (ge.GitHubRateLimitError, ge.GitRepositoryFoundError, ge.ReleaseNotFoundError, ge.ReleaseAssetError,
                ge.FileNotExeError, ge.FileNotScriptError, ge.NoAssetsFoundError, ge.InvalidDownloadTypeError) as e:
            gf.message(e.message, True)
            return
