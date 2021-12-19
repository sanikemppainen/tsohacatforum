"""Registering new users, checking login credentials, importing and exporting data from database relating to users"""

import secrets
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from database import database


def get_user_id():
    return session.get("userid", 0)


def check_user_exists(username):
    result = database.session.execute(
        "SELECT id, username, password, admin FROM Users WHERE username=:username", {"username": username})
    user = result.fetchone()
    if not user:
        return False
    return True


def login(username, password):
    session["csrf_token"] = secrets.token_hex(16)
    result = database.session.execute(
        "SELECT id, username, password, admin FROM Users WHERE username=:username", {"username": username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["userid"] = user.id
            session["admin"] = user.admin
            session["username"] = user.username
            return True
        else:
            return False


def register(username, password):
    hashpassword = generate_password_hash(password)
    if username == "adm":
        database.session.execute("INSERT INTO Users (username,password, admin) VALUES (:username,:password, 1)", {
                                 "username": username, "password": hashpassword})
        database.session.commit()
    else:
        try:
            database.session.execute("INSERT INTO Users (username,password, admin) VALUES (:username,:password, 0)", {
                                     "username": username, "password": hashpassword})
            database.session.commit()
        except:
            return False
    return login(username, password)


def admin_check():
    if get_user_id() != 0:
        if session["admin"] == 1:
            return True
    return False


def logout():
    del session["userid"]
    del session["username"]
    del session["admin"]
    del session["csrf_token"]
    del session["number"]


def delete_user(username):
    try:
        database.session.execute("DELETE FROM Users WHERE username=:username", {
                                 "username": username})
        database.session.commit()
        return True
    except:
        return False
