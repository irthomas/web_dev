# -*- coding: utf-8 -*-
"""
Created on Wed May 12 16:54:39 2021

@author: iant

CONFIG
"""

import platform
import sys
import os

if platform.system() == "Linux":
    FLASK_PATH = "/var/www/web_dev/fl"
    SECRET_KEY_PATH = "/var/www/web_dev/settings"
    SHARED_DIR_PATH = "/var/www/web_dev/shared"

else:
    FLASK_PATH = r"C:\Users\iant\Documents\PROGRAMS\web_dev\fl"
    SECRET_KEY_PATH = r"C:\Users\iant\Documents\PROGRAMS\web_dev\settings"
    SHARED_DIR_PATH = r"C:\Users\iant\Documents\PROGRAMS\web_dev\shared"


APP_PATH = os.path.join(FLASK_PATH, "file_tree")
DB_PATH = os.path.join(APP_PATH, "db", "file_tree.db")
UPLOAD_PATH = os.path.join(APP_PATH, "upload")

LEVELS = [
    "hdf5_level_0p1a",
    "hdf5_level_0p1d",
    "hdf5_level_0p1e",
    "hdf5_level_0p2a",
    "hdf5_level_0p2b",
    "hdf5_level_0p3a",
    "hdf5_level_0p3b",
    "hdf5_level_0p3c",
    "hdf5_level_0p3i",
    "hdf5_level_0p3j",
    "hdf5_level_0p3k",
    "hdf5_level_1p0a",
    # "hdf5_level_1p0b",
    ]

CHANNELS = ["SO", "LNO", "UVIS"]
COLUMN_NAMES = ["itl_dt", "orbit", "obs_type", "channel"] + LEVELS



REMOTE_HDF5_PATH = "/bira-iasb/data/SATELLITE/TRACE-GAS-ORBITER/NOMAD/hdf5/"
REMOTE_OBS_DB_FILE_PATH = "/bira-iasb/projects/NOMAD/Data/pfm_auxiliary_files/observation_type/obs_type.db"

LOCAL_DB_PATH = os.path.join(APP_PATH, "db")

# DEBUG = True

sys.path.append(SECRET_KEY_PATH)
from secret_keys import SECRET_KEYS

DT_FORMAT = "%Y-%m-%d %H:%M:%S"