# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 14:49:32 2022

@author: iant

CONFIG
"""

import platform
# import sys


if platform.system() == "Linux":

    SECRET_KEY_PATH = "/var/www/web_dev/settings"
    SHARED_DIR_PATH = "/var/www/web_dev/shared"
    JSON_TEMPLATE_DIR = "/var/www/web_dev/fl/nomad_orders/templates"
    JSON_TEMPLATE_PATH = "/var/www/web_dev/fl/nomad_orders/templates/nomad_orders_template.json"

else:

    SECRET_KEY_PATH = r"C:\Users\iant\Dropbox\NOMAD\Python\web_dev\settings"
    SHARED_DIR_PATH = r"C:\Users\iant\Dropbox\NOMAD\Python\web_dev\shared"
    JSON_TEMPLATE_DIR = r"C:\Users\iant\Dropbox\NOMAD\Python\web_dev\fl\nomad_orders\templates"
    JSON_TEMPLATE_PATH = r"C:\Users\iant\Dropbox\NOMAD\Python\web_dev\fl\nomad_orders\templates\nomad_orders_template.json"

# DEBUG = True

# sys.path.append(SECRET_KEY_PATH)
# from secret_keys import SECRET_KEYS
