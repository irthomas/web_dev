# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 22:24:20 2021

@author: iant

CONFIG
"""

import platform
import sys


if platform.system() == "Linux":

    DB_PATH = "/var/www/web_dev/fl/pvpower/db/pvpower.db"
    DB_PATH_TUYA = "/var/www/web_dev/fl/pvpower/db/plugs.db"
    SECRET_KEY_PATH = "/var/www/web_dev/settings"
else:
    DB_PATH = r"C:\Users\iant\Documents\PROGRAMS\web_dev\fl\pvpower\db\pvpower.db"
    DB_PATH = r"C:\Users\iant\Documents\PROGRAMS\web_dev\fl\pvpower\db\plugs.db"
    SECRET_KEY_PATH = r"C:\Users\iant\Documents\PROGRAMS\web_dev\settings"

DEBUG = False

sys.path.append(SECRET_KEY_PATH)
from secret_keys import pv_ip_address, TUYA_API

