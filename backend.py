from flask import Flask, request, Response, abort, render_template,session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
import sqlite3

app = Flask(__name__)

@app.route('/login',methods = ['POST'])
def login():
    if request.method == "POST":
        un = request.form.get("username")
        pwd = request.form.get("password")
        return render_template("map.html", username = un ,password = pwd)
    
@app.route('/register',methods = ['POST'])
def register():
    if request.method == "POST":
        un = request.form.get("username")
        pwd = request.form.get("password")
        place = request.form.get("working_place")
        print(place)
        
@app.route('/',methods = ['GET'])
def login_form():
    return render_template("login.html")
@app.route('/signup',methods = ['GET'])
def signup():
    return render_template("signup.html")

if __name__ == '__main__':
    
    app.run(host="127.0.0.1", port=5555, debug=True)
    aaaaa
