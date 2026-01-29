# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 22:24:20 2021

@author: iant

SIMPLE VEGA VISUALISATION: BAR CHART
"""




from flask import Flask, render_template
app = Flask(__name__)
    

        
@app.route('/')
def make_html():
    return render_template("bar_chart.html")

@app.route('/bar_chart.json')
def make_json():
    return render_template("bar_chart.json")

if __name__ == '__main__':
    app.run(debug=True)