#  Copyright (c) 2020.  InValidFire
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

import datetime

from github import Github
from wcmatch import wcmatch

import ghau.files as files


class GhauError(Exception):
    """Base Exception class"""
    pass


class GitRepositoryFoundError(GhauError):
    """Raised when a git repository is detected."""
    def __init__(self):
        self.message = "Git Repository detected, aborting update process to protect file structure."


class GitHubRateLimitError(GhauError):
    """Raised when exceeding GitHub's API rate."""
    def __init__(self, resettime):
        self.message = ("Current Github API rate limit reached. Cannot check for updates at this time.\n" 
                        "Scheduled to reset on " +
                        datetime.datetime.fromtimestamp(resettime).strftime('%B %d at %H:%M:%S'))


class ReleaseNotFoundError(GhauError):
    """Raised when there are no releases found for the requested repository."""
    def __init__(self, repo: str):
        self.message = ("No releases found for repository {}, aborting.".format(repo))


class ReleaseAssetError(GhauError):
    """Raised when there is no asset found in the release by the requested name"""
    def __init__(self, release, asset_name):
        self.message = ("No asset '{}' found for release {}, aborting".format(asset_name, release))


class RepositoryNotFoundError(GhauError):
    """Raised when Github request returns a 404"""
    def __init__(self, repo: str):
        self.message = ("The repository {} could not be found, aborting.".format(repo))


class NoAssetsFoundError(GhauError):
    """Raised when an asset request returns no asset list"""
    def __init__(self, release):
        self.message = ("No assets found for release {}".format(release))


class InvalidDownloadTypeError(GhauError):
    """Raised when the download parameter value is not expected."""
    def __init__(self, download):
        self.message = ("'download' parameter value '{}' is not expected.".format(download))


class FileNotExeError(GhauError):
    """Raised when the file given is not an executable."""
    def __init__(self, file: str):
        self.message = ("The file '{}' is not an .exe".format(file))


class FileNotScriptError(GhauError):
    """Raised when the file given is not a python script."""
    def __init__(self, file: str):
        self.message = ("The file '{}' is not a python script.".format(file))


class LoopPreventionError(GhauError):
    """Raised when rebooting after an update, to prevent potential loops if user doesn't bump version number."""
    def __init__(self):
        self.message = "Booting after update install, skipping update check."


def devtest():  # TODO Improve dev environment detection
    """Tests for an active dev environment"""
    pl = wcmatch.WcMatch(".", ".git/*", "", flags=wcmatch.RECURSIVE | wcmatch.DIRPATHNAME | wcmatch.FILEPATHNAME |
                         wcmatch.HIDDEN).match()
    if len(pl) > 0:
        raise GitRepositoryFoundError


def ratetest(ratemin: int, token=None):
    """Tests available Github API rate"""
    g = Github(token)
    rl = g.get_rate_limit()
    if rl.core.remaining <= ratemin:
        raise GitHubRateLimitError(rl.core.reset.timestamp())
    else:
        files.message("API requests remaining: " + str(rl.core.remaining))


def argtest(args: list, arg: str):
    if arg in args:
        raise LoopPreventionError
