# from django.db import models
import sqlite3
import re
import posixpath
from datetime import datetime
import paramiko

from downloader.config import DB_PATH, SECRET_KEYS
from secret_keys import APPROVED_EMAILS
# Create your models here.

CHANNELS = ["SO", "LNO", "UVIS"]
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
    "hdf5_level_1p0b",
    ]

REMOTE_DATA_PATH = "/bira-iasb/data/SATELLITE/TRACE-GAS-ORBITER/NOMAD/hdf5/"
TMP_ZIP_PATH = "/home/iant/projects/work/NOMAD/Science/ian/website_tmp/"



def connect_db():
    con = sqlite3.connect(DB_PATH)
    return con

def close_db(con):
    con.close()

def check_email(email):
    if email in APPROVED_EMAILS:
        print("Email address %s approved" %email)
        return True
    else:
        print("Error: email address %s not approved" %email)
        return False

def regexp(exp, regex_str):
    regex = re.compile(exp)
    return regex.search(regex_str) is not None


"""for obs overview db"""
# def search_db(regex_str, channel):
#     """search filename field for regex"""
#     con = connect_db()
#     con.create_function("REGEXP", 2, regexp)
#     cur = con.cursor()
#     table_name = "data_%s" %channel.lower()
#     cur.execute('SELECT filename FROM {} WHERE filename REGEXP ?'.format(table_name), [regex_str])
#     rows = cur.fetchall()
#     filenames = [filename[0] for filename in rows]
#     close_db(con)
#     return filenames

def search_db(regex_str, channel, level):
    """search filename field for regex"""
    
   
    con = connect_db()
    con.create_function("REGEXP", 2, regexp)
    cur = con.cursor()
    cur.execute('SELECT filename FROM filenames WHERE filename REGEXP ? AND channel=? AND level=?', [regex_str.strip(), channel, level])
    rows = cur.fetchall()
    filenames = [filename[0] for filename in rows]
    close_db(con)
    return filenames



def make_hdf5_filepaths(hdf5_level, filenames):
    
    print("Making lists of filepaths")
    filepaths = []
    
    
    for filename in filenames:
        year = filename[0:4]
        month = filename[4:6]
        day = filename[6:8]
        filepath = posixpath.join(hdf5_level, year, month, day, filename)
        filepaths.append(filepath)
        
    n = len(filepaths)
        
    #split into multiple lists if more than 1000 files
    filepaths_strs = []
    for i_start in range(0, n, 1000):
        i_end = min(i_start + 1000, n)
        
        filepaths_strs.append(" ".join(filepaths[i_start:i_end]))
    return filepaths, filepaths_strs

def make_zip_filepath(email):

    print("Making zip filepath")
    time_now_str = datetime.strftime(datetime.now(), "%H%M%S")
    zip_filename = email.split("@")[0].replace(".","") + "_" + time_now_str + ".zip"
    zip_filepath = "%s/%s" %(TMP_ZIP_PATH, zip_filename)
    
    return zip_filename, zip_filepath



def make_zip_file(zip_filepath, filepaths_strs):
    
    print("Making zip file")
    
    commands_all = []
    for filepaths_str in filepaths_strs:
    
        commands_all.append([
            "cd %s" %REMOTE_DATA_PATH, 
            "zip %s %s" %(zip_filepath, filepaths_str),
        ])
    commands_all.append([
        "curl -T %s -u nomad:%s ftp://ftp-ae.oma.be/tmp/" %(zip_filepath, SECRET_KEYS["nomad_ftp"]),
        "rm %s" %zip_filepath,
    ])
    
    output = []
    for i, commands in enumerate(commands_all):
        print("Executing command %i" %i)
        commands_joined = ";".join(commands)
        
        p = paramiko.SSHClient()
        p.set_missing_host_key_policy(paramiko.AutoAddPolicy())   # This script doesn't work for me unless this line is added!
        p.connect("hera.oma.be", port=22, username="iant", password=SECRET_KEYS["hera"])
        
        # print(commands_joined)
        stdin, stdout, stderr = p.exec_command(commands_joined)
        output.append(stdout.readlines())
    # opt = "".join(opt)
    return output



def delete_zip_file(zip_filename):
    #curl -v -u username:pwd ftp://host/FileTodelete.xml -Q "DELE FileTodelete.xml"

    command = "curl -v -u nomad:%s ftp://ftp-ae.oma.be/ -Q 'DELE /tmp/%s'" %(SECRET_KEYS["nomad_ftp"], zip_filename)
    
    p = paramiko.SSHClient()
    p.set_missing_host_key_policy(paramiko.AutoAddPolicy())   # This script doesn't work for me unless this line is added!
    p.connect("hera.oma.be", port=22, username="iant", password=SECRET_KEYS["hera"])
    
    # print(command)
    stdin, stdout, stderr = p.exec_command(command)
    opt = stdout.readlines()
    # opt = "".join(opt)
    return opt
