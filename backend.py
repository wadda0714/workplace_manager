from flask import Flask, request, Response, abort, render_template,session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
import sqlite3

app = Flask(__name__)

@app.route('/login',methods = ['POST'])
def login():
    if request.method == "POST":
        un = request.form.get("username")
        pwd = request.form.get("password")
        dbname = "systemdesign.sqlite"
        con = sqlite3.connect(dbname)
        cursor = con.cursor()
        cursor.execute("SELECT hashpass FROM employeeDB WHERE empname="+ un)
        print(cursor.fetchall())
        return render_template("map.html")
        
@app.route("/admin",methods = ["GET","POST"])
def admin():
    return render_template("admin.html")

@app.route('/register',methods = ['POST'])
def register():
    if request.method == "POST":
        un = request.form.get("username")
        pwd = request.form.get("password")
        place = request.form.get("working_place")
        dbname = "systemdesign.sqlite"
        con = sqlite3.connect(dbname)
        cursor = con.cursor()
        cursor.execute("")
        
        print(place)
      
@app.route('/',methods = ['GET'])
def login_form():
    return render_template("login.html")

@app.route('/signup',methods = ['GET'])
def signup():
    return render_template("signup.html")

@app.route("/regis/<workplace>",methods = ["GET","POST"])
def regis(workplace):
    dbname = "systemdesign.sqlite"
    con = sqlite3.connect(dbname)
    cursor = con.cursor()
    cursor.execute(sql_generateA())
    con.close()
    return render_template("map.html")
    
#def sql_generateA(dst_table,dst_data,ope):
   # if ope == "insert":
      #  pass
   # else if ope == "login":
     #   pass
        
   # else if ope == "update":
      #  pass
    #else if ope == "delete":
      #  pass
    
   # query = "SELECT" + dst_data + "FROM" + dst_table
    #return query
    
if __name__ == '__main__':
    
    app.run(host="127.0.0.1", port=5555, debug=True)
    
