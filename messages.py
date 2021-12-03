from flask import session
import flask_sqlalchemy
from database import database
import users, threads

def addmessagetothread(content):
    userid=users.userid()
    threadid=threads.getid()
    if userid==0:
        return False
    database.session.execute("INSERT INTO Messages (content, threadid, userid, sentat) VALUES (:content, :threadid, :userid, NOW())", {"content": content, "threadid": threadid, "userid": userid})
    database.session.commit()
    return True

def getmessages(threadid):
    messagesinthread = database.session.execute("SELECT M.* FROM MESSAGES M WHERE M.threadid=:threadid)", {"threadid": threadid}).fetchall()
    return messagesinthread

