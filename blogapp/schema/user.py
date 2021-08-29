from blogapp import db
from blogapp import login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
    
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(20),unique=False,nullable=False)
    image_file = db.Column(db.String(20),nullable=False,default='default.jpg')
    post  = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"{self. username},{self.email},{self.password}"
class Post(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    post_created = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    content = db.Column(db.String(5000),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    def __repr__(self):
        return f"{self.title},{self.post_created},{self.content},{self.user_id}"