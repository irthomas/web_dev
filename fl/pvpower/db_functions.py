# -*- coding: utf-8 -*-
"""
Created on Fri Mar 19 10:33:11 2021

@author: iant

DB FUNCTIONS
"""



import sqlite3 as sql
import os
# import sys
from datetime import datetime
# import requests
from config import DB_PATH, pv_ip_address

# Plus ID and UTC
dict_refs = {
    "ElectricityTariff":"ElectricityTariff",
    "EnergyDeliveredTariff1":"EnergyDeliveredTariff1",
    "EnergyReturnedTariff1":"EnergyReturnedTariff1",
    "EnergyDeliveredTariff2":"EnergyDeliveredTariff2",
    "EnergyReturnedTariff2":"EnergyReturnedTariff2",
    "PowerDelivered_total":"PowerDelivered_total", # grid to home
    "PowerReturned_total":"PowerReturned_total", # home to grid
    "PowerDelivered_l1":"PowerDelivered_l1",
    "PowerDelivered_l2":"PowerDelivered_l2",
    "PowerDelivered_l3":"PowerDelivered_l3",
    "PowerReturned_l1":"PowerReturned_l1",
    "PowerReturned_l2":"PowerReturned_l2",
    "PowerReturned_l3":"PowerReturned_l3",
    "Voltage_l1":"Voltage_l1",
    "Voltage_l2":"Voltage_l2",
    "Voltage_l3":"Voltage_l3",
    "Current_l1":"Current_l1",
    "Current_l2":"Current_l2",
    "Current_l3":"Current_l3",
    "PowerDeliveredHour":"PowerDeliveredHour",
    "PowerDeliveredNetto":"PowerDeliveredNetto", # delivered - returned
    "QuarterHourPeakElectricityAverageDelivered":"QuarterHourPeakElectricityAverageDelivered",
    "PeakConsumptionRunningMonth":"PeakConsumptionRunningMonth",
}




def get_sg_data():
    
    import urllib.request, json 
    try:
        with urllib.request.urlopen("http://%s/smartmeter/api/read" %pv_ip_address) as url:
            data = json.load(url)
    except Exception:
        return {}
        
    return {k:v for k,v in data.items() if k in dict_refs.values()}
        
    
    
    
    
    
    
def connect_db(db_path):
    # print("Opening db %s" %db_path)
    con = sql.connect(db_path, detect_types=sql.PARSE_DECLTYPES)
    return con

def close_db(con):
    con.close()






def get_db_rows(table_name):
    con = connect_db(DB_PATH)
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
    
    if table_name == "sg":
        query = """CREATE TABLE sg (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                Utc TEXT NOT NULL, \
                ElectricityTariff REAL NOT NULL, \
                EnergyDeliveredTariff1 REAL NOT NULL, \
                EnergyReturnedTariff1 REAL NOT NULL, \
                EnergyDeliveredTariff2 REAL NOT NULL, \
                EnergyReturnedTariff2 REAL NOT NULL, \
                PowerDelivered_total REAL NOT NULL, \
                PowerReturned_total REAL NOT NULL, \
                PowerDelivered_l1 REAL NOT NULL, \
                PowerDelivered_l2 REAL NOT NULL, \
                PowerDelivered_l3 REAL NOT NULL, \
                PowerReturned_l1 REAL NOT NULL, \
                PowerReturned_l2 REAL NOT NULL, \
                PowerReturned_l3 REAL NOT NULL, \
                Voltage_l1 REAL NOT NULL, \
                Voltage_l2 REAL NOT NULL, \
                Voltage_l3 REAL NOT NULL, \
                Current_l1 REAL NOT NULL, \
                Current_l2 REAL NOT NULL, \
                Current_l3 REAL NOT NULL, \
                PowerDeliveredHour REAL NOT NULL, \
                PowerDeliveredNetto REAL NOT NULL, \
                QuarterHourPeakElectricityAverageDelivered REAL NOT NULL, \
                PeakConsumptionRunningMonth REAL NOT NULL) """
        
        cur.execute(query)







def make_db(clear=False):
    
    sg_d = get_sg_data()
    if len(sg_d.keys()) > 0:
        populate_sg_db(sg_d, clear=clear)
    



def populate_sg_db(sg_d, clear=False):
    
    
    db_path = os.path.join(DB_PATH)
    con = connect_db(db_path)
    if clear:
        print("Making empty table")
        empty_table(con, "sg")
        
    cur = con.cursor()
    
    field_names = ["Utc"] + list(dict_refs.keys())
    field_names_text = ", ".join(field_names)
    
    questions_str = ",".join(["?"] * len(field_names))
    data = [datetime.utcnow()] + [sg_d[k] for k in dict_refs.keys()]

   
    if not clear:
        # print("Adding new entry to db")
        cur.execute('INSERT INTO sg (%s) VALUES (%s)' %(field_names_text, questions_str), data)

    con.commit()
    close_db(con)





# fields = ["Utc", "PowerDelivered_total", "PowerReturned_total"]
# table_name = "sg"
# dt = datetime(2023, 6, 19)

# dt_str = datetime.strftime(dt, "%Y-%m-%d")


def make_dict_from_fetchall(fields, rows):
    """get output from sqlite query and convert to dictionary"""
    
    if len(rows) == 0: #if no data return empty dict
        return {k:[] for k in fields}
    
    else: #make dictionary, one entry per field name
        rows_arr = [list(i) for i in zip(*rows)] #transpose list of lists
        return {k:rows_arr[i] for i, k in enumerate(fields)}


def get_data_from_utc(fields, table_name, dt_str):
    
    con = connect_db(DB_PATH)
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


def get_pv_for_day(dt):
    """function to get most important data for 1 day"""
    
    fields = ["Utc", "PowerDelivered_total", "PowerReturned_total"]
    table_name = "sg"

    dt_str = datetime.strftime(dt, "%Y-%m-%d")
    rows_d = get_data_from_utc(fields, table_name, dt_str)

    return rows_d




def get_pv_for_month(dt):
    """function to get most important data for 1 month"""
    
    fields = ["Utc", "PowerDelivered_total", "PowerReturned_total"]
    table_name = "sg"

    dt_str = datetime.strftime(dt, "%Y-%m")
    rows_d = get_data_from_utc(fields, table_name, dt_str)

    return rows_d




