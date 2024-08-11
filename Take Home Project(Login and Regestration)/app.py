"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from telnetlib import STATUS
from flask import Flask, request, render_template, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key="mykey"
mydb=mysql.connector.connect(host="localhost", user="root", password="1qaz@", database="mydatabase")
mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS user1 (id INT AUTO_INCREMENT PRIMARY KEY , username VARCHAR(255), password INT(255))")
# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

@app.route('/')
def home():    
    """Renders a sample page."""
    if "username" in session:
        return render_template("index.html", user=session["username"], list=list)
    else:
       return render_template("login.html")

@app.route('/login', methods=["POST", "GET"])
def login():
   if request.method == "POST":
      username = request.form.get("username")
      password = request.form.get("password")
      sql = "SELECT username FROM user1 WHERE username = %s AND password = %s"
      values = [username, password]
      mycursor.execute(sql, values)
      result = mycursor.fetchall()
      if len(result) > 0:
         session["username"] = username
         return redirect("/")
      else:
         return render_template("login.html", message = "Wrong username or password")
   else:
      return render_template("login.html")
  
@app.route('/logout')
def logout():
     session.pop("username", None)
     return render_template("login.html")
  
@app.route('/register', methods=["POST", "GET"])
def register():
   if request.method == "POST":
      username = request.form.get("username")
      password = request.form.get("password")
      confirm_password = request.form.get("confirm-password")
      if password != confirm_password:
         return render_template("register.html", message = "Passwords don't match")
      sql = "SELECT username FROM user1 WHERE username = %s"
      values = [username, ]
      mycursor.execute(sql, values)
      result = mycursor.fetchall()
      if len(result) > 0:
         return render_template("register.html", message = "username already given")
      else:
         sql = "INSERT INTO user1(username, password) VALUES(%s, %s)"
         values = [username, password]
         mycursor.execute(sql, values)
         mydb.commit()
         session["username"] = username
         return redirect("/")
   else:
     return render_template("register.html")
          
if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)