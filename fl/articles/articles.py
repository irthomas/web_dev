# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 13:13:00 2021

@author: iant

READ IN ARTICLES FROM SQLITE DB




"""


from db_functions import get_db_rows
from flask import Flask#, request, render_template
app = Flask(__name__)




@app.route('/')
def make_articles_page():
    

    rows = get_db_rows("articles")
    
    

    h = '<html><head>\n'

    h += '<title>Papers of Interest to the NOMAD Team</title>\n'
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
    for table_header in ["Title", "Journal", "First Author", "Publication Date", "DOI"]:
        h += '<th>%s</th>\n' %table_header
    h += '</tr>'

    for row in rows:
        h += '<tr>\n'
        for element in row[1:-1]:
            h += '<td>%s</td>' %element
        h += '<td><a href="https://dx.doi.org/%s">%s</a></td>' %(row[-1], row[-1])
    h += '</tr>\n'
    h += "</body></html>"

    return h







if __name__ == '__main__':
    app.run(debug=False)




