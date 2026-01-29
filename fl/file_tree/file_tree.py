# -*- coding: utf-8 -*-
"""
Created on Wed May 12 16:46:49 2021

@author: iant

GET OBS TYPE DB, CLICK ON EACH OBS TO FIND OUT MORE INFO E.G. COP ROW.

COMPARE TO DB OF ACTUAL 0.1A FILES TO CHECK IF FILE EXISTS


"""
import os
from datetime import datetime

from views import make_obs_type_table, get_single_obs_table, make_missing_txt
from config import UPLOAD_PATH

from flask import Flask, request, render_template, send_file
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_PATH


@app.route('/', methods=["GET", "POST"])
def make_index_page():

    file_type = request.args.get("type", default="all_files", type=str)

    dt_str_s = request.args.get("utc_start", default="2010-01-01", type=str)
    dt_str_e = request.args.get("utc_end", default="2040-01-01", type=str)

    
    dt_s = datetime.strptime(dt_str_s, "%Y-%m-%d")
    dt_e = datetime.strptime(dt_str_e, "%Y-%m-%d")
    
    search_params = {"utc_start_time_s":dt_s, "utc_start_time_e":dt_e, "file_type":file_type}

    obs_type_table = make_obs_type_table(search_params)
    

    return render_template("index.html", obs_type_table=obs_type_table)



@app.route('/info', methods=["GET", "POST"])
def obs_type_info():
    """get info frame for one observation"""
    
    i = -1
    if request.method == "GET":
                
        i = request.args.get("i", default=-1, type=int)
        
        return get_single_obs_table(i)




@app.route('/download', methods=["GET", "POST"])
def download_missing():
    """make a text file containing info for all missing files and download"""

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], "missing.txt")


    
    dt_s = datetime.strptime("2010-01-01", "%Y-%m-%d")
    dt_e = datetime.strptime("2040-01-01", "%Y-%m-%d")
    
    search_params = {"utc_start_time_s":dt_s, "utc_start_time_e":dt_e, "file_type":"missing_files"}

    #write to file in upload folder    
    make_missing_txt(search_params, filepath)

    #serve file in upload folder    
    return send_file(filepath, as_attachment=True)







if __name__ == '__main__':
    app.run(debug=False)




