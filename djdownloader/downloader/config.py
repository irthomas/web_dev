# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 22:24:20 2021

@author: iant

CONFIG
"""

import platform
import sys


if platform.system() == "Linux":

    DB_PATH = "/var/www/web_dev/djdownloader/downloader/db/levels.db"
    SECRET_KEY_PATH = "/var/www/web_dev/settings"
    SHARED_DIR_PATH = "/var/www/web_dev/shared"
else:
    DB_PATH = r"C:\Users\iant\Documents\PROGRAMS\web_dev\djdownloader\downloader\db\levels.db"
    SECRET_KEY_PATH = r"C:\Users\iant\Documents\PROGRAMS\web_dev\settings"
    SHARED_DIR_PATH = r"C:\Users\iant\Documents\PROGRAMS\web_dev\shared"

# DEBUG = True
DEBUG = False

sys.path.append(SECRET_KEY_PATH)
from secret_keys import SECRET_KEYS, ALLOWED_HOSTS


MAX_FILES = 10000