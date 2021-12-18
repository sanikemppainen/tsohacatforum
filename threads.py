from flask import session
from database import database
import users, messages

def send(topic, tags, message, username, pictureid):
	#jos threadia ei vielä ole, luo uusi ja lähetä sinne eka viesti
	# userid=users.userid(), if userid==0; return false
	userid=users.userid()
	if userid==0:
		return False
	tags=tags
	username=username
	preview=message[:100]+(message[100:] and "...")
	database.session.execute("INSERT INTO threads (topic, userid, username, createdat, tags, preview) VALUES (:topic, :userid, :username, NOW(), :tags, :preview)", {"topic":topic, "userid":userid, "username":username, "tags":tags, "preview":preview})
	database.session.commit()
	getthreadid=database.session.execute("SELECT id FROM Threads WHERE topic=:topic", {"topic":topic})
	threadid=getthreadid.fetchone()[0]
	messages.addmessagetothread(message, threadid, pictureid)	
	return True

#lisää että näkee montako threadia on yhteensä
#lisää että näkee mikä on eniten komentoitu ja järjestykset?
def getlist():
	sql="SELECT id, topic, username, createdat, tags, preview FROM Threads ORDER BY id DESC"
	results=database.session.execute(sql)
	allthreads=results.fetchall()
	return allthreads



#nimeä paremmin, hae viestit thread idllä
def getid(id):
	result=database.session.execute("SELECT topic, id FROM Threads WHERE id=:id", {"id":id})
	threadtopic=result.fetchone()[0]
	result2=database.session.execute("SELECT message, username, sentat, picturedata FROM Messages WHERE Messages.threadid =:id ORDER BY id ASC", {"id":id})
	messages=result2.fetchall()
	#loop thrpugh messsages to get pictureid and pictures for them if they have, then add to newlist and send that back??

	#print(messages)
	list=[threadtopic, messages]
	return list

def returnthreadid():
    return session.get("threadid",0)

def gettags():
	results=database.session.execute("SELECT tags FROM Threads")
	alltags=results.fetchall()
	return alltags

#def addtag(tag):
#	database.session.execute("INSERT INTO Threads ()")

def deletethread(topic):
	try:
		database.session.execute("DELETE FROM Threads WHERE topic=:topic", {"topic":topic})
		database.session.commit()
		return True
	except:
		return False

def searchthreads(query):
    sql = "SELECT id, topic FROM Threads WHERE topic LIKE :query"
    result = database.session.execute(sql, {"query":"%"+query+"%"})
    threads = result.fetchall()
    return threads

def searchtags(query):
    sql = "SELECT id, tags, topic FROM Threads WHERE tags LIKE :query"
    result = database.session.execute(sql, {"query":"%"+query+"%"})
    tags = result.fetchall()
    return tags

def gettopicbyid(id):
	sql="SELECT id, topic FROM Threads WHERE id=:id"
	results=database.session.execute(sql, {"id":id})
	mostmessagestopic=results.fetchall()
	return mostmessagestopic
