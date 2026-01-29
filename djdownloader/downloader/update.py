# -*- coding: utf-8 -*-
"""
Created on Mon Jun 28 13:51:37 2021

@author: iant
"""
import sys
sys.path.append('/var/www/web_dev/djdownloader')

from downloader.db_functions import make_db


# make_db(transfer=False)
make_db(transfer=True)