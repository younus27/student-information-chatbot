from flask import Flask, render_template, url_for, request, session, redirect,jsonify, flash, session
import requests
import random

import json
import pymongo

import datetime

from aws_lex import get_response

app = Flask(__name__)
app.config['SECRET_KEY'] = "cclminiproject"


def format_chat(chat):

	chat = str(chat.replace("\t",''))
	chat = str(chat.replace("\\n",'\n'))
	chat = chat.split("\n")

	return chat

def calculate_br(chat):

	format_chat = str(chat.replace("\t",''))
	format_chat = str(format_chat.replace("\\n",'\n'))
	format_chat = format_chat.split("\n")

	slas_n = format_chat.count('')

	return max(len(chat)//45+ 1+(len(chat)//45+1)//3+1 +slas_n , len(format_chat))



mongo_uri = "<Your Mongo URI>"
mongo = pymongo.MongoClient(mongo_uri)
db = mongo["chatbot"]

@app.route("/")
def index():
	# if "user" in session:
	# 	return redirect(url_for("chat"))
	return render_template("index.html")


@app.route("/login/", methods = ["GET","POST"])
def login():
	if request.method == "POST":

		email = request.form["email"]
		password = request.form["password"]

		user = db.users.find_one({"email":email})
		if user:
			if user["password"] == password:
				session["user"] = user['email']

				history = user["history"]

				previous_login_date = user["previous_login_date"]
				current_date = str(datetime.datetime.now().strftime("%d/%m/%Y"))

				if current_date != previous_login_date:
					history.append({"date":current_date })
					db.users.update_one(
						{"email":email},
						{"$set":{
							"history" : history,
							"previous_login_date":current_date
							}
						})

				return redirect(url_for("chat"))

			flash("Invalid password!","warning")
			return redirect(url_for("login"))

		flash("User Not Found!","warning")
		return redirect(url_for("login"))
		
	else:
		if "user" in session:
			return redirect(url_for("chat"))
		return render_template("login.html")


@app.route("/signup/", methods = ["GET","POST"])
def signup():
	if request.method == "POST":

		if db.users.find_one({"email":request.form["email"]}):
			flash("Email already in use!","warning")
			return redirect(url_for("signup"))

		user = {
				"name"		: request.form["name"],
				"email"		: request.form["email"],
				"password"	: request.form["password"],
				"history"	: [],
				"current_chat": [],
				"previous_login_date": str(datetime.datetime.now().strftime("%d/%m/%Y")) + " [Signed Up]"
			}

		db.users.insert_one(user)
		
		flash("Signed up successfully!","info")
		return redirect(url_for("login"))

	else:
		
		if "user" in session:
			return redirect(url_for("user"))

		return render_template("signup.html")


@app.route("/chat/", methods = ["GET","POST"])
def chat():

	if "user" in session:
		email = session["user"]

		user = db.users.find_one({"email":email})
		name = user["name"]

		if request.method == "POST":
			if request.form["query"] != "":

				user_time = " ["+str(datetime.datetime.now()).split(" ")[1].split(".")[0][:-3]+"]"
				bot_resp = get_response(request.form["query"])
				bot_time = " ["+str(datetime.datetime.now()).split(" ")[1].split(".")[0][:-3]+"]"


				dict_= {
					"user": request.form["query"],
					"bot" :  bot_resp
				}

				# print(bot_resp)

				dict_history= {
					"user": request.form["query"]+user_time,
					"bot" :  bot_resp+bot_time
				}

				history = user["history"]
				history.append(dict_history)

				current_chat = user["current_chat"]
				current_chat.append(dict_)


				db.users.update_one(
					{"email":email},
					{"$set":{
						"history" : history,
						"current_chat" : current_chat,
						}
					})

		current_chat = user["current_chat"]

		
		cc = []
		for chat in current_chat:

			cc.append(
				{"__message__" : format_chat(chat["user"]),
				"__br__" : calculate_br(chat["user"]),
				"__class__": "view_person"})

			print( calculate_br(chat["bot"]) )
			print( format_chat(chat["bot"]) )

			cc.append(
				{"__message__" :format_chat(chat["bot"]),

				"__br__" :calculate_br(chat["bot"]) ,
				"__class__": "view_bot"})

		# print("\n\ncc:\n",cc,"\n\n")

		return render_template("chatbot.html" ,current_chat = cc, user = name)

	else:
		flash("Please Login first","info")
		return redirect(url_for("login"))



@app.route("/history/")
def history():

	if "user" in session:
		email = session["user"]

		user = db.users.find_one({"email":email})
		name = user["name"]

		history = user["history"]

		
		cc = []
		for chat in history:

			try:
				cc.append(
					{"__message__" : format_chat(chat["user"]),
					"__br__" :  calculate_br(chat["user"]),
					"__class__": "view_person"})

				cc.append(
					{"__message__" : format_chat(chat["bot"]),
					"__br__" : calculate_br(chat["bot"]),
					"__class__": "view_bot"})
			except:
				cc.append(
					{"__date__" : chat["date"],
					"__class__": "date"}
					)

		# print("\n\ncc\n")
		# print(cc)

		return render_template("history.html" ,current_chat = cc, user = name)

	else:
		flash("Please Login first","info")
		return redirect(url_for("login"))


@app.route("/logout/")
def logout():
	if "user" in session:
		email = session["user"]

		user = db.users.find_one({"email":email})
		name = user['name']
		
		db.users.update_one({'email':email},
			{"$set":{
				"current_chat" : []
			}})

		flash(f"You have been Logged out, {name}","info")

	session.pop("user",None)
	return redirect(url_for("login"))


@app.route("/about/")
def about():
	return render_template("about.html")

@app.route("/help/")
def help():
	return render_template("help.html")

if __name__ == "__main__":
	app.run(debug=False)






























