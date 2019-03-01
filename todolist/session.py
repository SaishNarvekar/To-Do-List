import datetime
from todolist.connection import insert,retrive 
from flask import session

def update_timestamp():
    currentTimestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sqlQuery = "Update session_tracker set updated_at =\"{}\"".format(
        currentTimestamp)
    insert(sqlQuery=sqlQuery)
    expires_timestamp()


def expires_timestamp():
    expireTimestamp = (datetime.datetime.now(
    ) + datetime.timedelta(minutes=15)).strftime('%Y-%m-%d %H:%M:%S')
    sqlQuery = "Update session_tracker set expires_at =\"{}\"".format(
        expireTimestamp)
    insert(sqlQuery=sqlQuery)
    # print(expireTimestamp)


def delete_expired_session():
    currentTimestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    sqlQuery = "delete from session_tracker where expires_at <= \"{}\"".format(
        currentTimestamp)
    insert(sqlQuery=sqlQuery)
    session.pop('uuid', None)