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
#lisää että näkee tykkäykset 
def getlist():
	#result=database.session.execute("SELECT T.topic, T.createdat, U.username, T.messageids, T.id FROM Threads T, Users U ORDER BY T.id")
	result=database.session.execute("SELECT T.topic, T.createdat, U.username, T.messageids, T.id FROM Threads T, Users U ORDER BY T.id")
	return result.fetchall()

def getid(id):
	result=database.session.execute("SELECT topic FROM Threads WHERE id=:id", {"id":id})
	threadtopic=result.fetchone()[0]
	result2=database.session.execute("SELECT  message FROM Messages", {"threadid": id})
	messages=result2.fetchall()
	list=[threadtopic, messages]
	return list