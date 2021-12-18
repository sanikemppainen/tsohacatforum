from flask import session
import flask_sqlalchemy
from database import database
import users, threads, photos


def addmessagetothread(message, id, pictureid):
    userid=users.userid()
    if pictureid!=None:
        picturename=photos.getpicturename(pictureid)
        picturedata=photos.showphoto(picturename)
    if pictureid==None:
        picturedata=None
    #threadid=threads.returnthreadid()
    threadid= id
    userid=users.userid()
    if userid==0:
        return False
    getusername=database.session.execute("SELECT username FROM Users WHERE id=:userid", {"userid":userid})
    username=getusername.fetchone()[0]
    database.session.execute("INSERT INTO Messages (message, userid, threadid, username, sentat, pictureid, picturedata) VALUES (:message, :userid, :threadid, :username, NOW(), :pictureid, :picturedata)", {"message": message, "userid": userid, "threadid": threadid, "username": username, "pictureid":pictureid, "picturedata":picturedata})
    database.session.commit()
    return True

def getmessages(threadid):
    messagesinthread = database.session.execute("SELECT M.* FROM MESSAGES M WHERE M.threadid=:threadid) ORDER BY sentat ASC", {"threadid": threadid}).fetchall()
    return messagesinthread

def deletemessage(id):
    try:
        database.session.execute("DELETE FROM Messages WHERE id=:id ", {"id":id})
        database.session.commit()
        return True
    except:
        return False

def searchmessages(query):
    sql = "SELECT threadid, message FROM messages WHERE message LIKE :query"
    result = database.session.execute(sql, {"query":"%"+query+"%"})
    messages = result.fetchall()
    return messages

def getmostmessages():
	# find column with most of the same (and how many of those?) 
    sql = "SELECT threadid FROM messages GROUP BY threadid ORDER BY COUNT(*) DESC LIMIT 1"
    result = database.session.execute(sql)
    mostmessages = result.fetchone()[0]
    #fetchon()? fetchall[]?
    mostmessagestopic=threads.gettopicbyid(mostmessages)
    return mostmessagestopic