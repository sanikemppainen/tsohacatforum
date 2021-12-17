from logging import error
from flask import render_template, request, redirect, session, url_for
from app import app
from os import getenv
import threads, users, messages, vote, database


@app.route("/")
def frontpage():
	list=threads.getlist()
	count=len(list)
	mostmessages=messages.getmostmessages()
	print(mostmessages)
	return render_template("frontpage.html", threads=list, count=count, mostmessages=mostmessages)

@app.route("/send", methods=["POST"])
def send():
	content=request.form["content"]
	threadid=request.form["threadid"]
	username=request.form["username"]
	if messages.addmessage(content, threadid, username):
		return redirect("/")
	else:
		return render_template("error.html", message="Couldn't send the message")

@app.route("/login", methods=["GET","POST"])
def login():
	if request.method=="GET":
		return render_template("login.html")
	else:
		username=request.form["username"]
		password=request.form["password"]
		if users.login(username, password):
			return redirect("/")
		else:
			return render_template("error.html", message="Wrong username or password, please try again or make a new account")

@app.route("/register", methods=["GET","POST"])
def register():
	if request.method=="GET":
		return render_template("register.html")
	else:
		username=request.form["username"]
		password=request.form["password"]
		passwordagain=request.form["passwordagain"]
		if password!=passwordagain:
			return render_template("error.html", message= "Passwords don't match")
		if users.register(username, password):
			return redirect ("/")
		else:
			return render_template("error.html", message="Registeration failed, try again")

@app.route("/newthread", methods=["GET", "POST"])
def newthread():
	if request.method=="GET":
		taglist=threads.gettags()
		return render_template("newthread.html", taglist=taglist)
	else:
		#ota tiedot, lisää threads databaseen, ohjaa etusivulle
		#newtag=request.form["newtag"]
		#if newtag!="":
		#	tags=newtag
		#else:
		tags=request.form.get("tag")
		threadtopic=request.form["threadtopic"]
		threadmessage=request.form["threadmessage"]
		username=session.get("username")
		threads.send(threadtopic, tags, threadmessage, username)
		return redirect("/")	

@app.route("/thread/<int:id>", methods=["GET", "POST"])
def thread(id):
	if request.method=="GET":
		list=threads.getid(id)
		return render_template("thread.html", threadtopic=list[0], messages=list[1], threadid=id)
	else:
		#if liian pitkä kato osa 4 älä laita viestiä databaseewn
		#check sentmessage ja topic
		sentmessage=request.form["sentmessage"]
		threadid=id
		messages.addmessagetothread(sentmessage, threadid)
		list=threads.getid(id)		
		return render_template("thread.html", threadtopic=list[0], messages=list[1], threadid=id)

@app.route("/logout")
def logout():
	if users.userid()==0:
		return render_template("error.html", message="Can't logout before logging in")
	else:
		users.logout()
		return render_template("logout.html")

@app.route("/admin", methods=["GET", "POST"])
def admin():
	#checks if user has admin rights and displays admin page 
	if request.method=="GET":
		if users.admincheck():
			return render_template("admin.html", message="All access granted. Now you can delete stuff.")
		else:
			return render_template("error.html", message="no rights here")
	#collects info on what to delete and send that info as render template to delete page 
	else:
		username=request.form["username"]
		thread=request.form["thread"]
		if username !="":
			users.deleteuser(username)
		if thread !="":
			threads.deletethread(thread)
		return redirect("/delete")

@app.route("/delete", methods=["GET", "POST"])
def delete():
	return render_template("admin.html", message="Deleted succesfully or wrong info")

@app.route("/vote", methods=["GET", "POST"])
def vote():
	if request.method=="GET":
		return render_template("vote.html")
	else:
		nameofphoto=request.form["answer"]

		#vote.putvotes(nameofphoto)
		#get name, votes, photo url siihen if votes eniten 1 2 3 4 niin tallenna sen url tuohon muuttujaaan

		return render_template("result.html", votes="votes", nameofphoto="nameofphoto", photourl="photourl")
		
@app.route("/searchresult")
def result():
	query = request.args["query"]
	foundmessages=messages.searchmessages(query)
	foundthreads=threads.searchthreads(query)
	foundtags=threads.searchtags(query)
	return render_template("searchresult.html", foundtags=foundtags, foundmessages=foundmessages, foundthreads=foundthreads, query=query)
