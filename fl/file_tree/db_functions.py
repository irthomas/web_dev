# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 10:33:11 2021

@author: iant

DB FUNCTIONS
"""



import sqlite3 as sql
import re
import os
# import sys
# from datetime import datetime
import posixpath
from datetime import datetime, timedelta
import paramiko
import numpy as np


from config import SHARED_DIR_PATH, DB_PATH, REMOTE_HDF5_PATH, REMOTE_OBS_DB_FILE_PATH, SECRET_KEYS, DT_FORMAT
from config import LEVELS, CHANNELS, COLUMN_NAMES




def transfer_file_from_hera(local_path, remote_path):

    print("Connecting to hera")
    p = paramiko.SSHClient()
    p.set_missing_host_key_policy(paramiko.AutoAddPolicy())   # This script doesn't work for me unless this line is added!
    p.connect("hera.oma.be", port=22, username="iant", password=SECRET_KEYS["hera"])
    
    sftp = p.open_sftp()
    sftp.get(remote_path, local_path)
    sftp.close()
    p.close()
    


def transfer_cache_db(level):
    """copy cache db for chosen level from remote path to local computer"""

    local_path = os.path.join(SHARED_DIR_PATH, "db", level + ".db")
    remote_path = posixpath.join(REMOTE_HDF5_PATH, level, "cache.db")
    
    print("Downloading cache.db for level %s" %level)
    transfer_file_from_hera(local_path, remote_path)
    


def transfer_obs_type_db():
    """copy obs type db from remote path to local computer"""

    local_path = os.path.join(SHARED_DIR_PATH, "db", "obs_type.db")
    
    print("Downloading obs_type.db")
    transfer_file_from_hera(local_path, REMOTE_OBS_DB_FILE_PATH)
    

    

    
def connect_db(db_path):
    con = sql.connect(db_path, detect_types=sql.PARSE_DECLTYPES)
    return con

def close_db(con):
    con.close()
    


   
    
def get_all_rows_from_db(db_path, table_name):
    con = sql.connect(db_path, detect_types=sql.PARSE_DECLTYPES)
    con.row_factory = sql.Row
       
    cur = con.cursor()
    #first get column names
    cur.execute("PRAGMA table_info({})".format(table_name))
    rows = cur.fetchall()
    field_names = []
    field_types = []
    for row in rows:
        field_names.append(row[1])
        field_types.append(row[2])
    
    #now get all data
    cur.execute('SELECT * FROM {}'.format(table_name))
       
    rows = cur.fetchall()
    con.close()
    
    #make dictionary
    dictionary = {k:[] for k in field_names}
    for row in rows:
        for field_name, field_type in zip(field_names, field_types):
            dictionary[field_name].append(row[field_name])
        

    return dictionary
    





def search_db(con, table_name, field_name, start, end):
    """search filename field for regex"""

    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM files WHERE %s BETWEEN '%s' AND '%s'" %(field_name, start, end))
    rows = cur.fetchall()

    return rows


def empty_table(con, table_name):
    """delete table and rebuild empty"""
    print("Deleting and rebuilding table", table_name)

    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS {}'.format(table_name))
    
    if table_name == "tree":
        query = """CREATE TABLE tree (id INTEGER PRIMARY KEY AUTOINCREMENT, \
            itl_dt TIMESTAMP NOT NULL, \
            orbit INTEGER NOT NULL, \
            obs_type TEXT NOT NULL, \
            channel TEXT NOT NULL, """
        
        # for channel in CHANNELS:
        for level in LEVELS:
            query += "%s TEXT, " %(level)
        
        query = query[:-2]+ ")" #remove final ', ' and add closing bracket
        cur.execute(query)



def make_db(transfer=True, dt_range=[], clear=False):
    
    if transfer:
        transfer_obs_type_db()
        
        for level in LEVELS:
            transfer_cache_db(level)
            
    d_itl = get_itl_dict()
    tree_dict_all = make_matching_files_dict(d_itl, dt_range=dt_range)
    populate_file_tree_db(d_itl, tree_dict_all, dt_range=dt_range, clear=clear)
    


def get_itl_dict():
    print("Getting data from itl table in obs_type.db")
    db_path = os.path.join(SHARED_DIR_PATH, "db", "obs_type.db")
    table_name = "obs_from_itl"
    d_itl = get_all_rows_from_db(db_path, table_name)
    
    #sort itl dictionary by tc20_exec_start
    sort_indices = [i[1] for i in sorted((e,i) for i,e in enumerate(d_itl["tc20_exec_start"]))]
    for key in d_itl.keys():
        d_itl[key] = [d_itl[key][i] for i in sort_indices]
    
    return d_itl





def h5_filename_to_datetime(h5_f):
    
    dt = datetime(int(h5_f[0:4]), int(h5_f[4:6]), int(h5_f[6:8]), int(h5_f[9:11]), int(h5_f[11:13]), int(h5_f[13:15]))
    return dt




def make_cache_dbs_dict(dt_range=[]):
    """get a dictionary of h5_level:channel:datetimes:h5_filename for all levels in the time range"""

    #get full time range if not supplied
    if len(dt_range)==0:
        dt_range = [datetime(2018, 1, 1), datetime(2040, 1, 1)]

    #get data from all dbs of all levels
    table_name = "files"
    d_dbs = {}
    for level in LEVELS:
        print("Getting data from %s.db" %level)
        db_path = os.path.join(SHARED_DIR_PATH, "db", level+".db")
        con = connect_db(db_path)
        
        #get all rows from itl db for full time range
        #sort into a dictionary by channel and by observation datetime (from filename)
        rows = search_db(con, table_name, "beg_dtime", dt_range[0], dt_range[1])
        d_channel_obs = {k:{} for k in CHANNELS}
        for row in rows:
            h5_f = os.path.basename(row[0])
            h5_f_dt = h5_filename_to_datetime(h5_f)
            h5_channel = re.match("\d*_\d*_[0-9]p[0-9][a-z]_([A-Z]*)(?:\.h5|_.*)", h5_f)[1]
            
            if h5_f_dt not in d_channel_obs[h5_channel].keys():
                d_channel_obs[h5_channel][h5_f_dt] = ""
            
            d_channel_obs[h5_channel][h5_f_dt] += h5_f+"\n"
        d_dbs[level] = d_channel_obs
    
        close_db(con)
    return d_dbs



def nearest_ind(items, pivot):
    time_diff = np.abs([date - pivot for date in items])
    return time_diff.argmin(0)




def progress(iterable, total):
    """generic progress bar"""
    
    length=50

    def printProgressBar (iteration):
        percent = ("{0:.1f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = "*" * filledLength + '-' * (length - filledLength)
        print(f'\r |{bar}| {percent}% ', end = "\r")

    printProgressBar(0)

    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    print()
    
    
    

def make_matching_files_dict(d_itl, dt_range=[]):    
    
    """faster version of the function"""
    
    d_dbs = make_cache_dbs_dict(dt_range=dt_range)
    
    #get generic time range
    if len(dt_range)==0:
        dt_range = [datetime(2018, 1, 1), datetime(2040, 1, 1)]
    
    #get indices of itl obs in range
    itl_ixs = [i for i, dt in enumerate(d_itl["tc20_exec_start"]) if (dt > dt_range[0] and dt < dt_range[1])]
    itl_dts = [dt for i, dt in enumerate(d_itl["tc20_exec_start"]) if i in itl_ixs]
    itl_channels_list = [s.split(", ") for i,s in enumerate(d_itl["channels"]) if i in itl_ixs]

    print("Matching execution times to hdf5 databases for %i observations" %(len(itl_ixs)))
    
    tree_dict_all = {}
    
    matching_dts = {}
    for i, (itl_dt, itl_channels) in progress(enumerate(zip(itl_dts, itl_channels_list)), len(itl_dts)):
        
        tree_dict_all[itl_dt] = {k:[] for k in itl_channels}
        for level in LEVELS:
            for itl_channel in itl_channels:
                #check if there are filenames for that level
                if len(d_dbs[level][itl_channel]) > 0:
                    
                    #speed up matching - if previously found, just use the match again
                    if itl_dt in matching_dts.keys():
                        nearest_db_dt = matching_dts[itl_dt]
                    
                    else:
                        db_dt_list = sorted(list(d_dbs[level][itl_channel].keys()))
                        nearest_ix = nearest_ind(db_dt_list, itl_dt)
                        nearest_db_dt = db_dt_list[nearest_ix]
                        delta_dt = (itl_dt - nearest_db_dt).total_seconds()
                        matching_dts[itl_dt] = nearest_db_dt
                    # print(itl_dt, delta_dt)
                    
                    if np.abs(delta_dt) < 120:
                        if nearest_db_dt in d_dbs[level][itl_channel].keys():
                            tree_dict_all[itl_dt][itl_channel].append(d_dbs[level][itl_channel][nearest_db_dt].strip())
                        else:
                            tree_dict_all[itl_dt][itl_channel].append("")
                    else:
                        print("Error, time difference is too large:", itl_channel, level, itl_dt, "error = ", delta_dt)
                        tree_dict_all[itl_dt][itl_channel].append("")
                else:
                    tree_dict_all[itl_dt][itl_channel].append("")
        
        

    return tree_dict_all




def populate_file_tree_db(d_itl, tree_dict_all, dt_range=[], clear=False):
    
    
    levels_str = ", ".join(COLUMN_NAMES)
    questions_str = ",".join(["?"] * len(COLUMN_NAMES))
    
    db_path = os.path.join(DB_PATH)
    con = connect_db(db_path)
    if clear:
        empty_table(con, "tree")
    cur = con.cursor()

    #get generic time range
    if len(dt_range)==0:
        dt_range = [datetime(2018, 1, 1), datetime(2040, 1, 1)]

    #get indices of itl obs in range
    itl_ixs = [i for i, dt in enumerate(d_itl["tc20_exec_start"]) if (dt > dt_range[0] and dt < dt_range[1])]
    # itl_dts = [dt for i, dt in enumerate(d_itl["tc20_exec_start"]) if i in itl_ixs]
    itl_channels_list = [s.split(", ") for i,s in enumerate(d_itl["channels"]) if i in itl_ixs]
    itl_orbits_list = [s for i,s in enumerate(d_itl["orbit"]) if i in itl_ixs]
    itl_obs_type_list = [s for i,s in enumerate(d_itl["tc20_obs_type"]) if i in itl_ixs]


    #get indices of itl obs in range
    tree_dict_dts = [dt for dt in tree_dict_all.keys() if (dt > dt_range[0] and dt < dt_range[1])]

    #both should have the same length
    
    print("Repopulating file tree table with %i entries" %(len(tree_dict_dts)))
    for i in range(len(tree_dict_dts)):
    
    # for itl_dt, itl_channels, tree_dict_dt in progress(zip(itl_dts, itl_channels_list, tree_dict_dts)):

        tree_dict_dt = tree_dict_dts[i]
        for itl_channel in itl_channels_list[i]:
            line0 = [tree_dict_dt, itl_orbits_list[i], itl_obs_type_list[i], itl_channel]
            line0 += [n if n != "" else "NULL" for n in tree_dict_all[tree_dict_dt][itl_channel]]
            # print('INSERT INTO tree (%s) VALUES (%s)' %(levels_str, questions_str))
            # print(line0)
            cur.execute('INSERT INTO tree (%s) VALUES (%s)' %(levels_str, questions_str), line0)

    con.commit()
    close_db(con)



