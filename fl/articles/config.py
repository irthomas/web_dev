# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 22:24:20 2021

@author: iant

CONFIG
"""

import platform
import sys


if platform.system() == "Linux":

    # DB_PATH = "/var/www/web_dev/fl/data_downloader/obs_overview.db"
    DB_PATH = "/var/www/web_dev/fl/articles/db/articles.db"
    SECRET_KEY_PATH = "/var/www/web_dev/settings"
else:
    # DB_PATH = r"C:\Users\iant\Dropbox\NOMAD\Python\web_dev\djdownloader\downloader\obs_overview.db"
    DB_PATH = r"C:\Users\iant\Dropbox\NOMAD\Python\web_dev\fl\articles\db\articles.db"
    SECRET_KEY_PATH = r"C:\Users\iant\Dropbox\NOMAD\Python\web_dev\settings"

# DEBUG = True

sys.path.append(SECRET_KEY_PATH)
from secret_keys import passwords

