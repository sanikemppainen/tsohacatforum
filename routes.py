from flask import render_template, request, redirect, sessions
from app import app
from os import getenv
import threads, users, messages


@app.route("/")
def frontpage():
	list=threads.getlist()
	return render_template("frontpage.html", threads=list)

@app.route("/send", methods=["POST"])
def send():
	content=request.form["content"]
	threadid=request.form["threadid"]
	userid=request.form["userid"]
	if messages.addmessage(content, threadid, userid):
		return redirect("/")
	else:
		return render_template("error.html", message="Couldn't send the message")


#@app.route("/send", methods=["POST"])
#def send():
#	topic=request.form["topic"]
#	if threads.send(topic):
#		return redirect("/")
#	else:
#		return render_template("error.html", message="Couldn't create a thread. Please make sure you are logged in.")

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

@app.route("/newthread")
def newthread():
	return render_template("newthread.html")


@app.route("/thread/<int:id>")
def thread(id):
	list=threads.getid(id)
	return render_template("thread.html", threadtopic=list[0], messages=list[1])

@app.route("/logout")
def logout():
	users.logout()
	return redirect("/")
