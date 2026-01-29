# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 22:24:20 2021

@author: iant

READ DATABASE, GET DATA
"""



from config import JSON_TEMPLATE_PATH
from flask import Flask, render_template
import json
from datetime import datetime, timedelta
import time
import requests
app = Flask(__name__, static_url_path='/static')
    

SPICE_DT_FORMAT = "%Y-%m-%dT%H:%M:%S"

SPICE_SERVER = "http://spice.esac.esa.int"
KERNEL_SET_ID = 2

# SPICE_SERVER = "https://wgc2.jpl.nasa.gov:8443"
# KERNEL_SET_ID = 11

def new_calculation(post_dict):
    new_calc_url = "%s/webgeocalc/api/calculation/new" %SPICE_SERVER
    
    r = requests.post(new_calc_url, json=post_dict)
    new_calc_response = r.json()
    calculation_id = new_calc_response["calculationId"]
    print(calculation_id)
    return calculation_id


def get_response(post_dict):
    calculation_id = new_calculation(post_dict)
    time.sleep(2)

    results_url = "%s/webgeocalc/api/calculation/%s/results" %(SPICE_SERVER, calculation_id)
    # print(results_url)
    r = requests.get(results_url)
    response = r.json()

    print(response["status"])
    if response["status"] == "OK":
        return response["columns"], response["rows"]
    else:
        print(response)


def get_info(info_type):
    
    if info_type == "kernels":
        url = "%s/webgeocalc/api/kernel-sets" %SPICE_SERVER
    elif info_type == "bodies":
        url = "%s/webgeocalc/api/kernel-set/%s/bodies" %(SPICE_SERVER, KERNEL_SET_ID)
    elif info_type == "frames":
        url = "%s/webgeocalc/api/kernel-set/%s/frames" %(SPICE_SERVER, KERNEL_SET_ID)
    elif info_type == "instruments":
        url = "%s/webgeocalc/api/kernel-set/%s/instruments" %(SPICE_SERVER, KERNEL_SET_ID)
    
    r = requests.get(url)
    response = r.json()
    return response
        
    

def sub_obs_post(times):
    
    post_dict = {

      "kernels": [
        {
          "type": "KERNEL_SET",
          "id": KERNEL_SET_ID
        }
      ],
    
      "timeSystem": "UTC",
      "timeFormat": "CALENDAR",
      "times": times,
      "timeStep": 1,
      "timeStepUnits": "SECONDS",
    
      "calculationType": "SUB_OBSERVER_POINT",
      "target": "MARS",
      "targetFrame": "IAU_MARS",
      "observer": "-143",
      "subPointType": "Near point: ellipsoid",
      "aberrationCorrection": "NONE",
      "stateRepresentation": "LATITUDINAL"
    
    }
    return post_dict


def get_sub_obs_lat_lon(times):
    
    post_dict = sub_obs_post(times)
    rows = get_response(post_dict)[1]
    
    lons = [row[1] for row in rows]
    lats = [row[2] for row in rows]
    
    return lons, lats

# kernels = get_info("kernels")
# bodies = get_info("bodies")
# frames = get_info("frames")
# instruments = get_info("instruments")

# lons, lats = get_sub_obs_lat_lon("2019-10-19T08:24:00.000")


def make_lon_lat_dict_list():
    now = datetime.now()
    datetime_strings = [datetime.strftime(now - timedelta(minutes=minute_delta), SPICE_DT_FORMAT) for minute_delta in range(-4, 5)]
    lons, lats = get_sub_obs_lat_lon(datetime_strings)
    dictionary_list = [{"lon":lon, "lat":lat, "label":"", "colour":i, "datetime":dt} for i, (lon, lat, dt) in enumerate(zip(lons, lats, datetime_strings))]
    dictionary_list[4]["label"] = "ExoMars Trace Gas Orbiter"
    return dictionary_list

    
@app.route('/')
def make_html():
    return render_template("tgo_tracker.html")



@app.route('/tgo_tracker.json')
def make_json():
    
    with open(JSON_TEMPLATE_PATH, "r") as f:
        template = json.load(f)
        
    dictionary_list = make_lon_lat_dict_list()

    template["data"]["values"] = dictionary_list
    jdata = json.dumps(template, indent=4)
    
    # con.close()
    return jdata

if __name__ == '__main__':
    app.run(debug=True)
    
    
