from mysql import connector

def con():
    return connector.connect(user="bot",password="planner@2019",host="127.0.0.1",database='todolist')
    