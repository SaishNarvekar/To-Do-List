from mysql import connector

# class Connection:

#     # con = connector.connect(user="bot",password="planner@2019",host="127.0.0.1",database='todolist')

#     # def __init__(self):
#     #     self.con = connector.connect(user="bot",password="planner@2019",host="127.0.0.1",database='todolist')

#     def retrive(self,sqlQuery):
#         sqlConn = Connection.con
#         cur = sqlConn.cursor(buffered=True)
#         cur.execute(sqlQuery)
#         data = cur.fetchall()
#         sqlConn.commit()
#         return data

#     def insert(self,sqlQuery):
#         sqlConn = Connection.con
#         cur = sqlConn.cursor(buffered=True)
#         cur.execute(sqlQuery)
#         sqlConn.commit()
#         return cur

def con():
    return connector.connect(user="bot",password="planner@2019",host="127.0.0.1",database='todolist')

def retrive(sqlQuery):
    sqlConn = con()
    cur = sqlConn.cursor(buffered=True)
    cur.execute(sqlQuery)
    data = cur.fetchall()
    sqlConn.commit()
    return data

def insert(sqlQuery):
    sqlConn = con()
    cur = sqlConn.cursor(buffered=True)
    cur.execute(sqlQuery)
    sqlConn.commit()
    return cur
    