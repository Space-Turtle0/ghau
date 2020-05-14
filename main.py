import ghau
import logging
import sys
import os

#logging junk
logging.basicConfig(level=logging.DEBUG)

update = ghau.Update(version="v0.0.0", repo="InValidFire/UpdateTest")
update.wl_files("README.md", "main.py")
update.wl_test()
