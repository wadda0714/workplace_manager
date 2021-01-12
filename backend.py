from flask import Flask, request, Response, abort, render_template,session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
import sqlite3
import datetime

app = Flask(__name__)
@app.route('/login',methods = ['POST'])
def login():
    if request.method == "POST":
        un = request.form.get("username")
        pwd = request.form.get("password")
        cursor,con = connect_db()
        cursor.execute("SELECT hashpass FROM emptable WHERE empname='"+un+"'")
        li = cursor.fetchone()
        print(li[0])
        if li[0] == pwd:
            cursor.execute("SELECT defaultposition FROM emptable WHERE empname='"+un+"'")
            record = cursor.fetchone()
            cursor.execute("UPDATE emptable SET sheet = ? WHERE empname=?",(record[0],un))
            con.commit()
            con.close()
            return render_template("map.html",username=un,greeding = checktime())
        else:
            msg = "usernameかpasswordが違います。入力しなおしてください。"
            return render_template("new-login.html",err_msg=msg)
        
@app.route('/account_register',methods = ["POST"])
def account_register():
    if request.method == "GET":
        return render_template("account_register.html")
    elif request.method == "POST":
        un = request.form.get("username")
        pwd = request.form.get("password")
        cursor,con = connect_db()
        cursor.execute("SELECT empname FROM emptable WHERE empname=?",(un,))
        if cursor.fetchone() == None:
            cursor.execute("INSERT INTO emptable values(?,?,?,0,0)",(un,pwd,"出勤"))
            con.commit()
            con.close()
            return render_template("map.html",username=un,greeding = checktime())
        else:
            return render_template("new-login.html",msg2="既に存在するユーザーです")
            
        
        
        
@app.route("/admin",methods = ["GET","POST"])
def admin():
    return render_template("admin.html")
@app.route("/at_info", methods = ["POST"])
def info():
    cursor,con = connect_db()
    query = "SELECT empname FROM emptable WHERE status='" + "出勤" +"'"
    cursor.execute(query)
    employees = cursor.fetchall()
    employee = list()
    for i in employees:
        employee.append(i[0]) 
    return render_template("information.html",employees=employee)
    

      
@app.route('/',methods = ['GET'])
def login_form():
    return render_template("new-login.html")

@app.route('/signup',methods = ['GET'])
def signup():
    return render_template("signup.html")

#@app.route("/regis/<workplace>",methods = ["GET","POST"])
#def regis(workplace):
    #dbname = "mainprogram.sqlite"
    #con = sqlite3.connect(dbname)
    #cursor = con.cursor()
    #cursor.execute("SELECT ")
    #con.close()
    #return render_template("map.html")

@app.route("/search",methods = ["POST"])
def search():
    employees_name = request.form.get("employees_name")
    cursor,con = connect_db()
    cursor.execute("SELECT sheet FROM emptable WHERE empname='"+employees_name+"'")
    seat = cursor.fetchone()
    msg = employees_name + "さんは" + str(seat[0]) + "にいます"
    return render_template("search.html",msg = msg )
@app.route('/get_map/<Page>')
def get_map(Page):
    
    return render_template(Page+".html")
@app.route("/find/<seat>" ,methods = ["GET","POST"])
def find(seat):
    if False:
        pass
    else:
        previous_seat = seat
        scroll = request.form.get("scroll")
        print(scroll)
        cursor,con = connect_db()
        query = "SELECT empname FROM emptable WHERE sheet =" + seat
        cursor.execute(query)
        names = cursor.fetchall()
        name = list()
        for i in names:
            name.append(i[0]) 
        if name == []:
            a  = "この席は空いています"
            msg = list()
            msg.append(a)
            return render_template("ikkai.html",name=msg,scr=scroll,seat=seat)
        else:
            return render_template("ikkai.html",name=name,scr=scroll,seat=seat)
        
@app.route("/kintai",methods = ["POST"])
def kintai():
    seat = request.form.get("seat")
    if seat == None:
        seat = 0
    seat = int(seat)
    kintai = request.form.get("kintai")
            
    name = request.form.get("name")
    flag = request.form.get("flag")
    print(flag)
    print(name)
    print(kintai)
    print(seat)
    if flag == "on":
        try:
            
            cursor,con = connect_db()
            cursor.execute("UPDATE emptable set sheet = ?,status = ?, defaultposition = ? WHERE empname = ?",(seat,kintai,seat,name))
            con.commit()
            con.close()
            msg="登録完了しました"
        
        except sqlite3.Error as e:
            msg = "登録失敗しました"
    
            
    else:
        try:
                
            cursor,con = connect_db()
            cursor.execute("UPDATE emptable set sheet = ?,status = ? WHERE empname = ?",(seat,kintai,name))
            con.commit()
            con.close()
            msg="登録完了しました"
        
        except sqlite3.Error as e:
             msg = "登録失敗しました"
    
    return render_template("ikkai.html",msg=msg)
            
        

def checktime():
    now = datetime.datetime.now()
    now_time = "{0:%H}".format(now) 
    a = now_time.lstrip("0")
    if now_time == "00":
        a = 0;
    print(now_time)
    time = int(a)
    if time >= 5 and time < 12 :
        greeding = "Good Morning!"
    elif time >= 12 and time < 17:
        greeding = "Hello!"
    else:
        greeding = "Good Evening!"
    return greeding
def connect_db():
    dbname = "systemdb.sqlite"
    con = sqlite3.connect(dbname)
    cursor= con.cursor()
    return cursor,con
    

    
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
    
