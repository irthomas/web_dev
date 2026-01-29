# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 13:13:00 2021

@author: iant



"""

# import sqlite3
# import re
# import posixpath
# import sys
from datetime import datetime

from db_functions import search_db
from flask import Flask, request, render_template
app = Flask(__name__)


@app.route('/')
def make_index_page():
    
    return render_template("index.html")



if __name__ == '__main__':
    app.run(debug=False)




