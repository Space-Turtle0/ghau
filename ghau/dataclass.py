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
is_folder = True  # Friendly names to use with building whitelists
is_file = False


class Data:
    """A class to store all ghau update data.

    ...
    Attributes
    ----------
    version: str
        current version to compare when checking for updates
    repo: str
        github repo to look for updates in
    reboot: str (optional)
        command to run after update is installed. Used to reboot.
    auth: str (optional)
        authentication token used to increase Github API rate limit
    clean: bool (optional)
        fully clean directory before installation (except files protected by whitelist)
    whitelist: list (optional)
        list of protected files/directories. Each item is a dictionary structured as: {pattern: is_folder}.
        pattern: str
            string to check against files/directories for determining protection.
        is_folder: bool
            bool to determine if it's a folder or a file. True is folder, False is file.
    pre-releases: bool (optional)
        download pre-releases if found
    download: str (optional)
        choose between downloading source code vs uploaded assets (such as executables).
        Valid options: "zip", "asset"
    asset: str (optional)
        asset name to look for when downloading. Used when "download" is set to "asset".
        If no asset name is given, it will download the first asset it comes across.
    ratemin: int (optional)
        minimum amount of rates left before updates stop. Default is 20. 60/hr limit on unauthorized requests.
    debug: bool (optional)
        receive debug messages regarding the update status.
    """
    def __init__(self, version: str, repo: str, pre_releases: bool = False, ratemin: int = 20,
                 clean: bool = False, reboot: str = None, whitelist: list = None, auth: str = None, debug: bool = False,
                 download: str = "zip", asset: str = None):
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
