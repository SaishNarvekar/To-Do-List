from flask import Flask, render_template, request, url_for, redirect
from databaseConn import con


app = Flask(__name__)

@app.route("/")
def index():
    sqlConn = con()
    cur = sqlConn.cursor()
    cur.execute("select * from itemlist")
    data = cur.fetchall()
    return render_template("index.html",data = data)

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


if(__name__ == '__main__'):
    app.run(debug=True)
