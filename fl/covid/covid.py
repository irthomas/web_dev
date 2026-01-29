# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 22:24:20 2021

@author: iant

READ DATABASE, GET DATA
"""



# from db_config import DB_PATH, JSON_TEMPLATE_PATH
# import json
# import sqlite3 as sql
from flask import Flask, render_template, request
from calculations import make_html_calculations

# from datetime import datetime
app = Flask(__name__, static_url_path='/static')
    

@app.route('/cases.json')
def cases_json():
    return render_template("cases.json")

@app.route('/vacs.json')
def vacs_json():
    return render_template("vacs.json")

@app.route('/doses.json')
def doses_json():
    return render_template("doses.json")


        
@app.route('/', methods=["GET", "POST"])
def make_html():
    
    if request.method == "GET":
                
        delay = request.args.get("delay", default=35, type=int)
        take_up_rate = request.args.get("take_up_rate", default=80, type=int)
        
    return render_template("covid.html", calculations=make_html_calculations(delay, take_up_rate))


if __name__ == '__main__':
    app.run(debug=False)
    
    
