# -*- coding: utf-8 -*-
"""
Created on Thu May 13 16:59:13 2021

@author: iant
"""


import sqlite3 as sql
from datetime import datetime
import os
import re

from config import LOCAL_DB_PATH
from config import COLUMN_NAMES

# INVALID_OBS_TYPE_LETTERS = {
#     ("LNO", "N"):"LNO nightside nadir not yet calibrated", 
#     ("LNO", "O"):"LNO nightside limb not yet calibrated",
#     ("LNO", "L"):"LNO dayside limb not yet calibrated",
#     ("LNO", "P"):"LNO Phobos not yet calibrated",
#     ("LNO", "Q"):"LNO Deimos not yet calibrated",

#     ("UVIS", "P"):"UVIS Phobos not yet calibrated",
#     ("UVIS", "Q"):"UVIS Deimos not yet calibrated",
# }


def get_obs_type_dict(search_params):
    """get a limited range of info from db to fill left table"""
    con = sql.connect(os.path.join(LOCAL_DB_PATH, "file_tree.db"))
    con.row_factory = sql.Row
       
    cur = con.cursor()
    # cur.execute('SELECT * FROM tree')

    cur.execute('SELECT * FROM tree WHERE itl_dt BETWEEN ? AND ?', \
        [
            search_params["utc_start_time_s"], 
            search_params["utc_start_time_e"],
        ])
       
    rows = cur.fetchall()
    con.close()
    
    dictionary_list = []
    for row in rows:
        row_date = datetime.strptime(row["itl_dt"], "%Y-%m-%d %H:%M:%S")
        
        #get filename prefix
        h5_prefix = row["hdf5_level_0p1a"][0:15]
        
        dictionary = {"id":row["id"], "itl_dt":row_date, "obs_type":row["obs_type"], "channel":row["channel"], \
                      "h5_prefix":h5_prefix, "hdf5_level_0p2a":row["hdf5_level_0p2a"], "hdf5_level_1p0a":row["hdf5_level_1p0a"]}
        dictionary_list.append(dictionary)

    return dictionary_list





def make_obs_type_table(search_params):
    print("Loading data")
    obs_type_dict_list = get_obs_type_dict(search_params)
    
    h5_execdt_reasons = load_missing_log_file()
    
    h = ""
    h += "<table>\n"
    h += "<tr><th>Execution Time (from ITL)</th> <th>Observation Type</th> <th>Channel</th> <th>Reason for Missing File</th> </tr>\n"
    
    print("Making table")
    
    for obs_type_dict in obs_type_dict_list:
        idx = obs_type_dict["id"]
        itl_dt = obs_type_dict["itl_dt"]
        obs_type = obs_type_dict["obs_type"]
        channel = obs_type_dict["channel"]
        
        # l0p2a = obs_type_dict["hdf5_level_0p2a"]
        # last_level = obs_type_dict["hdf5_level_1p0a"]
        
        #get reason for file missing from text file
        if (itl_dt, channel) in h5_execdt_reasons.keys():
            reason = h5_execdt_reasons[(itl_dt, channel)]
        else:
            reason = ""
        
        #find the colour of the row, default = black unless files missing
        # colour = "#000000"
        
        # if l0p2a == "NULL":
        #     obs_type_letter = ""
        # else:
        #     obs_type_letter = re.match("\d*_\d*_\dp\d[a-z]_[A-Z]*_(?:\d_|)([A-Z]*)(?:_\d*|).h5", l0p2a)[1]
        
        # if last_level == "NULL":
        #     if (channel, obs_type_letter) in INVALID_OBS_TYPE_LETTERS:
        #         colour = "#00FF00"
        #     else:
        #         colour = "#FF0000"
        
        if reason == "":
            colour = "#000000"
            
        elif reason == "Unknown":
            colour = "#DD0000"
            
        else:
            colour = "#00DD00"

        
        #display all / missing / failed files only
        if "file_type" in search_params.keys():

            if search_params["file_type"] == "all_files":
        
                h += f"""<tr onclick='display_obs_info({idx})'>
                    <td><font color='{colour}'>{itl_dt}</font></td>
                    <td><font  color='{colour}'>{obs_type}</font></td>
                    <td><font  color='{colour}'>{channel}</font></td>
                    <td><font  color='{colour}'>{reason}</font></td>
                    </tr>\n"""

            elif search_params["file_type"] == "missing_files":
        
                if colour != "#000000":
                    h += f"""<tr onclick='display_obs_info({idx})'>
                        <td><font color='{colour}'>{itl_dt}</font></td>
                        <td><font  color='{colour}'>{obs_type}</font></td>
                        <td><font  color='{colour}'>{channel}</font></td>
                        <td><font  color='{colour}'>{reason}</font></td>
                        </tr>\n"""

            elif search_params["file_type"] == "failed_files":
        
                if colour == "#DD0000":
                    h += f"""<tr onclick='display_obs_info({idx})'>
                        <td><font color='{colour}'>{itl_dt}</font></td>
                        <td><font  color='{colour}'>{obs_type}</font></td>
                        <td><font  color='{colour}'>{channel}</font></td>
                        <td><font  color='{colour}'>{reason}</font></td>
                        </tr>\n"""

        else: #if nothing given, output all
            h += f"""<tr onclick='display_obs_info({idx})'>
                <td><font color='{colour}'>{itl_dt}</font></td>
                <td><font  color='{colour}'>{obs_type}</font></td>
                <td><font  color='{colour}'>{channel}</font></td>
                <td><font  color='{colour}'>{reason}</font></td>
                </tr>\n"""
                
        
    h += "</table>\n"
    
    return h




