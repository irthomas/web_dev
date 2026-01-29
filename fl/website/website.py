# -*- coding: utf-8 -*-
"""
Created on Sat Feb  20 10:25:08 2021

@author: iant
"""

from flask import Flask, render_template
app = Flask(__name__, static_url_path='/static')

@app.route('/')
def make_index():
    return render_template("index.html")

# @app.route('/cv.html')
# def make_cv():
#     return render_template("cv.html")


if __name__ == "__main__":
    app.run(debug=True)