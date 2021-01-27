# -*- coding: utf-8 -*
from flask import Flask, request, Response, abort, render_template,session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
import sqlite3
import datetime
import sys
import io

app = Flask(__name__)

@app.route('/login',methods = ['POST'])
def login():
    if request.method == "POST":
        un = request.form.get("username")
        pwd = request.form.get("password")
        admin_password = request.form.get("admin_password")
        cursor,con = connect_db()
        cursor.execute("SELECT hashpass FROM emptable WHERE empname='"+un+"'")
        li = cursor.fetchone()
        if li is None:
            msg = "usernameかpasswordが違います。入力しなおしてください。"
            return render_template("new-login.html",err_msg=msg)
        else:
            if li[0] == pwd:
                cursor.execute("SELECT defaultposition FROM emptable WHERE empname='"+un+"'")
                record = cursor.fetchone()
                cursor.execute("UPDATE emptable SET sheet = ? WHERE empname=?",(record[0],un))
                con.commit()
                con.close()
                if admin_password == "jugon":
                    return render_template("map.html",username=un,greeding = checktime(),admin_msg="管理者でログイン中")
                else:
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
            cursor.execute("INSERT INTO emptable values(?,?,?,?,?)",(un,pwd,"出勤","",""))
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
    record = cursor.fetchone()
    print(record)
    if record is None:
        msg = "ユーザーは存在しません"
        return render_template("search.html",msg=msg)
    elif record[0] == "":
        msg = employees_name + "さんは出勤していません"
        return render_template("search.html",msg = msg)
    else:
        seat = record[0].split(" ")
        msg = employees_name + "さんは" + record[0] + "にいます"
        return render_template(seat[0]+".html",msg = msg,dst="/static/pics/四星球.jpeg",user_seat=str(seat[1]))
@app.route('/get_map/<Page>')
def get_map(Page):
    
    return render_template(Page+".html")
@app.route("/find/<seat>" ,methods = ["GET","POST"])
def find(seat):
    if False:
        pass
    else:

        filename = request.form.get("filename")
        scroll = request.form.get("scroll")
        print(scroll)
        cursor,con = connect_db()
        
        cursor.execute("SELECT empname FROM emptable WHERE sheet =?",(filename + " " + seat,) )
        names = cursor.fetchall()
        name = list()
        for i in names:
            name.append(i[0]) 
        if name == []:
            a  = "この席は空いています"
            msg = list()
            msg.append(a)
            return render_template(filename+".html",name=msg,scr=scroll,seat=seat)
        else:
            return render_template(filename+".html",name=name,scr=scroll,seat=seat)
        
@app.route("/kintai",methods = ["POST"])
def kintai():
    seat = request.form.get("seat")
    filename = request.form.get("filename")
    if seat == None:
        seat = "0"
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
            cursor.execute("UPDATE emptable set sheet = ?,status = ?, defaultposition = ? WHERE empname = ?",(filename+" "+seat,kintai,filename+" "+seat,name))
            con.commit()
            con.close()
            msg="登録完了しました"
        
        except sqlite3.Error as e:
            msg = "登録失敗しました"
    
            
    else:
        try:
                
            cursor,con = connect_db()
            cursor.execute("UPDATE emptable set sheet = ?,status = ? WHERE empname = ?",(filename+" "+seat,kintai,name))
            con.commit()
            con.close()
            msg="登録完了しました"
        
        except sqlite3.Error as e:
             msg = "登録失敗しました"
    
    return render_template(filename+".html",msg=msg)
