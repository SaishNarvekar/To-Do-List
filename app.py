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
        username = request.form['username']
        hashed_password = hashlib.sha512(request.form['password'].encode('utf-8')).hexdigest()
        return auth_user(username,hashed_password)

    if "username" in session:
        return redirect(url_for('index'))

    return render_template('login.html',error=False)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if "username" in session:
        return redirect(url_for('index'))
    if request.method == 'GET':
        return render_template('register.html',registered = False)
    if request.method == 'POST':
        email = request.form['email']
        userName = request.form['username']
        hashPassWord = hashlib.sha512(request.form['password'].encode('utf-8')).hexdigest()
        sqlConn = con()
        cur = sqlConn.cursor()
        sqlQuery = "Insert Into users(email,username,hashed_password) VALUES (\"{}\",\"{}\",\"{}\");".format(email,userName,hashPassWord)
        cur.execute(sqlQuery)
        sqlConn.commit()
        return render_template('register.html',registered = True)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.errorhandler(404)
def notFound(error):
    return "404 Page"

def auth_user(username,hashed_password):
    sqlConn = con()
    cur = sqlConn.cursor(buffered=True)
    sqlQuery = "SELECT hashed_password from users where username = \"{}\";".format(username)
    cur.execute(sqlQuery)
    
    # print(cur.rowcount)
    # print(hashed_password)

    if cur.rowcount == 0:
        print("Wrong Info")
        return render_template('login.html',error=True)

    for i in cur.fetchone():
        if i == hashed_password:
            print("Valid")
            session['username'] = username
            return redirect(url_for('index'))
        else:
            print("Wrong Password")
            return render_template('login.html',error=True)

if(__name__ == '__main__'):
    app.run(debug=True)
