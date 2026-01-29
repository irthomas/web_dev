# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 14:49:32 2022

@author: iant

DB FUNCTIONS
"""



import sqlite3
import re
import os
import json

from config import SHARED_DIR_PATH
from config import JSON_TEMPLATE_PATH, JSON_TEMPLATE_DIR

    
    
def connect_db(db_path):
    print("Connecting to database %s" %db_path)
    con = sqlite3.connect(db_path)
    return con

def close_db(con):
    con.close()


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


def get_order_obs(plot_orders=None):
    
    level = "hdf5_level_1p0a"
    regex = re.compile("(....)(..).._......_1p0a_SO_._(?:\w_(\d*)|\w)\.h5")

    
    
    channels, filepaths = get_filenames_from_cache(level)
    
    filenames = [os.path.basename(f) for c,f in zip(channels, filepaths) if c == "SO"]
    
    regexes = [re.findall(regex, f)[0] for f in filenames if re.findall(regex, f)]
    filenames_split = [[int(i) for i in s] for s in regexes if s[2]]
    end_year = max([s[0] for s in filenames_split]) + 1
    
    max_n = 0
    
    #split by order, then by year-month
    
    if not plot_orders:
        unique_orders = sorted(list(set([s[2] for s in filenames_split])))
    else:
        unique_orders = plot_orders
    
    # labels = []
    # for year in range(2018, 2022):
    #     for month in range(1, 13):
    #         # print(month, year)
    #         labels.append("%02i/%04i" %(month, year))
    
    order_dict = {}
    for unique_order in unique_orders:
        
        order_dict[unique_order] = []
    
        for year in range(2018, end_year):
            for month in range(1, 13):
                # print(month, year)

                # label = "%02i/%04i" %(month, year)
                label = "%04i-%02i" %(year, month)

                #find all files matching month and year
                orders = [1 for s in filenames_split if s[0] == year and s[1] == month and s[2] == unique_order]
                n = sum(orders)
                
                #find maximum value
                if n > max_n:
                    max_n = n
                
                order_dict[unique_order].append({"label":label, "n":n}) #for each order, make a list of dictionaries
                
                
    return order_dict, max_n




def make_json(plot_orders=None):
    
    with open(JSON_TEMPLATE_PATH, "r") as f:
        template = json.load(f)
        
    order_dict, max_n = get_order_obs(plot_orders=plot_orders)
    orders = list(order_dict.keys())

    for plot_order in orders:
        
        template["title"] = "Order %i" %plot_order
        template["data"]["values"] = order_dict[plot_order]
        
        template["encoding"]["color"]["scale"]["domain"][1] = max_n
        template["encoding"]["y"]["scale"]["domain"][1] = max_n
        
        jdata = json.dumps(template, indent=4)
    
        with open(os.path.join(JSON_TEMPLATE_DIR, "nomad_order_%i.json" %plot_order), "w") as f:
            f.write(jdata)

    with open(os.path.join(JSON_TEMPLATE_DIR, "orders.txt"), "w") as f:
        for order in orders:
            f.write(str(order)+"\n")


