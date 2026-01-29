# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 21:24:57 2022

@author: iant

TEST MAKING A SIMPLE LOGIN SERVER
"""


from flask import Flask, request, url_for, redirect

from flask_login import LoginManager, login_required, UserMixin, login_user, current_user, logout_user

app = Flask(__name__)

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
    return user


# @login_manager.request_loader
# def request_loader(request):
#     username = request.form.get("username")
#     if username not in users:
#         return

#     user = User()
#     user.id = username
#     user.email = users[username]["email"]
#     return user


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
        return redirect(url_for("protected"))

    return "Bad login"


@app.route("/protected")
@login_required
def protected():
    return "Logged in as <b>" + current_user.id + "</b> with email address <b>" + current_user.email + "</b>. <a href='logout'>Logout</a>"



if __name__ == "__main__":
    app.run(debug=True)
