from flask import session
import flask_sqlalchemy
from database import database
import users, threads


def addmessagetothread(message, id):
    userid=users.userid()
    #threadid=threads.returnthreadid()
    threadid= id
    userid=users.userid()
    if userid==0:
        return False
    #TÄMÄ EI MENE MESSAGEEN SINNE EI MENE USERNAME MUTTA USER TABLESSA USENAME MENEE 
    getusername=database.session.execute("SELECT username FROM Users WHERE id=:userid", {"userid":userid})
    username=getusername.fetchone()[0]
    database.session.execute("INSERT INTO Messages (message, userid, threadid, username, sentat) VALUES (:message, :userid, :threadid, :username, NOW())", {"message": message, "userid": userid, "threadid": threadid, "username": username})
    database.session.commit()
    return True

def getmessages(threadid):
    messagesinthread = database.session.execute("SELECT M.* FROM MESSAGES M WHERE M.threadid=:threadid)", {"threadid": threadid}).fetchall()
    return messagesinthread

