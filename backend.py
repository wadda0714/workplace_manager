from flask import Flask, request, Response, abort, render_template,session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
import sqlite3

app = Flask(__name__)

@app.route('/login',methods = ['POST'])
def login():
    if request.method == "POST":
        un = request.form.get("username")
        pwd = request.form.get("password")
        dbname = "emp.sqlite"
        con = sqlite3.connect(dbname)
        cursor = con.cursor()
        cursor.execute("SELECT hashpass FROM emptable WHERE empname='"+un+"'")
        li = cursor.fetchone()
        print(li[0])
        if li[0] == pwd:
            return render_template("map.html",username=un)
        else:
            msg = "usernameかpasswordが違います。入力しなおしてください。"
            return render_template("new-login.html",err_msg=msg)
        
        
@app.route("/admin",methods = ["GET","POST"])
def admin():
    return render_template("admin.html")

@app.route('/register',methods = ['POST'])
def register():
    if request.method == "POST":
        un = request.form.get("username")
        pwd1 = request.form.get("password1")
        pwd2 = request.form.get("password2")
        email = request.form.get("email")
        dbname = "emp.sqlite"
        con = sqlite3.connect(dbname)
        cursor = con.cursor()
        cursor.execute("INSERT INTO emptable values(1)")
        con.commit()
        print(place)
      
@app.route('/',methods = ['GET'])
def login_form():
    return render_template("new-login.html")

@app.route('/signup',methods = ['GET'])
def signup():
    return render_template("signup.html")

@app.route("/regis/<workplace>",methods = ["GET","POST"])
def regis(workplace):
    dbname = "mainprogram.sqlite"
    con = sqlite3.connect(dbname)
    cursor = con.cursor()
    cursor.execute("SELECT ")
    con.close()
    return render_template("map.html")

@app.route("/search",methods = ["POST"])
def search():
    employees_name = request.form.get("employees_name")
    dbname = "mainprogram.sqlite"
    con = sqlite3.connect(dbname)
    cursor = con.cursor()
    cursor.execute("SELECT defaultposition FROM emptable WHERE empname='"+employees_name+"'")
    
    return render_template("map.html",workplace=text1)
@app.route('/get_map/<Page>')
def get_map(Page):
    return render_template(Page+".html")
@app.route("/find/<seat>" ,methods = ["GET","POST"])
def find(seat):
    #dbname = "mainprogram.sqlite"
    #con = sqlite3.connect(dbname)
   # cursor = con.cursor()
   # cursor.execute("SELECT empname FROM emptable WHERE position")
    print(seat)
    return render_template("ikkai.html",user=seat)
        

    
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
    
