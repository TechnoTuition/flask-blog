from blogapp import app
from blogapp.schema.user import User
from flask import render_template

@app.route("/")
def home():
    #user = User.query.all()
    return render_template("home/index.html")

@app.route("/about")
def about():
    return "ABOUT"
