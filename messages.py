"""Messages to and from database"""

from database import database
import users
import threads
import photos


def add_message_to_thread(message, id, pictureid):
    #adding message to thread and checking if a picture is associated with the message
    userid = users.get_user_id()
    if pictureid is not None:
        picturename = photos.get_picture_name(pictureid)
        picturedata = photos.get_data(picturename)
    if pictureid is None:
        picturedata = None
    threadid = id
    userid = users.get_user_id()
    if userid == 0:
        return False
    getusername = database.session.execute(
        "SELECT username FROM Users WHERE id=:userid", {"userid": userid})
    username = getusername.fetchone()[0]
    database.session.execute(
        "INSERT INTO Messages (message, userid, threadid, username, sentat, pictureid, picturedata)\
            VALUES (:message, :userid, :threadid, :username, NOW(), :pictureid, :picturedata)", {
                "message": message, "userid": userid, "threadid": threadid, "username": username,
                "pictureid": pictureid, "picturedata": picturedata})
    database.session.commit()
    return True


def get_messages(threadid):
    messagesinthread = database.session.execute(
        "SELECT M.* FROM MESSAGES M WHERE M.threadid=:threadid) ORDER BY sentat ASC", {
            "threadid": threadid}).fetchall()
    return messagesinthread


def delete_message(id):
    try:
        database.session.execute(
            "DELETE FROM Messages WHERE id=:id ", {"id": id})
        database.session.commit()
        return True
    except:
        return False


def search_messages(query):
    sql = "SELECT threadid, message FROM messages WHERE message LIKE :query"
    result = database.session.execute(sql, {"query": "%"+query+"%"})
    messages = result.fetchall()
    return messages


def get_most_messages():
    #finds thread with most messages
    sql = "SELECT threadid FROM messages GROUP BY threadid ORDER BY COUNT(*) DESC LIMIT 1"
    result = database.session.execute(sql)
    mostmessages = result.fetchone()[0]
    mostmessagestopic = threads.get_topic_by_id(mostmessages)
    return mostmessagestopic
