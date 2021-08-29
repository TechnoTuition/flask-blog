from blogapp import app
from blogapp import db
from blogapp.schema.user import User,Post
from flask import render_template,request,flash
from flask import redirect,url_for
from flask_login import login_required,current_user

@app.route("/post",methods=['GET','POST'])
@login_required
def blog():
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        if not title:
            flash("Title dose not empty","danger")
            return redirect(url_for("blog"))
        elif not content:
            flash("Content dose not empty","danger")
            return redirect(url_for("blog"))
        else:
            post = Post(title=title,content=content,user_id=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("Post hase been created","info")
            return redirect(url_for("user_account"))
    return render_template("blog/write_post.html")
@app.route("/delete/<int:post_id>",methods=['GET','POST'])
@login_required
def post_delete(post_id):
    print(post_id)
    post = Post.query.filter_by(id=post_id).first()
    db.session.delete(post)
    db.session.commit()
    flash("you are successfully delete post ","info")
    return redirect("/account")


@app.route("/edit/<int:id>",methods=['GET','POST'])
@login_required
def edit_post(id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        post = Post.query.filter_by(id=id).first()
        post.title = title
        post.content = content
        db.session.add(post)
        db.session.commit()
        flash("Your post hase been update","info")
        return redirect("/account")
    post = Post.query.filter_by(id=id).first()
    return render_template("blog/edit_post.html",allpost=post)