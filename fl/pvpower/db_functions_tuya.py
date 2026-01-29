#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 16:11:34 2026

@author: debian
"""


from datetime import datetime, timedelta
import time
import tinytuya
import sqlite3 as sql
import os

from config import DB_PATH_TUYA, TUYA_API

# Plus ID and UTC
DICT_REFS = {
    "Dishwasher":"Dishwasher",
    "Washing_machine":"Washing_machine",
    "Fridge_and_freezer":"Fridge_and_freezer",
}

class tuya(object):

    def __init__(self):
        self.connect()
        self.get_devices()

    def connect(self):
        self.tt = tinytuya.Cloud(
            apiRegion=TUYA_API["region"],
            apiKey=TUYA_API["key"],
            apiSecret=TUYA_API["secret"],
            apiDeviceID=TUYA_API["id"]
            )

    def get_devices(self):
        """get dictionary of devices"""
        devices = self.tt.getdevices()
        self.device_d = {device["name"]: device["id"] for device in devices}

    def get_power(self, name):
        """get power in watts"""
        id_ = self.device_d[name]
        status = self.tt.getstatus(id_)
        return status["result"][4]["value"] / 10.0

    def switch_on(self, name):
        id_ = self.device_d[name]
        commands = {
            "commands": [
                {"code": "switch_1", "value": True},
                {"code": "countdown_1", "value": 0},
            ]
        }
        result = self.tt.sendcommand(id_, commands)
        return result

    def switch_off(self, name):
        id_ = self.device_d[name]
        commands = {
            "commands": [
                {"code": "switch_1", "value": False},
                {"code": "countdown_1", "value": 0},
            ]
        }
        result = self.tt.sendcommand(id_, commands)
        return result


def connect_db(db_path):
    # print("Opening db %s" %db_path)
    con = sql.connect(db_path, detect_types=sql.PARSE_DECLTYPES)
    return con

def close_db(con):
    con.close()

def get_db_rows(table_name):
    con = connect_db(DB_PATH_TUYA)
    cur = con.cursor()
    cur.execute('SELECT * FROM {}'.format(table_name))


    rows = cur.fetchall()
    close_db(con)
    return rows


def empty_table(con, table_name):
    """delete table and rebuild empty"""
    print("Deleting and rebuilding table", table_name)

    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS {}'.format(table_name))
    
    if table_name == "tuya":
        query = """CREATE TABLE tuya (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                Utc TEXT NOT NULL, \
                Dishwasher REAL NOT NULL, \
                Washing_machine REAL NOT NULL, \
                Fridge_and_freezer REAL NOT NULL) """
        
        cur.execute(query)

def populate_tuya_db(tuya_d, clear=False):
    
    
    db_path_tuya = os.path.join(DB_PATH_TUYA)
    con = connect_db(db_path_tuya)
    if clear:
        empty_table(con, "tuya")
        
    cur = con.cursor()
    
    field_names = ["Utc"] + list(DICT_REFS.keys())
    field_names_text = ", ".join(field_names)
    
    questions_str = ",".join(["?"] * len(field_names))
    data = [datetime.utcnow()] + [tuya_d[k] for k in DICT_REFS.keys()]

   
    if not clear:
        # print("Adding new entry to db")
        cur.execute('INSERT INTO tuya (%s) VALUES (%s)' %(field_names_text, questions_str), data)

    con.commit()
    close_db(con)


def get_plug_data(tuya_plugs):
    
    names = DICT_REFS.keys() 
    powers = {name:tuya_plugs.get_power(name) for name in names}
    
    return powers


def make_db(clear=False):
    tuya_plugs = tuya()
    # print(tuya_plugs.device_d)
    
    tuya_d = get_plug_data(tuya_plugs)
    if len(tuya_d.keys()) > 0:
        populate_tuya_db(tuya_d, clear=clear)
    
    
def make_dict_from_fetchall(fields, rows):
    """get output from sqlite query and convert to dictionary"""
    
    if len(rows) == 0: #if no data return empty dict
        return {k:[] for k in fields}
    
    else: #make dictionary, one entry per field name
        rows_arr = [list(i) for i in zip(*rows)] #transpose list of lists
        return {k:rows_arr[i] for i, k in enumerate(fields)}


def get_data_from_utc(fields, table_name, dt_str):
    
    con = connect_db(DB_PATH_TUYA)
    cur = con.cursor()
    cur.execute(
        'SELECT %s ' %(", ".join(fields)) + # fields to return
        'FROM {} '.format(table_name) +  # table name
        'WHERE Utc LIKE "%s%%"' %(dt_str) #where date starts with dt str
        )
    rows = cur.fetchall()
    close_db(con)
    
    rows_d = make_dict_from_fetchall(fields, rows)
    
    return rows_d


def get_plugs_for_day(dt):
    """function to get most important data for 1 day"""
    
    fields = ["Utc", "Dishwasher", "Washing_machine", "Fridge_and_freezer"]
    table_name = "tuya"

    dt_str = datetime.strftime(dt, "%Y-%m-%d")
    rows_d = get_data_from_utc(fields, table_name, dt_str)

    return rows_d
