from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine, text
import os

db_connection_string = os.environ['DB_CONNECTION_STRING']
engine = create_engine(db_connection_string,
                       connect_args={
                           "ssl":{
                               "ssl_ca": "/etc/ssl/cert.pem"
                           }
                       })


app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("login.html")

@app.route("/", methods = ["POST"])
def login():
    data = request.form
    name1 = data["name"]
    password1 = data["password"]
    with engine.connect() as conn:
        result = conn.execute(text("SELECT Username, Userpassword FROM users WHERE Username='%s' AND Userpassword='%s' " % (name1, password1)))
        results = result.all()
        if len(results) == 1:
            print('Name found in database')
            return redirect("https://damdave.github.io/gdave")
        else:
            return redirect("/")


@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "POST":
        data = request.form
        name = data["name"]
        password = data["password"]
        email = data["email"]
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM users WHERE Userpassword='%s' " % password))
            results = result.all()
            if len(results) == 0:
                print('Name is stored in database')
                conn.execute(text("INSERT INTO users(Username, Userpassword, email) VALUES('%s', '%s', '%s')" % (name, password, email)))
            else:
                return redirect("/signup")

        return redirect("/")
    return render_template("signup.html")

if __name__=="__main__":
    app.run()