@app.route('/register_map',methods=["POST"])
def register_map():
    html = request.form.get("imagemap")
    list(html)[11] = ""
    imgname = request.form.get("imgname")
    mapname = imgname.split(".")[0]
    print(mapname)
    path = "templates/"+mapname+".html"
    upper_html = ("""<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache">
    <link rel="stylesheet" href="/static/css/ikkai.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <title>Document</title>
</head>

<body>
    <script>
    </script>
    <form action="/kintai" method="POST" id="submit">

        <fieldset>

            <legend>勤怠情報変更フォーム</legend>
            <p>勤務状況</p><select name="kintai" id="kintai">
      <option>出勤</option>
      <option>社用外出</option>
      <option>私用外出</option>
      <option>遅刻</option>
      <option>早退</option>
      <option>休み</option>
      <option>午前休</option>
      <option>午後休</option>
      <option>在宅勤務</option>
      <option>退社</option>
      <option>出張</option>
    </select>
            <br>

            <label class="always"><input type="checkbox"  id ="flag" >毎日この席に座る</label>
            <br>
            <label><input type="submit" value="送信" onclick="flag_check()" ></label>
        </fieldset>
    </form>
    <p>{{msg}}</p>
    <p id="submit_msg"></p>
    <ul>
        {% for msg in name %}
        <li>{{msg}}</li>
        {% endfor %}
    </ul>
    <div class="contents">
        <img src="/static/pics/"""+imgname+"""" usemap="#ImageMap1" alt="" />""")
    lower_html = ("""</div>




    <script type="text/javascript">
        function get_class(e) {
            var e = e || window.event;
            var elem = e.target || e.srcElement;
            var elem_id = elem.id;
            var filename = document.getElementsByTagName("map")[0].id.split(".")[0];
            var seat = "{{seat}}";
            if (seat != elem_id) {
                var form = document.createElement("form");
                var input = document.createElement("input");
                var scroll = document.createElement("input");
                scroll.name = "scroll";
                scroll.type = "hidden";
                scroll.value = document.documentElement.scrollTop;
                form.appendChild(scroll);
                form.action = "/find/" + elem.id;
                form.method = "post";
                input.name = "filename";
                input.type = "hidden";
                input.value = filename;
                form.appendChild(input);
                document.body.appendChild(form);

                form.submit();

            }





        }
    </script>
    <script>
    var map = document.getElementsByTagName("map")
    var count=0
    var i =0
    var child = map[0].childNodes
    for (i=0;i<child.length;i++){
        child.item(i).id = String(i)
        print(child.item(i).id)
        count++
    }
</script>
    <script>
        var form = document.getElementById("submit");
        var filename = document.getElementsByTagName("map")[0].id.split(".")[0];
        var input = document.createElement("input");
        input.name = "filename"
        input.value = filename
        input.type = "hidden";
        form.appendChild(input)
    </script>
    <script type="text/javascript">
        function submit(e) {
            var elem = document.getElementById("seat");
            if (elem != null) {
                elem.parentNode.removeChild(elem);
            }
            var form = document.getElementById("submit");
            var e = e || window.event;

            var elem = e.target || e.srcElement;

            var elem_id = elem.id;
            var input = document.createElement("input");
            var input2 = document.createElement("input");
            var msg = document.getElementById("submit_msg");
            var filename = document.getElementsByTagName("map")[0].id.split(".")[0];
            input.name = "filename"
            input.value = filename
            input.type = "hidden";
            form.appendChild(input)


            input2.type = "hidden";

            input2.name = "seat";

            input2.value = elem.id;

            input2.id = "seat";
            msg.textContent = elem.id + "を選択しました";

            form.appendChild(input2);


        }
    </script>
    <script type="text/javascript">
        function flag_check() {
            var checkbox = document.getElementById("flag");
            var input = document.createElement("input");
            var form = document.getElementById("submit");
            input.name = "flag"
            input.type = "hidden"
            if (checkbox.checked == true) {
                input.value = "on";
            } else {
                input.value = "off";
            }
            form.appendChild(input)
        }
    </script>
</body>
<script type="text/javascript">
    scroll();
    var form = document.getElementById("submit");

    var parent_username = window.parent.document.getElementById("username");

    var username = parent_username.textContent;
    var name_input = document.createElement("input");

    name_input.type = "hidden";

    name_input.name = "name";

    name_input.value = username;

    form.appendChild(name_input);

    function scroll() {
        try {
            s = "{{scr}}";
            if (s != "") {
                document.documentElement.scrollTop = Number(s);
            }


        } catch (error) {
            alert(error);
        }
    }
</script>
<script>
    var seat = "{{user_seat}}";
    console.log(seat)
    var parent_elem = document.getElementsByTagName("map")[0].split(".")[0]
    var elem = document.getElementById(seat)
    var coords = $("#" + seat).attr('coords').split(',');
    console.log(coords)
    var thisLeft = coords[0];
    var thisTop = coords[1];
    for (var i = 0; i < coords.length; i++) {
        if (i % 2 == 0) {
            thisLeft = Math.min(thisLeft, coords[i]);
        } else {
            thisTop = Math.min(thisTop, coords[i]);
        }
    }
    var offsettop = elem.offsetTop
    var offsetleft = elem.offsetLeft
    console.log(offsetleft)
    var img = document.createElement("img")
    img.src = "/static/pics/四星球.jpeg"
    img.style = "margin-left:" + thisLeft + "px;margin-top:" + thisTop + "px;width:10px;height:10px;,position:absolute;"
    parent_elem.appendChild(img)
    document.body.getElementById(parent_elem)
</script>


</html>""")
    html = upper_html+html+lower_html
    selecter = '<!--ここにはいる-->\n<li class="menu-item"><a href="#" id="'+mapname+'" onclick="disp_iframe()">'+mapname+'</a></li>\n'
    replace_setA = ('<!--ここにはいる-->', selecter)
    replace_func("templates/map.html",replace_setA)
    with open(path,'x',encoding="utf-8") as f:
        f.write(html)
    return render_template("index.html",msg="登録完了しました")
@app.route('/delete',methods = ["POST"])
def delete_emp():
    name = request.form.get("empname")
    cursor,con = connect_db()
    cursor.execute("DELETE from emptable WHERE empname=? ",(name,))
    con.commit()
    con.close()
    msg = "削除完了しました"
    return render_template("del.html",msg=msg)
    

            
        

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
    dbname = "userinfo.sqlite"
    con = sqlite3.connect(dbname)
    cursor= con.cursor()
    return cursor,con
    
    

def replace_func(fname, replace_set):
    target, replace = replace_set
    
    with open(fname, 'r',encoding="utf-8") as f1:
        tmp_list =[]
        for row in f1:
            if row.find(target) != -1:
                tmp_list.append(replace)
            else:
                tmp_list.append(row)
    
    with open(fname, 'w',encoding="utf-8") as f2:
        for i in range(len(tmp_list)):
            f2.write(tmp_list[i])
        print("inserted!")
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
    
