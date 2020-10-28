from flask import Flask, request, Response, abort, render_template,session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin


app = Flask(__name__)


@app.route('/login',methods = ['POST'])
def login():
    if request.method == "POST":
        un = request.form.get("username")
        username = session.get('un',un)
        
        return render_template("map.html", username = username)
@app.route('/',methods = ['GET'])
def login_form():
    return render_template("login.html")
@app.route('/map',methods = ['GET'])
def map():
    return render_template("map.html")

if __name__ == '__main__':
    
    app.run(host="127.0.0.1", port=5555, debug=True)
