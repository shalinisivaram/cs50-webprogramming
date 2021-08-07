import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash




app=Flask(__name__)
app.secret_key='booking'

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db=SQL("sqlite:///salon.db")

@app.route("/")
def index():

        return render_template("index.html")





@app.route("/register", methods=["GET","POST"])
def register():
    error=None
    if request.method == "POST":

         salonname=request.form.get("salonname")
         username=request.form.get("username")
         password=request.form.get("password")
         confirmation=request.form.get("confirmation")
         address=request.form.get("address")
         city=request.form.get("city")

         rows= db.execute("SELECT * FROM salon WHERE username=?",username)

         if not salonname:
             error ='salonname required'

         elif len(rows) != 0:
             error ='usernname already exist'

         elif not username:
             error ='username required'

         elif not password:
             error ='password required'

         elif not confirmation:
             error ='enter password again'

         elif password != confirmation:
             error = 'password not matching'

         elif not address:
             error ='address required'

         elif not city:
             error ='choose your city'

         else:
             db.execute("INSERT INTO salon (salonname,username,hash,address,city) VALUES (?,?,?,?,?)",salonname,username,generate_password_hash(request.form.get("password")),address,city)
             return redirect("/")
         return render_template('register.html', error=error)

    else:
        return render_template("register.html")

@app.route("/booking", methods=["GET","POST"])

def booking():
    if request.method =="POST":
      salon=request.form.get("salon")
      gender=request.form.get("gender")
      date=request.form.get("date")
      time=request.form.get("time")
      name=request.form.get("name")
      mobilenumber=request.form.get("tel")
      service=request.form.getlist("service")
      services = ','.join(service)



      db.execute("INSERT INTO user (name,salonname,gender,date,time,mobilenumber,service) VALUES (?,?,?,?,?,?,?)",name,salon,gender,date,time,mobilenumber,services)
      return redirect("/success")

    else:
        salons=db.execute("SELECT salonname,address FROM salon")
        return render_template("booking.html",salons=salons)

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            error = 'enter username'

        elif not request.form.get("password"):
            error = "enter password"
            return render_template("login.html", error=error)
        rows = db.execute("SELECT * FROM salon where username = ?", request.form.get("username"))

        if len(rows)!=1 or not check_password_hash(rows[0]["hash"],request.form.get("password")):
            error = "invalid username / password"
            return render_template("login.html", error=error)

        else:
            session["name"] = request.form.get("username")
            return redirect ("/appoinment")

    else:
            return render_template("login.html")

@app.route("/appoinment")
def appoinment():
    salonname = db.execute("SELECT salonname FROM salon where username= ?", session["name"])
    salonname = salonname[0]['salonname']
    users=db.execute("SELECT * FROM user WHERE salonname = ?", salonname)
    return render_template("appoinment.html",users=users)