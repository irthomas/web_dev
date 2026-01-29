# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 22:24:20 2021

@author: iant

CONFIG
"""

import platform
# import sys
import os

if platform.system() == "Linux":
    
    FLASK_PATH = "/var/www/web_dev/fl"
    SECRET_KEY_PATH = "/var/www/web_dev/settings"
else:
    FLASK_PATH = r"C:\Users\iant\Dropbox\NOMAD\Python\web_dev\fl"
    SECRET_KEY_PATH = r"C:\Users\iant\Dropbox\NOMAD\Python\web_dev\settings"

APP_PATH = os.path.join(FLASK_PATH, "uk_elec")
DB_PATH = os.path.join(APP_PATH, "db", "uk_elec.db")

# DEBUG = True

# sys.path.append(SECRET_KEY_PATH)
# from secret_keys import SECRET_KEYS
