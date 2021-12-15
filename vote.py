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
    print (result)
    if result!="":
        return True
    return False
