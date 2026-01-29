# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 21:24:57 2022

@author: iant

TODO: 
    Improve security of edit_frame get request and user dictionary
    Lock file on text input
    Datetime conversion for date inputs
    Add ability to sort columns in table
    Email reminder iframe
"""


from flask import Flask, request, url_for, redirect
from flask_login import LoginManager, login_required, UserMixin, login_user, current_user, logout_user

from config import secret_key, users

from read_from_file import read_from_file
from replace_line_in_file import replace_line_in_file
from add_line_to_file import add_line_to_file
from make_ai_table import make_ai_table
from iframes import edit_line, add_line






app = Flask(__name__)

app.secret_key = secret_key

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"




class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return

    user = User()
    user.id = username
    user.email = users[username]["email"]
    user.groups = users[username]["groups"]
    return user



@app.route("/")
@login_required
def index():
    return "Protected page. <a href='logout'>Logout</a>"


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "Logged out. <a href='login'>Login</a>"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return """
               <form action="login" method="POST">
                <input type="text" name="username" id="username" placeholder="username"/>
                <input type="password" name="password" id="password" placeholder="password"/>
                <input type="submit" name="submit"/>
               </form>
               """

    username = request.form["username"]
    if username in users and request.form["password"] == users[username]["password"]:
        user = User()
        user.id = username
        user.email = users[username]["email"]
        login_user(user)
        return redirect(url_for("ai_table"))

    return "Bad login"


@app.route("/ai_table")
@login_required
def ai_table():

    ai_dict = read_from_file()
    
    header_text = "Logged in as <b>" + current_user.id + "</b> with email address <b>" + current_user.email + "</b>. <a href='logout'>Logout</a><br><br>"

    page = make_ai_table(current_user.id, ai_dict, header_text=header_text)
    
    return page







@app.route("/edit_ai", methods=["GET"])
@login_required
def edit_ai():
    
    ai_dict = read_from_file()

    if request.method == "GET":
        id_ = request.args.get("id")
    return edit_line(id_, ai_dict[id_])

@app.route("/add_ai", methods=["GET"])
@login_required
def add_ai():
    
    ai_dict = read_from_file()
    first_key = list(ai_dict.keys())[0]
    ai_elements = list(ai_dict[first_key].keys())
    
    new_ai_number = max([int(i) for i in ai_dict.keys()]) + 1

    return add_line(new_ai_number, ai_elements)








@app.route("/submit_edit", methods=["GET", "POST"])
@login_required
def submit_edit():
    
    ai_dict = read_from_file()

    if request.method == "POST":
        
        # text = ""
        # for key in request.form:
        #     text += "%s: %s\n" %(key, request.form[key])
        # return text
        
        id_ = request.form["id"]
        
        new_line = {"id":id_}
        
        
        #convert checkboxes to list
        access_list = []
        
        for group in ["bira", "oip", "swiss"]:
            if group in request.form.keys():
                access_list.append(group)
        access = ",".join(access_list)
                
        
        for key in ai_dict[id_].keys():
            if key == "Access":
                new_line[key] = access
            else:
                new_line[key] = request.form[key]

        # text = ""
        # for key in new_line:
        #     text += "%s: %s\n" %(key, new_line[key])
        # return text
        
        
        replace_line_in_file(id_, new_line)
        
        h = ""
        h += "<h3>Action item %s (%s) has been edited</h3>\n" %(id_, new_line["Action"])
        h += '<button type="cancel" name="cancel" onclick="parent.close_edit_frame()">Close</button>\n'
        
        return h





@app.route("/submit_add", methods=["POST"])
@login_required
def submit_add():
    
    ai_dict = read_from_file()

    if request.method == "POST":
        
        # text = ""
        # for key in request.form:
        #     text += "%s: %s\n" %(key, request.form[key])
        # return text
        
        new_id = request.form["id"] #id is a string
        
        new_line = {"id":new_id}
        
        
        #convert checkboxes to list
        access_list = []
        
        for group in ["bira", "oip", "swiss"]:
            if group in request.form.keys():
                access_list.append(group)
        access = ",".join(access_list)
                

        first_key = list(ai_dict.keys())[0]
        for key in ai_dict[first_key].keys():
            if key == "Access":
                new_line[key] = access
            else:
                new_line[key] = request.form[key]

        # text = ""
        # for key in new_line:
        #     text += "%s: %s\n" %(key, new_line[key])
        # return text
        
        
        add_line_to_file(new_line)
        
        h = ""
        h += "<h3>Action item %s (%s) has been added</h3>\n" %(new_id, new_line["Action"])
        h += '<button type="cancel" name="cancel" onclick="parent.close_add_frame()">Close</button>\n'
        
        return h


if __name__ == "__main__":
    app.run(debug=False)
