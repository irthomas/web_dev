# -*- coding: utf-8 -*-
"""
Created on Wed May 12 16:54:39 2021

@author: iant

CONFIG
"""

import platform
# import sys
import os

if platform.system() == "Linux":
    FLASK_PATH = "/var/www/web_dev/fl"

else:
    FLASK_PATH = r"C:\Users\iant\Documents\PROGRAMS\web_dev\fl"


APP_PATH = os.path.join(FLASK_PATH, "cop_tables")
COP_DATE = "mtp063_proposed"


# DEBUG = True

# sys.path.append(SECRET_KEY_PATH)
# from secret_keys import SECRET_KEYS

