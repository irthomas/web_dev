# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 10:33:11 2021

@author: iant

DB FUNCTIONS
"""



import sqlite3
import re
# import sys
# from datetime import datetime

from config import DB_PATH



    
    
def connect_db():
    con = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    return con

def close_db(con):
    con.close()


def regexp(exp, regex_str):
    regex = re.compile(exp)
    return regex.search(regex_str) is not None



def search_db(table_name, search_params):
    """search filename field for regex"""
    # con = connect_db()
    # con.create_function("REGEXP", 2, regexp)
    # cur = con.cursor()
    # cur.execute('SELECT * FROM {} WHERE filename REGEXP ?'.format(table_name), [regex_str])

    print(search_params)
    con = connect_db()
    cur = con.cursor()
    cur.execute('SELECT * FROM {} WHERE utc_start_time BETWEEN ? AND ? AND mtp_number BETWEEN ? AND ?'.format(table_name), \
        [
            search_params["utc_start_time_s"], 
            search_params["utc_start_time_e"],
            search_params["mtp_s"],
            search_params["mtp_e"],
            
        ])


    rows = cur.fetchall()
    close_db(con)
    return rows
