"""Photos to and from database, decompressing photo data"""

from base64 import b64encode
from zlib import compress, decompress
from database import database

def add_photo(name, data):
    database.session.execute("INSERT INTO Pictures (name, data) VALUES (:name, :data)", {
        "name": name, "data": data})
    database.session.commit()
    return True


def get_data(name):
    result = database.session.execute(
        "SELECT data FROM Pictures WHERE name=:name", {"name": name})
    data = result.fetchone()[0]
    data = compress(data)
    retunable = b64encode(decompress(data)).decode("utf-8")
    return retunable


def get_picture_id(name):
    result = database.session.execute(
        "SELECT id FROM Pictures WHERE name=:name", {"name": name})
    id = result.fetchone()[0]
    return id


def get_picture_name(pictureid):
    id = pictureid
    result = database.session.execute(
        "SELECT name FROM Pictures WHERE id=:id", {"id": id})
    name = result.fetchone()[0]
    return name
