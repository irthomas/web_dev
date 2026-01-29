# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 10:34:31 2020

@author: iant

GET JSON DATA AND SAVE TO SQLITE DB
"""
from urllib.request import urlopen
import json
from datetime import datetime, timedelta
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import os

from db_config import DB_PATH, BASE_PATH, COMMUNES, POPULATIONS, AGE_GROUPS, POP_DIST



def connect_db(db_path):
    print("Opening db connection")
    con = sqlite3.connect(db_path)
    return con

def empty_table(con, table_name):
    """delete table and rebuild empty"""
    print("Deleting and rebuilding table", table_name)

    cur = con.cursor()
    cur.execute('DROP TABLE IF EXISTS {}'.format(table_name))
    
    if table_name == "cases":
        cur.execute('CREATE TABLE cases (id INTEGER PRIMARY KEY AUTOINCREMENT, commune TEXT NOT NULL, date TIMESTAMP NOT NULL, cases INTEGER NOT NULL)')

    elif table_name == "vacs":
        cur.execute("""CREATE TABLE vacs (id INTEGER PRIMARY KEY AUTOINCREMENT, age_group TEXT NOT NULL, date TIMESTAMP NOT NULL, \
                    vacs_1 INTEGER NOT NULL, cumulative_1 REAL NOT NULL, cumulative_percent_1 REAL NOT NULL, \
                    vacs_2 INTEGER NOT NULL, cumulative_2 REAL NOT NULL, cumulative_percent_2 REAL NOT NULL)""")

    elif table_name == "doses":
        # cur.execute("""CREATE TABLE doses (id INTEGER PRIMARY KEY AUTOINCREMENT, date TIMESTAMP NOT NULL, \
        #             doses_double INTEGER NOT NULL, cumulative_doses_double INTEGER NOT NULL,
        #             doses_single INTEGER NOT NULL, cumulative_doses_single INTEGER NOT NULL)""")
        cur.execute("""CREATE TABLE doses (id INTEGER PRIMARY KEY AUTOINCREMENT, date TIMESTAMP NOT NULL, \
                    cumulative_doses_double INTEGER, cumulative_doses_double_projected INTEGER, \
                    cumulative_doses_single INTEGER, cumulative_doses_single_projected INTEGER)""")


def close_db(con):
    print("Closing db connection")
    con.close()


def make_db():
    con = connect_db(DB_PATH)

    empty_table(con, "cases")
    populate_cases_table(con)

    empty_table(con, "vacs")
    populate_vacs_table(con)

    empty_table(con, "doses")
    populate_doses_table(con)

    close_db(con)











def get_cases_dict():
        
    url = ("https://epistat.sciensano.be/Data/COVID19BE_CASES_MUNI.json")
    response = urlopen(url)
    dict_list_all = json.loads(response.read().decode("utf-8")) #get list of dictionaries from json
    
    #initialise empty dictionaries e.g.
    #communes = {"Watermael-Boitsfort":[], "Auderghem":[], "Uccle":[]}
    #communes_cases = {"Watermael-Boitsfort":{"dates":[], "cases":[]}, "Auderghem":{"dates":[], "cases":[]}, "Uccle":{"dates":[], "cases":[]}}
    
    communes = {}
    communes_cases = {}
    for commune_name in COMMUNES:
        communes[commune_name] = []
        communes_cases[commune_name] = {"dates":[], "cases":[]}
    
    
    for dictionary in dict_list_all:
        if "TX_DESCR_FR" in dictionary: #search commune name
            if dictionary["TX_DESCR_FR"] in communes.keys():
                if "DATE" in dictionary.keys() and "CASES" in dictionary.keys(): #check both required fields are present
                    communes[dictionary["TX_DESCR_FR"]].append(dictionary)
                        
    for commune, commune_data in communes.items():
        for data in commune_data:
            communes_cases[commune]["dates"].append(datetime.strptime(data["DATE"], "%Y-%m-%d")) #convert date to datetime
            if data["CASES"] == "<5": #scrub non-integer values
                communes_cases[commune]["cases"].append(0)
            else:
                communes_cases[commune]["cases"].append(float(data["CASES"])/POPULATIONS[commune]*100000.) #cases per 100k population

    return communes_cases


def calculate_weekly_cases(commune_data):
    """for each commune, calculate weekly number of cases"""
    dates = commune_data["dates"]
    cases = commune_data["cases"]
    
    weekly_cases = [0]*7 #assume 0 at start
    for date_index in range(7, len(dates)):
        matching_cases = [cases[i]  for i, dt in enumerate(dates) if (dates[date_index] - timedelta(days=7)) < dt < dates[date_index]]
        weekly_cases.append(sum(matching_cases))

    commune_data["weekly_cases"] = weekly_cases
        
    return commune_data


def populate_cases_table(con):
    """add all cases data to sql database"""
    print("Populating cases table with data")

    communes_cases = get_cases_dict()
    
    for commune in COMMUNES:
        commune_data = communes_cases[commune]
        
        commune_data = calculate_weekly_cases(commune_data)

        cur = con.cursor()
        for date, cases in zip(commune_data["dates"], commune_data["weekly_cases"]):
            cur.execute('INSERT INTO cases (commune, date, cases) VALUES (?,?,?)', (commune, date, cases))
        con.commit()











def get_vacs_dict():
    url = ("https://epistat.sciensano.be/Data/COVID19BE_VACC.json")
    response = urlopen(url)
    dict_list_all = json.loads(response.read().decode("utf-8")) #get list of dictionaries from json
    
    
    vacs = {}
    vacs_data = {}
    for age_group in AGE_GROUPS:
        vacs[age_group] = []
        vacs_data[age_group] = {
            "dates_1":[], "vacs_1":[], "cumulative_1":[], "cumulative_percent_1":[],
            "dates_2":[], "vacs_2":[], "cumulative_2":[], "cumulative_percent_2":[]
        }
    
    
    
    for dictionary in dict_list_all:
        # if "AGEGROUP" in dictionary: #search commune name
        vacs[dictionary["AGEGROUP"]].append(dictionary)
            
    for age_group, age_group_data in vacs.items():
        for data in age_group_data:
            
            if data["DOSE"] == "A":
                vacs_data[age_group]["dates_1"].append(datetime.strptime(data["DATE"], "%Y-%m-%d")) #convert date to datetime
                vacs_data[age_group]["vacs_1"].append(data["COUNT"])
                vacs_data[age_group]["cumulative_1"].append(sum(vacs_data[age_group]["vacs_1"]))
                vacs_data[age_group]["cumulative_percent_1"].append(sum(vacs_data[age_group]["vacs_1"]) / POP_DIST[age_group] * 100.0)
    
            elif data["DOSE"] == "B":
                vacs_data[age_group]["dates_2"].append(datetime.strptime(data["DATE"], "%Y-%m-%d")) #convert date to datetime
                vacs_data[age_group]["vacs_2"].append(data["COUNT"])
                vacs_data[age_group]["cumulative_2"].append(sum(vacs_data[age_group]["vacs_2"]))
                vacs_data[age_group]["cumulative_percent_2"].append(sum(vacs_data[age_group]["vacs_2"]) / POP_DIST[age_group] * 100.0)

    return vacs_data




def sort_vacs_data(): 
    """sort vaccination data - sum up each day, and make cumulative and percentages"""

    vacs_data = get_vacs_dict()
    
    d1 = datetime(year=2020, month=12, day=28)
    d2 = datetime.now() - timedelta(days=1)
    
    dates = [d1 + timedelta(days=x) for x in range((d2-d1).days + 1)] #list of datetimes from start to now minus 1 day
    
    sorted_vacs_data = {i:{} for i in AGE_GROUPS}
    
    for age_group, age_group_data in sorted_vacs_data.items():
        age_group_data["dates"] = dates
        age_group_data["vacs_1"] = []
        age_group_data["cumulative_1"] = []
        age_group_data["cumulative_percent_1"] = []
        age_group_data["vacs_2"] = []
        age_group_data["cumulative_2"] = []
        age_group_data["cumulative_percent_2"] = []
    
        for date in dates:
            indices = np.where(vacs_data[age_group]["dates_1"] == np.datetime64(date))[0]
            sum_vacs = sum([v for i,v in enumerate(vacs_data[age_group]["vacs_1"]) if i in indices])
            age_group_data["vacs_1"].append(sum_vacs)
            age_group_data["cumulative_1"].append(sum(age_group_data["vacs_1"]))
            age_group_data["cumulative_percent_1"].append(sum(age_group_data["vacs_1"]) / POP_DIST[age_group] * 100.0)
        
            indices = np.where(vacs_data[age_group]["dates_2"] == np.datetime64(date))[0]
            sum_vacs = sum([v for i,v in enumerate(vacs_data[age_group]["vacs_2"]) if i in indices])
            age_group_data["vacs_2"].append(sum_vacs)
            age_group_data["cumulative_2"].append(sum(age_group_data["vacs_2"]))
            age_group_data["cumulative_percent_2"].append(sum(age_group_data["vacs_2"]) / POP_DIST[age_group] * 100.0)

    return sorted_vacs_data


def populate_vacs_table(con):
    """add all vacs data to sql database"""
    print("Populating vacs table with data")

    sorted_vacs_data = sort_vacs_data()
    keys = ['vacs_1', 'cumulative_1', 'cumulative_percent_1', 'vacs_2', 'cumulative_2', 'cumulative_percent_2']
    
    query_columns = "age_group, date, "+ ", ".join(keys)
    
    for age_group in AGE_GROUPS:
        vacs_data = sorted_vacs_data[age_group]
        
        
        cur = con.cursor()
        for i in range(len(vacs_data["dates"])):
            query = 'INSERT INTO vacs (' + query_columns + ') VALUES (?,?,?,?,?,?,?,?)'
            query_tuple = (age_group, vacs_data["dates"][i], *[vacs_data[j][i] for j in keys])
            cur.execute(query, query_tuple)
        con.commit()
 



def get_doses_dict():
    url = ("https://covid-vaccinatie.be/api/v1/delivered.json")
    response = urlopen(url)
    dict_list_all = json.loads(response.read().decode("utf-8"))["result"]["delivered"] #get list of dictionaries from json
    
    # with open(os.path.join(BASE_PATH, "delivered.json"), "r") as f:
    #     lines = f.readlines()[0]
    # dict_list_all = json.loads(lines)["result"]["delivered"]

    delivery_dates = [datetime.strptime(data["date"], "%Y-%m-%d") for data in dict_list_all]
    
    d1 = datetime(year=2020, month=12, day=28)
    d2 = datetime.now()
    
    dates = [d1 + timedelta(days=x) for x in range((d2-d1).days + 1)] #list of datetimes from start to now
    
    
    doses_dict = {}
    doses_dict["dates"] = dates
    doses_dict["doses_double"] = []
    doses_dict["cumulative_doses_double"] = []
    doses_dict["doses_single"] = []
    doses_dict["cumulative_doses_single"] = []
    
    for date in dates:
        indices = np.where(delivery_dates == np.datetime64(date))[0]

        sum_doses_double = sum([v["amount"] for i,v in enumerate(dict_list_all) if i in indices and v["manufacturer"]!="Johnson&Johnson"])
        doses_dict["doses_double"].append(sum_doses_double)
        doses_dict["cumulative_doses_double"].append(sum(doses_dict["doses_double"]))

        sum_doses_single = sum([v["amount"] for i,v in enumerate(dict_list_all) if i in indices and v["manufacturer"]=="Johnson&Johnson"])
        doses_dict["doses_single"].append(sum_doses_single)
        doses_dict["cumulative_doses_single"].append(sum(doses_dict["doses_single"]))
    
    return doses_dict


def project_doses(doses_dict):
    
    n_days_to_fit = 56
    n_days_to_project = 56
    
    n_dates = len(doses_dict["dates"])
    
    x_fit = range(n_days_to_fit)
    x_proj = range(n_days_to_fit + n_days_to_project)

    d1 = doses_dict["dates"][0]
    d2 = doses_dict["dates"][-1] + timedelta(days=n_days_to_project)
    dates_new = [d1 + timedelta(days=x) for x in range((d2-d1).days + 1)] #list of datetimes from start to now + projection days




    
    doses_double = doses_dict["cumulative_doses_double"][(-1*n_days_to_fit):]
    polyfit_double = np.polyfit(x_fit, doses_double, 2)
    polyval_double = np.polyval(polyfit_double, x_proj)
    
    doses_proj_double = np.zeros(len(dates_new)) * np.nan
    doses_proj_double[(n_dates - n_days_to_fit):(n_dates + n_days_to_project)] = polyval_double
    
    doses_new_double = np.zeros(len(dates_new)) * np.nan
    doses_new_double[:n_dates] = doses_dict["cumulative_doses_double"]
    
    
    doses_dict["dates_projected"] = dates_new
    doses_dict["cumulative_doses_double_new"] = doses_new_double
    doses_dict["cumulative_doses_double_projected"] = doses_proj_double




    doses_single = doses_dict["cumulative_doses_single"][(-1*n_days_to_fit):]
    polyfit_single = np.polyfit(x_fit, doses_single, 2)
    polyval_single = np.polyval(polyfit_single, x_proj)
    
    doses_proj_single = np.zeros(len(dates_new)) * np.nan
    doses_proj_single[(n_dates - n_days_to_fit):(n_dates + n_days_to_project)] = polyval_single
    
    doses_new_single = np.zeros(len(dates_new)) * np.nan
    doses_new_single[:n_dates] = doses_dict["cumulative_doses_single"]
    
    
    doses_dict["dates_projected"] = dates_new
    doses_dict["cumulative_doses_single_new"] = doses_new_single
    doses_dict["cumulative_doses_single_projected"] = doses_proj_single

    return doses_dict
    

def populate_doses_table(con):
    """add all delivered doses data to sql database"""
    print("Populating doses table with data")

    doses_dict = get_doses_dict()
    doses_dict = project_doses(doses_dict)
    
    cur = con.cursor()
    # for date, doses_double, cum_double, doses_single, cum_single in \
    #     zip(doses_dict["dates"], doses_dict["doses_double"], doses_dict["cumulative_doses_double"], \
    #         doses_dict["doses_single"], doses_dict["cumulative_doses_single"]):
            
    #     cur.execute('INSERT INTO doses (date, doses_double, cumulative_doses_double, doses_single, cumulative_doses_single) VALUES (?,?,?,?,?)', \
    #                 (date, doses_double, cum_double, doses_single, cum_single))

    for date, cum_double, cum_double_proj, cum_single, cum_single_proj,  in \
        zip(doses_dict["dates_projected"], \
            doses_dict["cumulative_doses_double_new"], \
            doses_dict["cumulative_doses_double_projected"], \
            doses_dict["cumulative_doses_single_new"], \
            doses_dict["cumulative_doses_single_projected"]):
            
        cur.execute('INSERT INTO doses (date, cumulative_doses_double, cumulative_doses_double_projected, \
                    cumulative_doses_single, cumulative_doses_single_projected) VALUES (?,?,?,?,?)', \
                    (date, cum_double, cum_double_proj, cum_single, cum_single_proj))

    con.commit()



