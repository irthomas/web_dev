# -*- coding: utf-8 -*-
"""
Created on Mon May 17 13:19:57 2021

@author: iant
"""

from datetime import datetime

def get_dt(dt_str):
    patterns = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]

    for pattern in patterns:
        try:
            return datetime.strptime(dt_str, pattern)
        except:
            pass

    return None