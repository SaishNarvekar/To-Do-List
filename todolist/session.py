import datetime
from todolist.connection import Connection 
from flask import session

sqlCon = Connection()


class mySession:

    def __init__(self):
        pass

    def __enter__(self):
        return self
    
    @property
    def currentTime(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @property
    def expireTime(self):
        return (datetime.datetime.now(
    ) + datetime.timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S')

    def update(self):
        sqlQuery = "Update session_tracker set updated_at =\"{}\"".format(
        self.currentTime)
        sqlCon.insert(sqlQuery)
        sqlQuery = "Update session_tracker set expires_at =\"{}\"".format(
        self.expireTime)
        sqlCon.insert(sqlQuery)
    
    def delete(self):
        sqlQuery = "delete from session_tracker where expires_at <= \"{}\"".format(
        self.currentTime)
        sqlCon.insert(sqlQuery)