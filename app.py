from flask import Flask, render_template, request, url_for, redirect, session
from databaseConn import con
import hashlib, uuid
import datetime

app = Flask(__name__)
app.secret_key = "82bfce4d0166155f1dd8524112584fb1"


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=15)

@app.route("/")
def index():
    data = get_DataBase_Results("select * from itemlist")
    if "username" in session:
        return render_template("index.html", data=data, session=session)
    else:
        return render_template("index.html", data=data)


@app.route("/add")
def dashboard():
    return render_template("add.html")


@app.route("/update", methods=['POST'])
def update():
    value = request.form['item']
    print(value)
    sqlQuery = "Insert Into itemlist(item) VALUES (\"{}\");".format(value)
    insert_DataBase_Results(sqlQuery)
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        hashed_password = hashlib.sha512(request.form['password'].encode('utf-8')).hexdigest()
        return auth_user(username,hashed_password)

    if "uuid" in session:
        return redirect(url_for('index'))

    return render_template('login.html',error=False)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if "uuid" in session:
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('register.html',registered = False)
    if request.method == 'POST':
        email = request.form['email']
        userName = request.form['username']
        hashPassWord = hashlib.sha512(request.form['password'].encode('utf-8')).hexdigest()
        sqlQuery = "Insert Into users(email,username,hashed_password) VALUES (\"{}\",\"{}\",\"{}\");".format(email,userName,hashPassWord)
        insert_DataBase_Results(sqlQuery)
        return render_template('register.html',registered = True)


@app.route('/logout')
def logout():
    insert_DataBase_Results("delete from session_tracker where uuid = \"{}\"".format(session["uuid"]))
    session.pop('uuid', None)
    return redirect(url_for('index'))

@app.errorhandler(404)
def notFound(error):
    return "404 Page"

def auth_user(username,hashed_password):
    sqlConn = con()
    cur = sqlConn.cursor(buffered=True)
    sqlQuery = "SELECT hashed_password from users where username = \"{}\";".format(username)
    cur.execute(sqlQuery)
    
    if cur.rowcount == 0:
        print("Wrong Info")
        return render_template('login.html',error=True)

    for i in cur.fetchone():
        if i == hashed_password:
            print("Valid")
            userID = uuid.uuid4()
            session['uuid'] = userID
            insert_DataBase_Results("insert into session_tracker values (\"{}\" ,\"{}\")".format(userID,username))
            return redirect(url_for('index'))
        else:
            print("Wrong Password")
            return render_template('login.html',error=True)

def get_DataBase_Results(sqlQuery):
    sqlConn = con()
    cur = sqlConn.cursor()
    cur.execute(sqlQuery)
    data = cur.fetchall()
    sqlConn.commit()
    return data

def insert_DataBase_Results(sqlQuery):
    sqlConn = con()
    cur = sqlConn.cursor()
    cur.execute(sqlQuery)
    sqlConn.commit()

if(__name__ == '__main__'):
    app.run(host='0.0.0.0',debug=True)
