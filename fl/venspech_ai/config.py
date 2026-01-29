# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 11:47:26 2022

@author: iant
"""

import os
import sys
import platform

if platform.system() == "Linux":
    FLASK_PATH = "/var/www/web_dev/fl"
    SECRET_KEY_PATH = "/var/www/web_dev/settings"
    SHARED_DIR_PATH = "/var/www/web_dev/shared"

else:
    FLASK_PATH = r"C:\Users\iant\Documents\PROGRAMS\web_dev\fl"
    SECRET_KEY_PATH = r"C:\Users\iant\Documents\PROGRAMS\web_dev\settings"
    SHARED_DIR_PATH = r"C:\Users\iant\Documents\PROGRAMS\web_dev\shared"



sys.path.append(SECRET_KEY_PATH)
from secret_keys import SECRET_KEYS, venspec_ai_users



secret_key = SECRET_KEYS["venspec_ai"]

users = venspec_ai_users

actions_filepath = os.path.join(SHARED_DIR_PATH, "secret", "venspec_ai", "actions.tsv")