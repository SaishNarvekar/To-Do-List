from flask import Flask, render_template, request, url_for, redirect, session
from databaseConn import con
import hashlib, uuid

app = Flask(__name__)
app.secret_key = "12345"


@app.route("/")
def index():
    sqlConn = con()
    cur = sqlConn.cursor()
    cur.execute("select * from itemlist")
    data = cur.fetchall()
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
    sqlConn = con()
    cur = sqlConn.cursor()
    sqlQuery = "Insert Into itemlist(item) VALUES (\"{}\");".format(value)
    cur.execute(sqlQuery)
    sqlConn.commit()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    if "username" in session:
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        userName = request.form['username']
        hashPassWord = hashlib.sha512(request.form['password'].encode('utf-8')).hexdigest()
        sqlConn = con()
        cur = sqlConn.cursor()
        sqlQuery = "Insert Into users(username,hashed_password) VALUES (\"{}\",\"{}\");".format(userName,hashPassWord)
        cur.execute(sqlQuery)
        sqlConn.commit()
        return render_template('register.html',registered = True)


@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    session.pop('id', None)
    return redirect(url_for('index'))


if(__name__ == '__main__'):
    app.run(debug=True)
