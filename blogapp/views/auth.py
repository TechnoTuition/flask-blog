import secrets
import os
from blogapp import app
from flask import render_template
from flask import request
from flask import redirect,url_for
from flask import flash
from blogapp import db
from blogapp.schema.user import User
from blogapp import bcrypt
from flask_login import login_required,login_user,current_user,logout_user

@app.route("/signup",methods=['GET','POST'])
def user_signup():
    if current_user.is_authenticated:
        flash("You have already Signup ","danger")
        return redirect(url_for("user_profile"))
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        
        user = User.query.filter_by(email=email).first()
        if user:
            
            flash("Email account already exist","danger")
            return redirect(url_for("user_login"))
            
        else:
            hash_pass = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username,email=email,password=hash_pass)
            db.session.add(new_user)
            db.session.commit()
            flash("Your account hase been created ","info")
            return redirect(url_for("user_login"))
    return render_template("auth/signup.html")
    


@app.route("/login",methods=['GET','POST'])
def user_login():
    if current_user.is_authenticated:
        flash("You have already Logged in","danger")
        return redirect(url_for("user_account"))
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
       
        if user and bcrypt.check_password_hash(user.password,password):
            login_user(user,remember=True)
            flash("You are Successfully logged in","info")
            return redirect(url_for("user_account"))
        else:
            flash("email or password dose not match ","danger")
          #  return redirect(url_for("user_signup"))
        

    return render_template("auth/login.html")

@app.route("/account")
@login_required
def user_account():
    
    return render_template("auth/account.html",name=current_user)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You are Successfully Logout ","info")
    return redirect(url_for("user_login"))
    
#--------------////--------------#   
def image_save(image):
    random_hex = secrets.token_hex(8)
    _,f_ext = os.path.splitext(image.filename)
    pic_fn = random_hex + f_ext
  #  print(profile_fn)
    picture_path = os.path.join(app.root_path,'static/profile_pics',pic_fn)
    image.save(picture_path)
    return pic_fn
    
@app.route("/account/profile",methods= ['GET','POST'])
@login_required
def user_profile():
    if request.method == 'POST':
        pics = request.files['pics']
        picture_file = image_save(pics)
        current_user.image_file = picture_file
        db.session.commit()
       # print(pics)
    image_file = url_for('static',filename=f"profile_pics/{current_user.image_file}")
    return render_template("auth/profile.html",user=current_user,image_file=image_file)