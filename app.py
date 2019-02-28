from todolist import app

# print((datetime.datetime.now() - datetime.timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S'))

if(__name__ == '__main__'):
    app.run(host='0.0.0.0', debug=True)
