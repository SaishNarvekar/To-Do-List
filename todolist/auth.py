from todolist import app
from flask import session, request, render_template, redirect,url_for
import datetime,time,uuid,hashlib
from todolist.connection import Connection
from todolist.session import mySession

sqlCon = Connection()
mySession = mySession()

class Authentication:

    def __init__(self):
        pass

    def auth_user(self,username, hashed_password):

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
