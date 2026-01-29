# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 13:13:00 2021

@author: iant

READ IN OBS PLANNING DATA FROM SQLITE DB




"""

# import sqlite3
# import re
# import posixpath
# import sys
from datetime import datetime

from db_functions import search_db
from flask import Flask, request, render_template
app = Flask(__name__)


occultation_table_headers = [
    "SQL Obs Id",
    "Prime Instrument",
    "Orbit Number",
    "MTP Number",
    "Occultation Type",
    "UTC Start Time",
    "UTC Transition Time",
    "UTC End Time",
    "Duration (s)",
    "Start Lon",
    "Transition Lon",
    "End Lon",
    "Start Lat",
    "Transition Lat",
    "End Lat",
    "Transition Local Time (hrs)",
    "Orbit Type",
    "IR Observation Name",
    "IR Description",
    "UVIS Description",
    "Orbit Comment",
]


nadir_table_headers = [
    "SQL Obs Id",
    "Orbit Number",
    "MTP Number",
    "Nadir Type",
    "UTC Start Time",
    "UTC Centre Time",
    "UTC End Time",
    "Duration (s)",
    "Start Lon",
    "Centre Lon",
    "End Lon",
    "Start Lat",
    "Centre Lat",
    "End Lat",
    "Centre Incidence Angle",
    "Centre Local Time (hrs)",
    "Orbit Type",
    "IR Observation Name",
    "IR Description",
    "UVIS Description",
    "Orbit Comment", 
]


@app.route('/')
def make_index_page():
    
    return render_template("index.html")


    
@app.route('/occultations', methods=["GET", "POST"])
def make_occultation_page():

    dt_str_s = request.args.get("utc_start", default="2010-01-01", type=str)
    dt_str_e = request.args.get("utc_end", default="2040-01-01", type=str)

    mtp_s = request.args.get("mtp_start", default=0, type=int)
    mtp_e = request.args.get("mtp_end", default=999, type=int)

    
    
    dt_s = datetime.strptime(dt_str_s, "%Y-%m-%d")
    dt_e = datetime.strptime(dt_str_e, "%Y-%m-%d")
    


    search_params = {"utc_start_time_s":dt_s, "utc_start_time_e":dt_e, "mtp_s":mtp_s, "mtp_e":mtp_e}


    rows = search_db("occultations", search_params)
    
    

    h = '<html><head>'
    
    h += '<style>tr:nth-of-type(odd){background-color:#ccc;}</style>\n'
    h += '</head><body>\n'
    h += '<table style="width:300%">\n'

    h += '<tr>'
    for table_header in occultation_table_headers:
        h += '<th>%s</th>\n' %table_header
    h += '</tr>'

    for row in rows:
        h += '<tr>\n'
        for element in row:
            if element == datetime(year=2000, month=1, day=1):
                element = "-"
            h += '<td>%s</td>' %element
    h += '</tr>\n'
    h += "</body></html>"

    return h




@app.route('/nadirs', methods=["GET", "POST"])
def make_nadir_page():

    dt_str_s = request.args.get("utc_start", default="2010-01-01", type=str)
    dt_str_e = request.args.get("utc_end", default="2040-01-01", type=str)

    mtp_s = request.args.get("mtp_start", default=0, type=int)
    mtp_e = request.args.get("mtp_end", default=999, type=int)

    
    
    dt_s = datetime.strptime(dt_str_s, "%Y-%m-%d")
    dt_e = datetime.strptime(dt_str_e, "%Y-%m-%d")
    


    search_params = {"utc_start_time_s":dt_s, "utc_start_time_e":dt_e, "mtp_s":mtp_s, "mtp_e":mtp_e}


    rows = search_db("nadirs", search_params)
    
    

    h = '<html><head>'
    
    h += '<style>tr:nth-of-type(odd){background-color:#ccc;}</style>\n'
    h += '</head><body>\n'
    h += '<table style="width:300%">\n'

    h += '<tr>'
    for table_header in nadir_table_headers:
        h += '<th>%s</th>\n' %table_header
    h += '</tr>'

    for row in rows:
        h += '<tr>\n'
        for element in row:
            if element == "2000-01-01 00:00:00":
                element = "-"
            h += '<td>%s</td>' %element
    h += '</tr>\n'
    h += "</body></html>"

    return h






if __name__ == '__main__':
    app.run(debug=False)




