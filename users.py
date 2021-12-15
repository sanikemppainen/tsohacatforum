from flask import session
from database import database
from werkzeug.security import check_password_hash, generate_password_hash

def userid():
    return session.get("userid",0)

#def getusername():
#    return session.get["username"]

def login(username, password):
    result=database.session.execute("SELECT id, username, password, admin FROM Users WHERE username=:username", {"username":username})
    user=result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["userid"]=user.id
            session["admin"]=user.admin
            session["username"]=user.username
            #session["csrf_token"]=secrets.token_hex(16)
            #csfr token
            return True
        else:
            return False

def register(username, password):
    hashpassword = generate_password_hash(password)
    if username=="adm":
        database.session.execute("INSERT INTO Users (username,password, admin) VALUES (:username,:password, 1)", {"username":username, "password":hashpassword})
        database.session.commit()
    else:
        try:
            database.session.execute("INSERT INTO Users (username,password, admin) VALUES (:username,:password, 0)", {"username":username, "password":hashpassword})
            database.session.commit()
        except:
            return False
        return login(username, password)

def admincheck():
    if userid()!=0:
        if session["admin"]==1:
            return True
    return False

def logout():
    del session["userid"]
    #del session["username"]
    #del session["admin"]
    #del session["csrf_token"]