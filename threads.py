from flask import session
from database import database
import users

def send(topic):
	#jos threadia ei vielä ole, luo uusi ja lähetä sinne eka viesti
	# userid=users.userid(), if userid==0; return false
	userid=users.userid()
	if userid==0:
		return False
	database.session.execute("INSERT INTO threads (topic, userid, createdat) VALUES (:topic, :userid, NOW())", {"topic":topic, "userid":userid})
	database.session.commit()
	
	return True

#lisää että näkee montako threadia on yhteensä
#lisää että näkee mikä on eniten komentoitu ja järjestykset?
def getlist():
	sql="SELECT id, topic, username, createdat, tags FROM Threads ORDER BY id DESC"
	results=database.session.execute(sql)
	allthreads=results.fetchall()
	#session["id"]=allthreads.id
	return allthreads

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
