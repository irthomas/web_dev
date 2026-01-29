# -*- coding: utf-8 -*-
"""
Created on Wed May 12 16:46:49 2021

@author: iant

READ IN COP ROW INFO, SHOW SUBDOMAIN TABLE WITH CLICKABLE FRAMES TO SCIENCE/STEPPING AND FIXED ROWS


"""


from views import make_subdomain_table, get_subd_row_info


from flask import Flask, request, render_template
app = Flask(__name__)



@app.route('/', methods=["GET", "POST"])
def make_index_page():

    channel = request.args.get("channel", default="lno", type=str)
    
    search_params = {"channel":channel}
    
    subdomain_table = make_subdomain_table(search_params)
    

    return render_template("index.html", subdomain_table=subdomain_table)

@app.route('/info', methods=["GET", "POST"])
def subd_row_info():
    
    channel = "lno"
    subd_row = -1
    if request.method == "GET":
                
        channel = request.args.get("channel", default="lno", type=str)
        subd_row = request.args.get("subd_row", default=-1, type=int)
        
        return get_subd_row_info(channel, subd_row)
        


# @app.route("/ajax.txt")
# def ajax_text():
#     return "this is the replacement text"


if __name__ == '__main__':
    app.run(debug=False)




