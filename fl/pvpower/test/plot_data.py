# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 20:42:08 2023

@author: iant
"""
import sqlite3 as sql
import os
from datetime import datetime, timezone
import numpy as np

import matplotlib.pyplot as plt

"""
price from grid, price to grid
0.153/0.098
0.192/0.129
0.474/0.348
"""

DB_PATH = r"C:\Users\iant\Documents\PROGRAMS\web_dev\fl\pvpower\db\pvpower.db"



fields = [
 'ElectricityTariff',
 # 'EnergyDeliveredTariff1',
 # 'EnergyReturnedTariff1',
 # 'EnergyDeliveredTariff2',
 # 'EnergyReturnedTariff2',
  'PowerDelivered_total',
  'PowerReturned_total',
 # 'PowerDelivered_l1',
 # 'PowerDelivered_l2',
 # 'PowerDelivered_l3',
 # 'PowerReturned_l1',
 # 'PowerReturned_l2',
 # 'PowerReturned_l3',
 # 'Voltage_l1',
 # 'Voltage_l2',
 # 'Voltage_l3',
 # 'Current_l1',
 # 'Current_l2',
 # 'Current_l3',
 # 'PowerDeliveredHour',
 # 'PowerDeliveredNetto',
 # 'QuarterHourPeakElectricityAverageDelivered',
 # 'PeakConsumptionRunningMonth'
]


def connect_db(db_path):
    # print("Opening db %s" %db_path)
    con = sql.connect(db_path, detect_types=sql.PARSE_DECLTYPES)
    return con

def close_db(con):
    con.close()



def fetchall(query):

    print(query)
    con = connect_db(DB_PATH)
    cur = con.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    close_db(con)
    
    return rows


def make_dict_from_fetchall(fields, rows):
    """get output from sqlite query and convert to dictionary"""
    
    if len(rows) == 0: #if no data return empty dict
        return {k:[] for k in fields}
    
    else: #make dictionary, one entry per field name
        rows_arr = [list(i) for i in zip(*rows)] #transpose list of lists
        
        out_d = {k:rows_arr[i] for i, k in enumerate(fields)}
        if "Utc" in out_d.keys():
            out_d["Utc"] = [datetime.strptime(dt, "%Y-%m-%d %H:%M:%S.%f").replace(tzinfo=timezone.utc).astimezone(tz=None) for dt in out_d["Utc"]]

        return out_d


def get_data_from_utc(fields, table_name, dt_str):
    
    query = (
        'SELECT %s ' %(", ".join(fields)) + # fields to return
        'FROM {} '.format(table_name) +  # table name
        'WHERE Utc LIKE "%s%%"' %(dt_str) #where date starts with dt str
    )
    rows = fetchall(query)    
    rows_d = make_dict_from_fetchall(fields, rows)
    
    return rows_d



    
    

def get_all_data(fields, table_name):
    
    query = (
        'SELECT %s ' %(", ".join(fields)) + # fields to return
        'FROM {} '.format(table_name)  # table name
    )
    
    rows = fetchall(query)
    rows_d = make_dict_from_fetchall(fields, rows)
    
    return rows_d



# fields = ["Utc", "PowerDelivered_total", "PowerReturned_total"]
table_name = "sg"

# plt.figure()
# secs = 0
# for i in range(6, 31):
dt = datetime(2023, 7, 1)
dt_str = datetime.strftime(dt, "%Y-%m")


# rows_d = get_data_from_utc(fields+["Utc"], table_name, dt_str)
# for field in fields:
#     plt.figure()
#     plt.title(field)
#     plt.plot(rows_d["Utc"], rows_d[field])    
    
    
# # plt.plot(rows_d["PowerDelivered_total"], alpha=0.1)
# plt.plot(rows_d["PowerDelivered_total"])
# plt.plot(rows_d["PowerReturned_total"])
# # print(i, sum(rows_d["PowerDelivered_total"])/1e6)
    
# plt.plot(rows_d["Utc"], rows_d["PowerDelivered_total"])



def first_values_of_day(field_names, table_name):
    
    query = (
        'SELECT %s ' %(", ".join(field_names)) + # fields to return
        'FROM {} '.format(table_name) + # table name
        'GROUP BY date(Utc);'
        )
    rows = fetchall(query)
    rows_d = make_dict_from_fetchall(field_names, rows)
        
    return rows_d


field_names = ["EnergyDeliveredTariff1", "EnergyDeliveredTariff2", "EnergyReturnedTariff1", "EnergyReturnedTariff2"]
table_name = "sg"
rows_d = first_values_of_day(field_names+["Utc"], table_name)

ixs = np.asarray([i for i,dt in enumerate(rows_d["Utc"]) if dt > datetime(2023, 7, 6, tzinfo=timezone.utc)])

for field_name in field_names:
    rows_d[field_name] = np.asfarray(rows_d[field_name])

plt.figure()
# plt.title("EnergyDelivered")
plt.bar(np.asarray(rows_d["Utc"])[ixs][:-1], np.diff(rows_d["EnergyReturnedTariff1"][ixs]+rows_d["EnergyReturnedTariff2"][ixs]), label="Energy to grid")    
plt.bar(np.asarray(rows_d["Utc"])[ixs][:-1], -np.diff(rows_d["EnergyDeliveredTariff1"][ixs]+rows_d["EnergyDeliveredTariff2"][ixs]), label="Energy from grid")    
plt.legend()
plt.ylabel("Energy (kWh)")
plt.xticks(np.asarray(rows_d["Utc"])[ixs][:-1], rotation=90)
plt.grid()
# plt.figure()
# plt.title("EnergyReturned")