def get_single_obs_dict(i):
    con = sql.connect(os.path.join(LOCAL_DB_PATH, "file_tree.db"))
    con.row_factory = sql.Row
       
    cur = con.cursor()
    cur.execute('SELECT * FROM tree WHERE id = ?', (i,)) #sql starts at id=1
       
    rows = cur.fetchall()
    con.close()
    
    dictionary_list = []
    for row in rows:
        row_date = datetime.strptime(row["itl_dt"], "%Y-%m-%d %H:%M:%S")
        dictionary = {"itl_dt":row_date}
        for column_name in COLUMN_NAMES:
            if column_name not in dictionary.keys():
                if row[column_name] == "NULL":
                    dictionary[column_name] = ""
                else:
                    dictionary[column_name] = row[column_name]
                

        dictionary_list.append(dictionary)

    if len(dictionary_list) == 1:
        return dictionary_list[0]
    else:
        print("Error: Multiple matching rows found")
        return {}



def get_single_obs_table(i):
    single_obs_dict = get_single_obs_dict(i)
    
    h = ""
    h += "<table>\n"
    
    for column_name in COLUMN_NAMES:
        
        info = single_obs_dict[column_name]
        if type(info) == str:
            info = info.replace("\n", "<br>")    
        
        
        new_column_names = {
            "itl_dt":"Execution Time (from ITL)", 
            "orbit":"TGO Orbit Number", 
            "obs_type":"Observation Type",
            "channel":"Channel"
        }
        if column_name in new_column_names.keys():
            column_name = new_column_names[column_name]
        
        h += f"<tr><td>{column_name}</td> <td>{info}</td> </tr>\n"
        
        
    h += "</table>\n"
    
    return h




def make_missing_txt(search_params, filepath):
    """make a text file containing info for all missing files"""
    
    obs_type_dict_list = get_obs_type_dict(search_params)
    
    h5_prefixes = []
    for obs_type_dict in obs_type_dict_list:
        itl_dt = obs_type_dict["itl_dt"]
        obs_type = obs_type_dict["obs_type"]
        channel = obs_type_dict["channel"]
        h5_prefix = obs_type_dict["h5_prefix"]
        
        last_level = obs_type_dict["hdf5_level_1p0a"]
        
        #if h5 missing from level 1.0a, add to list
        if last_level == "NULL":
            h5_prefixes.append("%s, %s, %s, %s" %(itl_dt, obs_type, channel, h5_prefix))
    

    #write to file in upload folder    
    with open(filepath, "w") as f:
        for h5_prefix in h5_prefixes:
            f.write("%s\n" %h5_prefix)



def load_missing_log_file():
    
    filepath = os.path.join(LOCAL_DB_PATH, "missing_file_log.txt")
    
    with open(filepath, "r") as f:
        missing_file_outputs = f.readlines()

    h5_execdt_reasons = {}
    # h5_prefix_reasons = {}
    for missing_file_output in missing_file_outputs:
        h5_exectime, h5_obstype, h5_channel, h5_prefix, h5_highest_level, h5, reason = missing_file_output.split(",")
        
        h5_dt = datetime.strptime(h5_exectime, "%Y-%m-%d %H:%M:%S")
        reason = reason.strip()
        
        h5_execdt_reasons[(h5_dt, h5_channel)] = reason
        # h5_prefix_reasons[(h5_prefix, h5_channel)] = reason
    
    return h5_execdt_reasons#, h5_prefix_reasons