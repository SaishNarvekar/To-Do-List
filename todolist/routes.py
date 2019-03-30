from todolist import app
from flask import session, request, render_template, redirect,url_for
import datetime,time,uuid,hashlib
from todolist.connection import Connection
from todolist.session import mySession

sqlCon = Connection()
mySession = mySession()

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=15)
    session.modified = True
    mySession.delete()

@app.route("/")
def index():
    
    if "uuid" in session:
        mySession.update()
        return render_template("index.html",session=session)
    else:
        return render_template("index.html")


@app.route("/private-list")
def dashboard():
    return render_template("private-list.html")

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        hashed_password = hashlib.sha512(
            request.form['password'].encode('utf-8')).hexdigest()
        return auth_user(username, hashed_password)

    if "uuid" in session:
        mySession.update()
        return redirect(url_for('index'))

    return render_template('login.html', error=False)


@app.route('/register', methods=['GET', 'POST'])
def register():

    if "uuid" in session:
        mySession.update()
        return redirect(url_for('index'))

    if request.method == 'GET':
        return render_template('register.html', registered=False)

    if request.method == 'POST':
        email = request.form['email']
        userName = request.form['username']
        hashPassWord = hashlib.sha512(
            request.form['password'].encode('utf-8')).hexdigest()
        sqlQuery = "Insert Into users(email,username,hashed_password) VALUES (\"{}\",\"{}\",\"{}\");".format(
            email, userName, hashPassWord)
        sqlCon.insert(sqlQuery)
        return render_template('register.html', registered=True)


@app.route('/logout')
def logout():
    sqlCon.insert(
        "delete from session_tracker where uuid = \"{}\"".format(session["uuid"]))
    session.pop('uuid', None)
    return redirect(url_for('index'))


@app.route('/error/<code>')
def error(code):
    return render_template('error.html', code=code)


@app.errorhandler(404)
def notFound(error):
    return redirect('/error/404')

def auth_user(username, hashed_password):
    
    sqlQuery = "SELECT hashed_password from users where username = \"{}\";".format(
        username)
    cur = sqlCon.insert(sqlQuery)
    
    if cur.rowcount == 0:
        print("Wrong Info")
        return render_template('login.html', error=True)

    for i in cur.fetchone():
        if i == hashed_password:
            print("Valid")
            userID = uuid.uuid4()
            session['uuid'] = userID
            sqlCon.insert(
                "insert into session_tracker (uuid,username) values (\"{}\" ,\"{}\")".format(userID, username))
            mySession.update()
            return redirect(url_for('index'))
        else:
            print("Wrong Password")
            return render_template('login.html', error=True)