from todolist import app
from flask import session, request, render_template, redirect,url_for
import datetime,time,uuid,hashlib
from todolist.connection import con,retrive, insert

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=15)
    session.modified = True
    delete_expired_session()


@app.route("/")
def index():
    
    if "uuid" in session:
        update_timestamp()
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
        update_timestamp()
        expires_timestamp()
        return redirect(url_for('index'))

    return render_template('login.html', error=False)


@app.route('/register', methods=['GET', 'POST'])
def register():

    if "uuid" in session:
        update_timestamp()
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
        insert(sqlQuery)
        return render_template('register.html', registered=True)


@app.route('/logout')
def logout():
    insert(
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
    
    sqlConn = con()
    cur = sqlConn.cursor(buffered=True)
    sqlQuery = "SELECT hashed_password from users where username = \"{}\";".format(
        username)
    cur.execute(sqlQuery)
    

    if cur.rowcount == 0:
        print("Wrong Info")
        return render_template('login.html', error=True)

    for i in cur.fetchone():
        if i == hashed_password:
            print("Valid")
            userID = uuid.uuid4()
            session['uuid'] = userID
            insert(
                "insert into session_tracker (uuid,username) values (\"{}\" ,\"{}\")".format(userID, username))
            expires_timestamp()
            return redirect(url_for('index'))
        else:
            print("Wrong Password")
            return render_template('login.html', error=True)


def update_timestamp():
    currentTimestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sqlQuery = "Update session_tracker set updated_at =\"{}\"".format(
        currentTimestamp)
    insert(sqlQuery)
    expires_timestamp()


def expires_timestamp():
    expireTimestamp = (datetime.datetime.now(
    ) + datetime.timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S')
    sqlQuery = "Update session_tracker set expires_at =\"{}\"".format(expireTimestamp)
    insert(sqlQuery)
    # print(expireTimestamp)


def delete_expired_session():
    currentTimestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sqlQuery = "delete from session_tracker where expires_at <= \"{}\"".format(
        currentTimestamp)
    insert(sqlQuery)