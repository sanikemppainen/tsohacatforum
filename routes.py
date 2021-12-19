"""Routes to requests"""

from flask import render_template, request, redirect, session, abort
from app import app
import threads
import users
import messages
import votes
import photos


@app.route("/", methods=["GET", "POST"])
def frontpage():
	#displays frontpage, checks csrf, gets list of threads to display
    list = threads.get_list()
    count = len(list)
    mostmessages = messages.get_most_messages()
    if session.get("number") == None:
        session["number"] = 10
        number = 10
    else:
        number = session["number"]
    newlist = []
    n = 0
    for i in list:
        if n < int(number):
            newlist.append(i)
            n = n+1
    if len(list) > len(newlist):
        showmore = "... change number of threads shown on page to see more"
    else:
        showmore = ""
    return render_template("frontpage.html", threads=newlist, count=count, mostmessages=mostmessages, showmore=showmore)


@app.route("/send", methods=["POST"])
def send():
	#responds to message being sent to a thread
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    content = request.form["content"]
    threadid = request.form["threadid"]
    username = request.form["username"]
    if messages.addmessage(content, threadid, username):
        return redirect("/")
    else:
        return render_template("error.html", message="Couldn't send the message")


@app.route("/login", methods=["GET", "POST"])
def login():
	#logging in users and checking given data
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Wrong username or password, please try again or make a new account")


@app.route("/register", methods=["GET", "POST"])
def register():
	#registers users and checking given data
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        passwordagain = request.form["passwordagain"]
        if password != passwordagain:
            return render_template("error.html", message="Passwords don't match")
        if users.register(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Registeration failed, try again")


@app.route("/newthread", methods=["GET", "POST"])
def newthread():
	#start a new thread by sending message to it
    if request.method == "GET":
        taglist = threads.get_tags()
        return render_template("newthread.html", taglist=taglist)
    else:
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        tags = request.form.get("tag")
        threadtopic = request.form["threadtopic"]
        threadmessage = request.form["threadmessage"]
        username = session.get("username")
		#check if photo is given
        photo = request.files["photo"]
        name = photo.filename
        pictureid = None
        if name != "":
            if not name.endswith(".jpg"):
                return render_template("error.html", message="Invalid filename. You can only send .jpg files")
            data = photo.read()
            if len(data) > 1000*1024:
                return render_template("error.html", message="The file is too big")
            photos.add_photo(name, data)
            pictureid = photos.get_picture_id(name)
        threads.send(threadtopic, tags, threadmessage, username, pictureid)
        return redirect("/")


@app.route("/thread/<int:id>", methods=["GET", "POST"])
def thread(id):
	#sending a message to an existing thread
    if request.method == "GET":
        list = threads.get_thread_by_id(id)
        return render_template("thread.html", threadtopic=list[0], messages=list[1], threadid=id)
    else:
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        sentmessage = request.form["sentmessage"]
        threadid = id
        photo = request.files["photo"]
        name = photo.filename
        pictureid = None
        print(pictureid)
        print("eka yllä")
        if name != "":
            if not name.endswith(".jpg"):
                return render_template("error.html", message="Invalid filename. You can only send .jpg files")
            data = photo.read()
            if len(data) > 1000*1024:
                return render_template("error.html", message="The file is too big")
            photos.add_photo(name, data)
            pictureid = photos.get_picture_id(name)
            print(pictureid)
        messages.add_message_to_thread(sentmessage, threadid, pictureid)
        list = threads.get_thread_by_id(id)
        return render_template("thread.html", threadtopic=list[0], messages=list[1], threadid=id)


@app.route("/sendphoto", methods=["POST"])
def sendphoto():
	#collecting data on sent photo
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    photo = request.files["photo"]
    name = photo.filename
    if not name.endswith(".jpg"):
        return render_template("error.html", message="Invalid filename. You can only send .jpg files")
    data = photo.read()
    if len(data) > 100*1024:
        return render_template("error.html", message="The file is too big")
    if photos.add_photo(name, data):
        response = photos.get_data(name)
    else:
        return render_template("error.html", message="Error in adding photo")
    return render_template("thread.html")


@app.route("/logout")
def logout():
    if users.get_user_id() == 0:
        return render_template("error.html", message="Can't logout before logging in")
    else:
        users.logout()
        return render_template("logout.html")


@app.route("/admin", methods=["GET", "POST"])
def admin():
    # checks if user has admin rights and displays admin page
    if request.method == "GET":
        if users.admin_check():
            return render_template("admin.html", message="All access granted. Now you can delete stuff.")
        else:
            return render_template("error.html", message="No rights here")
    # collects data on what to delete
    else:
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        username = request.form["username"]
        thread = request.form["thread"]
        if username != "":
            users.delete_user(username)
        if thread != "":
            threads.delete_thread(thread)
        return redirect("/delete")


@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        if session["csrf_token"] is not request.form["csrf_token"]:
            abort(403)
    return render_template("admin.html", message="Deleted succesfully")


@app.route("/vote", methods=["GET", "POST"])
def vote():
	#collect voting results and displays results
    if request.method == "GET":
        return render_template("vote.html")
    else:
        if "answer" in request.form:
            nameofphoto = request.form["answer"]
            list = votes.add_votes(nameofphoto)
            photourl = f"{list[0].nameofphoto}.jpg"
        return render_template("result.html", list=list, photourl=photourl)


@app.route("/searchresult")
def result():
	#gets and displays search results
    query = request.args["query"]
    foundmessages = messages.search_messages(query)
    foundthreads = threads.search_by_threads(query)
    foundtags = threads.search_by_tags(query)
    return render_template("searchresult.html", foundtags=foundtags, foundmessages=foundmessages, foundthreads=foundthreads, query=query)


@app.route("/selectnumber", methods=["POST"])
def selectnumber():
	#how many threads shown on frontpage
    number = request.form["number"]
    session["number"] = number
    return redirect("/")
