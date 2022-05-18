import csv
import os
import smtplib
from sqlite3 import register_converter
from flask import Flask, redirect, render_template, request
import textwrap
app=Flask(__name__)

# stores all the students
students = []
WORDS = []
with open("large.txt", "r") as file:
    for line in file.readlines():
        WORDS.append(line.rstrip())

@app.route("/")
def index():
    # sort of like get from dictionary where secondary parameter is value if key not found
    name = request.args.get('name', "Rafee") 

    return render_template("index.html", name=name)

@app.route("/registrants")
def registrants():
    return render_template("registered.html", students=students)

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    email = request.form.get("email")
    dorm = request.form.get("dorm")

    if not dorm or not name:
        return render_template("failure.html")
    file = open("templates/registered.csv", "a")
    writer = csv.writer(file)
    writer.writerow((name, email, dorm))
    file.close() 
    Gmail_Email = 'rafeeali21@gmail.com'
    Gmail_password = 'ndudrdubnrykntmq' 
    send_to = ['rafeali21@gmail.com', 'history.geo12@gmail.com', 'hotcars431@gmail.com']
    # message = "You Are logged !"
    # subject = "Wow that\'t kinda awesome"
    file = open("registered.csv", "a")
    body = textwrap.dedent("\n Request is complete \n Thank You \n Rafee Ali")
    email_text = """\
    From: %s
    To: %s


    %s
    """ % (Gmail_Email, ",".join(send_to), body)
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(Gmail_Email, Gmail_password)
        server.sendmail(Gmail_Email, send_to, email_text)
        students.append(f"{name} from {dorm}")
        server.close()
        return redirect("/registrants")
    except:
        return render_template("failure.html")
    # return redirect(f"http://www.{name}.com", code=303)

@app.route("/registered")
def registered():
    with open(registered.csv, "r") as file:
        reader = csv.reader(file)
        students = list(reader)
    return render_template("registered.html", students=students)

@app.route("/search")
def search():
    q = request.args.get("q")       
    words = [word for word in WORDS if q and word.startswith(q)]
    return render_template("search.html",words=words)

