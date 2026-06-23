# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 13:13:00 2021

@author: iant

READ IN POWER FROM SMART METER AND DISPLAY IN ONLINE CHART




"""


from db_functions import get_db_rows, dict_refs, get_pv_for_day
from db_functions_tuya import DICT_REFS, get_plugs_for_day
from views import vega_head, vega_embed
from flask import Flask#, request, render_template
app = Flask(__name__)

import altair as alt
import numpy as np
import pandas as pd

from datetime import datetime, timedelta, timezone

MAX_POINTS_PV = 2490
MAX_POINTS_PLUGS = 1240

@app.route('/table/')
def make_pvpower_table():
    

    rows = get_db_rows("sg")
    
    

    h = '<html><head>\n'

    h += '<title>Home Power</title>\n'
    h += '<link rel="stylesheet" type="text/css" href="/static/assets/css/style.css"/>\n'
    h += '<link rel="shortcut icon" type="image/png" href="/static/assets/favicon.ico"/>\n'


    h += '<style>\n'
    h += 'table {\n'
    h += '  font-family: arial, sans-serif;\n'
    h += '  border-collapse: collapse;\n'
    h += '  width: 100%;\n'
    h += '}\n'

    h += 'td, th {\n'
    h += '  border: 1px solid #dddddd;\n'
    # h += '  text-align: center;\n'
    h += '  padding: 8px;\n'
    h += '}\n'
    h += '</style>\n'
    
    # h += '<style>tr:nth-of-type(odd){background-color:#ccc;}</style>\n'
    h += '</head><body>\n'
    h += '<table>\n'

    h += '<tr>'
    for table_header in ["Row ID", "UTC time"] + list(dict_refs.keys()):
        h += '<th>%s</th>\n' %table_header
    h += '</tr>'

    for row in rows:
        h += '<tr>\n'
        for element in row:
            if isinstance(element, str):
                h += '<td>%s</td>' %element
            else:                
                h += '<td>%0.3f</td>' %element
    h += '</tr>\n'
    h += "</body></html>"

    return h


@app.route('/')
def today_plot():
    
    dt = datetime.now() #replace by today
    
    data_d = get_pv_for_day(dt)
    
    data_d["PowerReturned_total"] = np.asarray(data_d["PowerReturned_total"], dtype=float)
    data_d["PowerDelivered_total"] = -np.asarray(data_d["PowerDelivered_total"], dtype=float)
    # data_d["Utc"] = list(range(len(data_d["Utc"])))
    
    data_d["Utc"] = [datetime.strptime(dt, "%Y-%m-%d %H:%M:%S.%f").replace(tzinfo=timezone.utc).astimezone(tz=None) for dt in data_d["Utc"]]
    
    
    #rename datasets
    new_keys = ["Time", "Power from Grid", "Power to Grid"]
    for key, new_key in zip(data_d.keys(), new_keys):
        data_d[new_key] = data_d.pop(key) 
    
    
    
    #if more than 5000 entries, need to interpolate
    if len(data_d["Time"]) > MAX_POINTS_PV:
        seconds = [(dt - data_d["Time"][0]).total_seconds() for dt in data_d["Time"]]
        seconds_interp = np.linspace(seconds[0], seconds[-1], num=MAX_POINTS_PV)
        p_ret = np.interp(seconds_interp, seconds, data_d["Power to Grid"])
        p_del = np.interp(seconds_interp, seconds, data_d["Power from Grid"])
        
        utc_interp = [data_d["Time"][0] + timedelta(seconds=i) for i in seconds_interp]
        
        data_d["Power to Grid"] = p_ret
        data_d["Power from Grid"] = p_del
        data_d["Time"] = utc_interp



    
    x_name = "Time"; x_spec = "Time:T"
    # x_name = "index"; x_spec = "index:Q"
    
    df = pd.DataFrame(data=data_d).melt(x_name, var_name="Power", value_name="Watts")


    # # Create a selection that chooses the nearest point & selects based on x-value
    # nearest = alt.selection_point(nearest=True, on='mouseover',
    #                         fields=[x_name], empty=False)
    
    chart = alt.Chart(df).mark_line(interpolate='basis').encode(
        x=x_spec,  # specify nominal data
        y='Watts:Q',  # specify quantitative data
        color='Power:N',  # specify quantitative data
    ).properties(
    width=800,
    height=400
    )   

    # # Transparent selectors across the chart. This is what tells us
    # # the x-value of the cursor
    # selectors = alt.Chart(df).mark_point().encode(
    #     x=x_spec,
    #     opacity=alt.value(0),
    # ).add_params(
    #     nearest
    # )
    
    # # Draw points on the line, and highlight based on selection
    # points = chart.mark_point().encode(
    #     opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    # )
    
    # # Draw text labels near the points, and highlight based on selection
    # text = chart.mark_text(align='left', dx=5, dy=-5).encode(
    #     text=alt.condition(nearest, 'Watts:Q', alt.value(' '))
    # )
    
    # # Draw a rule at the location of the selection
    # rules = alt.Chart(df).mark_rule(color='gray').encode(
    #     x=x_spec,
    # ).transform_filter(
    #     nearest
    # )
    
    # # Put the five layers into a chart and bind the data
    # alt.layer(
    #     chart, selectors, points, rules, text
    # ).properties(
    #     width=1200, height=500
    # )

    json = chart.to_json()
    
    h = """<!DOCTYPE html>
        <html>
        <head>
        %s
        </head>
        <body>
        %s
        </body>
        </html>""" %(vega_head(), vega_embed(json))
    return h

@app.route('/plugs/')
def today_plot_tuya():
    
    dt = datetime.now() #replace by today
    
    data_d = get_plugs_for_day(dt)

    for key in DICT_REFS.keys():
        data_d[key] = np.asarray(data_d[key], dtype=float)
    
    data_d["Time"] = [datetime.strptime(dt, "%Y-%m-%d %H:%M:%S.%f").replace(tzinfo=timezone.utc).astimezone(tz=None) for dt in data_d["Utc"]]
    
    data_d.pop("Utc")
    #rename datasets
    # new_keys = ["Time", "Dishwasher", "Washing_machine", "Fridge_and_freezer"]
    # for key, new_key in zip(data_d.keys(), new_keys):
    #     data_d[new_key] = data_d.pop(key) 
   
    
    #if more than 5000 entries, need to interpolate
    if len(data_d["Time"]) > MAX_POINTS_PLUGS:
        seconds = [(dt - data_d["Time"][0]).total_seconds() for dt in data_d["Time"]]
        seconds_interp = np.linspace(seconds[0], seconds[-1], num=MAX_POINTS_PLUGS)
        
        for key in DICT_REFS.keys():
            data_d[key] = np.interp(seconds_interp, seconds, data_d[key])
        data_d["Time"] = [data_d["Time"][0] + timedelta(seconds=i) for i in seconds_interp]
        
    
    x_name = "Time"; x_spec = "Time:T"
    # x_name = "index"; x_spec = "index:Q"
    
    df = pd.DataFrame(data=data_d).melt(x_name, var_name="Power", value_name="Watts")


    # # Create a selection that chooses the nearest point & selects based on x-value
    # nearest = alt.selection_point(nearest=True, on='mouseover',
    #                         fields=[x_name], empty=False)
    
    chart = alt.Chart(df).mark_line(interpolate='basis').encode(
        x=x_spec,  # specify nominal data
        y='Watts:Q',  # specify quantitative data
        color='Power:N',  # specify quantitative data
    ).properties(
    width=800,
    height=400
    )   

    # # Transparent selectors across the chart. This is what tells us
    # # the x-value of the cursor
    # selectors = alt.Chart(df).mark_point().encode(
    #     x=x_spec,
    #     opacity=alt.value(0),
    # ).add_params(
    #     nearest
    # )
    
    # # Draw points on the line, and highlight based on selection
    # points = chart.mark_point().encode(
    #     opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    # )
    
    # # Draw text labels near the points, and highlight based on selection
    # text = chart.mark_text(align='left', dx=5, dy=-5).encode(
    #     text=alt.condition(nearest, 'Watts:Q', alt.value(' '))
    # )
    
    # # Draw a rule at the location of the selection
    # rules = alt.Chart(df).mark_rule(color='gray').encode(
    #     x=x_spec,
    # ).transform_filter(
    #     nearest
    # )
    
    # # Put the five layers into a chart and bind the data
    # alt.layer(
    #     chart, selectors, points, rules, text
    # ).properties(
    #     width=1200, height=500
    # )

    json = chart.to_json()
    
    h = """<!DOCTYPE html>
        <html>
        <head>
        %s
        </head>
        <body>
        %s
        </body>
        </html>""" %(vega_head(), vega_embed(json))
    return h



if __name__ == '__main__':
    app.run(debug=True)




