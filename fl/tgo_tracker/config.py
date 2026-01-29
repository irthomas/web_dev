# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 22:24:20 2021

@author: iant

DB CONFIG
"""

import platform


if platform.system() == "Linux":

    # DB_PATH = "/var/www/web_dev/fl/tgo_tracker/tgo_tracker.db"
    JSON_TEMPLATE_PATH = "/var/www/web_dev/fl/tgo_tracker/templates/tgo_tracker_template.json"
else:
    # DB_PATH = "tgo_tracker.db"
    JSON_TEMPLATE_PATH = "templates/tgo_tracker_template.json"


