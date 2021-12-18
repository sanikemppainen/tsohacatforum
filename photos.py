from flask import session
from flask.helpers import make_response
from database import database
from base64 import b64decode, b64encode
from zlib import compress, decompress

def addphoto(name, data):
    database.session.execute("INSERT INTO Pictures (name, data) VALUES (:name, :data)", {"name":name, "data": data})
    database.session.commit()
    return True

def showphoto(name):
    result=database.session.execute("SELECT data FROM Pictures WHERE name=:name", {"name":name})
    data=result.fetchone()[0]
    #image=make_response(bytes(data))
    #data.headers.set("Content-Type", "image/jpeg")
    data=compress(data)
    retunable= b64encode(decompress(data)).decode("utf-8")
    return retunable

def getpictureid(name):
    result=database.session.execute("SELECT id FROM Pictures WHERE name=:name", {"name":name})
    id=result.fetchone()[0]
    return id

def getpicturename(pictureid):
    id=pictureid
    result=database.session.execute("SELECT name FROM Pictures WHERE id=:id", {"id":id})
    name=result.fetchone()[0]
    return name