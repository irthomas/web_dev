# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 20:36:15 2021

@author: iant

MAKE THE JSONS
"""

from db_config import DB_PATH, JSON_TEMPLATE_PATH
import json
import sqlite3 as sql
from datetime import datetime
import os

def make_cases_json():
    con = sql.connect(DB_PATH)
    con.row_factory = sql.Row
       
    cur = con.cursor()
    # cur.execute('SELECT * FROM "{}"'.format(COMMUNES[0]))
    cur.execute('SELECT * FROM cases')
       
    rows = cur.fetchall()
    con.close()
    
    dictionary_list = []
    for row in rows:
        row_date = datetime.strftime(datetime.strptime(row["date"], "%Y-%m-%d %H:%M:%S"), "%Y-%m-%d")
        dictionary = {"commune":row["commune"], "cases_date":row_date, "cases":row["cases"]}
        dictionary_list.append(dictionary)
    # e.g. {"commune": "Watermael-Boitsfort", "cases_date":"2020-03-03 00:00:00", "cases": 0}, 
    
    with open(os.path.join(JSON_TEMPLATE_PATH, "cases_template.json"), "r") as f:
        template = json.load(f)
    template["data"]["values"] = dictionary_list
    jdata = json.dumps(template, indent=4)
    
    # con.close()
    return jdata

def write_cases_json():
    with open(os.path.join(JSON_TEMPLATE_PATH, "cases.json"), "w") as f:
        f.write(make_cases_json())
        
        
        
        
        

def make_vacs_json(table_name):
    con = sql.connect(DB_PATH)
    con.row_factory = sql.Row
       
    cur = con.cursor()
    # cur.execute('SELECT * FROM "{}"'.format(COMMUNES[0]))
    cur.execute('SELECT * FROM {}'.format(table_name))
       
    rows = cur.fetchall()
    con.close()
    
    dictionary_list = []
    for row in rows:
        row_date = datetime.strftime(datetime.strptime(row["date"], "%Y-%m-%d %H:%M:%S"), "%Y-%m-%d")
        dictionary = {"age_group":"%s 1st dose" %row["age_group"], "vacs_date":row_date, "vacs":row["cumulative_percent_1"]}
        dictionary_list.append(dictionary)
        dictionary = {"age_group":"%s 2nd dose" %row["age_group"], "vacs_date":row_date, "vacs":row["cumulative_percent_2"]}
        dictionary_list.append(dictionary)
   
    with open(os.path.join(JSON_TEMPLATE_PATH, "vacs_template.json"), "r") as f:
        template = json.load(f)
    template["data"]["values"] = dictionary_list
    jdata = json.dumps(template, indent=4)
    
    # con.close()
    return jdata

def write_vacs_json():
    with open(os.path.join(JSON_TEMPLATE_PATH, "vacs.json"), "w") as f:
        f.write(make_vacs_json("vacs"))





def make_doses_json(table_name):
    con = sql.connect(DB_PATH)
    con.row_factory = sql.Row
       
    cur = con.cursor()
    # cur.execute('SELECT * FROM "{}"'.format(COMMUNES[0]))
    cur.execute('SELECT * FROM {}'.format(table_name))
       
    rows = cur.fetchall()
    con.close()
    
    dictionary_list = []
    for row in rows:
        row_date = datetime.strftime(datetime.strptime(row["date"], "%Y-%m-%d %H:%M:%S"), "%Y-%m-%d")
        dictionary = {"dosage":"Two dose vaccine", "doses_date":row_date, "doses":row["cumulative_doses_double"]}
        dictionary_list.append(dictionary)
        dictionary = {"dosage":"Two dose vaccine projected", "doses_date":row_date, "doses":row["cumulative_doses_double_projected"]}
        dictionary_list.append(dictionary)
        # dictionary = {"dosage":"One dose vaccine", "doses_date":row_date, "doses":row["cumulative_doses_single"]}
        # dictionary_list.append(dictionary)
   
    with open(os.path.join(JSON_TEMPLATE_PATH, "doses_template.json"), "r") as f:
        template = json.load(f)
    template["data"]["values"] = dictionary_list
    jdata = json.dumps(template, indent=4)
    
    # con.close()
    return jdata

def write_doses_json():
    with open(os.path.join(JSON_TEMPLATE_PATH, "doses.json"), "w") as f:
        f.write(make_doses_json("doses"))



