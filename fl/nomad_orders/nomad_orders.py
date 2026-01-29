# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 14:49:32 2022

@author: iant

READ IN OBS PLANNING DATA FROM SQLITE DB




"""

# import sqlite3
import os
# import re
# import json
# import posixpath
# import sys
# from datetime import datetime

from db_functions import make_json
from config import JSON_TEMPLATE_DIR

from flask import Flask, request, render_template
app = Flask(__name__)



# make_json(plot_orders=[119, 121, 134, 136])

# make_json()

#get list of orders
plot_orders = []
with open(os.path.join(JSON_TEMPLATE_DIR, "orders.txt"), "r") as f:
    for line in f.readlines():
        plot_orders.append(int(line))


@app.route('/')
def make_index_page():
    
    
    h = '<!DOCTYPE html><html><head>\n'
    h += '<script src="https://cdn.jsdelivr.net/npm/vega@5"></script>\n'
    h += '<script src="https://cdn.jsdelivr.net/npm/vega-lite@4"></script>\n'
    h += '<script src="https://cdn.jsdelivr.net/npm/vega-embed@6"></script>\n'
    h += '<link href="/static/assets/css/style.css" rel="stylesheet">\n'
    h += '</head>\n'
    
    h += '<body>\n'
    h += '<h1>NOMAD SO</h1>\n'
    h += '<h2>Number of observations per diffraction order</h2>\n'
    
    for order in plot_orders:
        h += '<div id="vis%i"></div><br>\n' %order
          
        h += '  <script>\n'
        h += '    const spec%i = "nomad_orders.json?order=%s";\n' %(order, order)
        h += '  	vegaEmbed("#vis%i", spec%i)\n' %(order, order)
        h += '      .then(result => console.log(result))\n'
        h += '      .catch(console.warn);\n'
        h += '  </script>\n'
    
    h += '<p>Ian Thomas 2022</p>\n'
    h += '<p><a href="../..">Return to main page</a></p>\n'
    h += '</body>\n'
    h += '</html>\n'

    return h



@app.route('/nomad_orders.json', methods=["GET", "POST"])
def serve_json():
    
    order = request.args.get("order", type=int)

    return render_template("nomad_order_%i.json" %order)



if __name__ == '__main__':
    app.run(debug=False)



