from flask import session
from database import database
from werkzeug.security import check_password_hash, generate_password_hash

def userid():
    return session.get("userid",0)

def login(username, password):
    result=database.session.execute("SELECT id, password FROM Users WHERE username=:username", {"username":username})
    user=result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["userid"]=user.id
            return True
        else:
            return False

def register(username, password):
    hashpassword = generate_password_hash(password)
    try:
        database.session.execute("INSERT INTO Users (username,password) VALUES (:username,:password)", {"username":username, "password":hashpassword})
        database.session.commit()
    except:
        return False
    return login(username, password)

def logout():
    del session["userid"]