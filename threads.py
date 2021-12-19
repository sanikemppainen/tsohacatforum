"""Creating, updating and deleting threads, getting and putting data on threads to database"""

from flask import session
from database import database
import users
import messages


def send(topic, tags, message, username, pictureid):
    # jos threadia ei vielä ole, luo uusi ja lähetä sinne eka viesti
    userid = users.get_user_id()
    if userid == 0:
        return False
    tags = tags
    username = username
    preview = message[:100]+(message[100:] and "...")
    database.session.execute("INSERT INTO threads (topic, userid, username, createdat, tags, preview) VALUES (:topic, :userid, :username, NOW(), :tags, :preview)", {
                             "topic": topic, "userid": userid, "username": username, "tags": tags, "preview": preview})
    database.session.commit()
    getthreadid = database.session.execute(
        "SELECT id FROM Threads WHERE topic=:topic", {"topic": topic})
    threadid = getthreadid.fetchone()[0]
    messages.add_message_to_thread(message, threadid, pictureid)
    return True


def get_list():
	#return a list of all of the threads
    sql = "SELECT id, topic, username, createdat, tags, preview FROM Threads ORDER BY id DESC"
    results = database.session.execute(sql)
    allthreads = results.fetchall()
    return allthreads


def get_thread_by_id(id):
	#return a thread topic and messages associated with given thread id
    result = database.session.execute(
        "SELECT topic, id FROM Threads WHERE id=:id", {"id": id})
    threadtopic = result.fetchone()[0]
    result2 = database.session.execute(
        "SELECT message, username, sentat, picturedata FROM Messages WHERE Messages.threadid =:id ORDER BY id ASC", {"id": id})
    messages = result2.fetchall()
    list = [threadtopic, messages]
    return list


def get_thread_id():
    return session.get("threadid", 0)


def get_tags():
    results = database.session.execute("SELECT tags FROM Threads")
    alltags = results.fetchall()
    return alltags


def delete_thread(topic):
    try:
        database.session.execute(
            "DELETE FROM Threads WHERE topic=:topic", {"topic": topic})
        database.session.commit()
        return True
    except:
        return False


def search_by_threads(query):
    sql = "SELECT id, topic FROM Threads WHERE topic LIKE :query"
    result = database.session.execute(sql, {"query": "%"+query+"%"})
    threads = result.fetchall()
    return threads


def search_by_tags(query):
    sql = "SELECT id, tags, topic FROM Threads WHERE tags LIKE :query"
    result = database.session.execute(sql, {"query": "%"+query+"%"})
    tags = result.fetchall()
    return tags


def get_topic_by_id(id):
    sql = "SELECT id, topic FROM Threads WHERE id=:id"
    results = database.session.execute(sql, {"id": id})
    topic = results.fetchall()
    return topic
