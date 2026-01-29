# -*- coding: utf-8 -*-
"""
Created on Wed May 19 10:13:40 2021

@author: iant

CONTINUOUSLY UPDATE EVERY 10 SECONDS. RUN IN SEPARATE TERMINAL
"""
import os
import time

from db_functions_tuya import make_db, DB_PATH_TUYA

if not os.path.exists(DB_PATH_TUYA):
    make_db(clear=True)

i = 0
while True:
    make_db(clear=False)
    time.sleep(10)
    i += 1
    
    if i - (i // 1000)*1000 == 0:
        print(i)


