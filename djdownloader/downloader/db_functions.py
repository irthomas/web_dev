# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 12:00:21 2021

@author: iant

DOWNLOAD CACHE.DB FILES AND PROCESS CONTENTS

FOR OBS OVERVIEW:
OPEN ON SERVER:
    mysql -hsqlprod1-ae -unomad_user -p* nomad

DUMP:
mysqldump -hsqlprod1-ae -unomad_user -p* nomad > /home/iant/linux/obs_overview.sql

REBUILD:
./mysql2sqlite obs_overview.sql | sqlite3 obs_overview.db

"""


import posixpath
import os
# from datetime import datetime
import paramiko
import sqlite3
import re

from downloader.config import SECRET_KEYS, DB_PATH, SHARED_DIR_PATH
from downloader.models import LEVELS, REMOTE_DATA_PATH




def transfer_cache_db(level):
    """copy cache db for chosen level from remote path to local computer"""
    localpath = os.path.join(SHARED_DIR_PATH, "db", level + ".db")
    
    remotepath = posixpath.join(REMOTE_DATA_PATH, level, "cache.db")
    
    print("Connecting to hera")
    p = paramiko.SSHClient()
    p.set_missing_host_key_policy(paramiko.AutoAddPolicy())   # This script doesn't work for me unless this line is added!
    p.connect("hera.oma.be", port=22, username="iant", password=SECRET_KEYS["hera"])
    
    sftp = p.open_sftp()
    print("Downloading cache.db for level %s" %level)
    sftp.get(remotepath, localpath)
    sftp.close()
    p.close()


def connect_db(db_path):
    print("Connecting to database %s" %db_path)
    con = sqlite3.connect(db_path)
    return con

def close_db(con):
    con.close()


def empty_db(con):
    """delete table and rebuild empty"""
    print("Deleting table")

    cur = con.cursor()
    
    cur.execute('DROP TABLE IF EXISTS filenames')
    cur.execute('CREATE TABLE filenames (id INTEGER PRIMARY KEY AUTOINCREMENT, level TEXT NOT NULL, channel TEXT NOT NULL, filename TEXT NOT NULL)')


def get_filenames_from_cache(level):
    """get filenames from cache.db"""
    
    print("Getting data for level %s from cache.db" %level)
    localpath = os.path.join(SHARED_DIR_PATH, "db", level + ".db")
    
    con = connect_db(localpath)
    cur = con.cursor()
    cur.execute('SELECT path FROM files')
    rows = cur.fetchall()
    filepaths = [filepath[0] for filepath in rows]
    close_db(con)
    filenames = [os.path.split(filepath)[1] for filepath in filepaths]
    
    channels = [re.search("(SO|LNO|UVIS)", filename).group() for filename in filenames]
    return channels, filenames


def populate_db(con, level):
    """add all filenames to new sql database"""

    channels, filenames = get_filenames_from_cache(level)

    print("Adding %i files for level %s to levels.db" %(len(filenames), level))
    cur = con.cursor()
    for channel, filename in zip(channels, filenames):
        cur.execute('INSERT INTO filenames (level, channel, filename) VALUES (?,?,?)', (level, channel, filename))
    con.commit()


def make_db(transfer=False):
    """sort through data and add it to empty sql db"""
    
    if transfer:
        for level in LEVELS:
            transfer_cache_db(level)
    
    con = connect_db(DB_PATH)
    empty_db(con)

    for level in LEVELS:
        populate_db(con, level)
    close_db(con)

