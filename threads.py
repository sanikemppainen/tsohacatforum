from flask import session
from database import database
import users, messages

def send(topic, tags, message):
	#jos threadia ei vielä ole, luo uusi ja lähetä sinne eka viesti
	# userid=users.userid(), if userid==0; return false
	userid=users.userid()
	if userid==0:
		return False
	tags=tags
	database.session.execute("INSERT INTO threads (topic, userid, createdat, tags) VALUES (:topic, :userid, NOW(), :tags)", {"topic":topic, "userid":userid, "tags":tags})
	database.session.commit()
	getthreadid=database.session.execute("SELECT id FROM Threads WHERE topic=:topic", {"topic":topic})
	threadid=getthreadid.fetchone()[0]
	messages.addmessagetothread(message, threadid)	
	return True

#lisää että näkee montako threadia on yhteensä
#lisää että näkee mikä on eniten komentoitu ja järjestykset?
def getlist():
	sql="SELECT id, topic, userid, createdat, tags FROM Threads ORDER BY id DESC"
	results=database.session.execute(sql)
	allthreads=results.fetchall()
	return allthreads

#nimeä paremmin
def getid(id):
	result=database.session.execute("SELECT topic, id FROM Threads WHERE id=:id", {"id":id})
	threadtopic=result.fetchone()[0]
	result2=database.session.execute("SELECT message, username, sentat FROM Messages WHERE Messages.threadid =:id ORDER BY id DESC", {"id":id})
	messages=result2.fetchall()
	#print(messages)
	list=[threadtopic, messages]
	return list

def returnthreadid():
    return session.get("threadid",0)

def gettags():
	results=database.session.execute("SELECT tags FROM Threads")
	alltags=results.fetchall()
	return alltags