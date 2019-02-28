from todolist.dbconnection import con

def get_DataBase_Results(sqlQuery):
    sqlConn = con()
    cur = sqlConn.cursor(buffered=True)
    cur.execute(sqlQuery)
    data = cur.fetchall()
    sqlConn.commit()
    return data

def insert_DataBase_Results(sqlQuery):
    sqlConn = con()
    cur = sqlConn.cursor(buffered=True)
    cur.execute(sqlQuery)
    sqlConn.commit()
    return cur