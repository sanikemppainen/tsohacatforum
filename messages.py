from flask import session
import flask_sqlalchemy
from database import database
import users, threads


def addmessagetothread(message, id):
    userid=users.userid()
    #threadid=threads.returnthreadid()
    threadid=id
    if userid==0:
        return False
    database.session.execute("INSERT INTO Messages (message, threadid, userid, sentat) VALUES (:message, :threadid, :userid, NOW())", {"message": message, "threadid": threadid, "userid": userid})
    database.session.commit()
    return True

def getmessages(threadid):
    messagesinthread = database.session.execute("SELECT M.* FROM MESSAGES M WHERE M.threadid=:threadid)", {"threadid": threadid}).fetchall()
    return messagesinthread

