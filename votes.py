from flask import session
from database import database

def putvotes(nameofphoto):
    #if exists not
    if checkifrowexists(nameofphoto):
        database.session.execute("UPDATE Votes SET votes=votes+1 WHERE nameofphot0=:nameofphoto", {"nameofphoto": nameofphoto})
        database.session.commit()
    database.session.execute("INSERT INTO Votes (nameofphoto, votes) VALUES (:nameofphoto, 1)", {"nameofphoto":nameofphoto})
    database.session.commit()

def checkifrowexists(nameofphoto):
    result=database.session.execute("SELECT nameofphoto FROM Votes WHERE nameofphoto=:nameofphoto", {"nameofphoto":nameofphoto})
    if result==None:
        return False
    return True

def addvotes(nameofphoto):
    getvotes=database.session.execute("SELECT votes FROM Votes WHERE nameofphoto=:nameofphoto", {"nameofphoto":nameofphoto})
    getvotesresult=getvotes.fetchone()[0]
    if getvotesresult==None:
        votes=1
    else:
        votes=getvotesresult+1
    if checkifrowexists(nameofphoto):
        database.session.execute("UPDATE Votes SET votes=:votes WHERE nameofphoto=:nameofphoto", {"nameofphoto": nameofphoto, "votes":votes})
        database.session.commit()
    else:
        sql="INSERT INTO Votes (nameofphoto, votes) VALUES (:nameofphoto, :votes)"
        database.session.execute(sql,{"nameofphoto":nameofphoto, "votes":votes})
        database.session.commit()
        #eniten
    
    row=database.session.execute("SELECT nameofphoto, votes FROM Votes WHERE votes=(SELECT MAX(votes) FROM Votes)")
    returnrow=row.fetchall()
    return returnrow
    