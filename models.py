from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import os
from main import app
from werkzeug.security import generate_password_hash
import datetime

db = SQLAlchemy(app)

def migrate():
    with app.app_context():
        db.create_all()




class UserProfile(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    bio=db.Column(db.Text,nullable=True)
    user=db.relationship("User",back_populates='profile')
    user_id=db.Column(db.Integer, db.ForeignKey("Blog users.id"))

    
class Comment(db.Model):
    __tablename__ = "comments"
    id= db.Column(db.Integer, primary_key=True)
    text=db.Column(db.String(250), nullable=False)
    # ///// one to many ralatioship (post to comments)////
    post=db.relationship("BlogPost",back_populates='comments')
    post_id=db.Column(db.Integer, db.ForeignKey('Blog Posts.id'))

    # ///// one to many ralatioship (user to comments)////
    author=db.relationship("User",back_populates='comments')
    author_id=db.Column(db.Integer, db.ForeignKey('Blog users.id'))





class BlogPost(db.Model):
    __tablename__="Blog Posts"
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String,nullable=False)
    subtitle=db.Column(db.String,nullable=False)
    img_url=db.Column(db.String,nullable=False)
    date=db.Column(db.String,nullable=False)
    content=db.Column(db.Text,nullable=False)
    # ///// one to many ralatioship (posts to User)////
    author=db.relationship("User",back_populates="posts",)
    author_id=db.Column(db.Integer,db.ForeignKey('Blog users.id'))
    
    # ///// one to many ralatioship (post to comments)////
    comments=db.relationship("Comment",back_populates='post')




class User(UserMixin,db.Model):
    __tablename__= "Blog users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String,unique=True, nullable=False)
    phone=db.Column(db.Integer, nullable=False)
    first_name=db.Column(db.String, nullable=False)
    last_name=db.Column(db.String, nullable=False)
    password=db.Column(db.String, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True,)
    paid=db.Column(db.Boolean,nullable=False,default=False)
    # ///// one to many ralatioship (posts to User)////
    posts=db.relationship("BlogPost",back_populates="author")
    
    # ///// one to many ralatioship (user to comments)////
    comments=db.relationship("Comment",back_populates='author')
    
    # ///// one to many ralatioship (user to profile)////
    profile=db.relationship("UserProfile",back_populates='user')




    def __init__(self, email, password, confirmed,first_name,last_name,phone,username,
                 paid=False, admin=False, confirmed_on=None):
        self.email = email
        
        self.password = generate_password_hash(password=password,method=os.environ.get('SECURITY_PASSWORD_SALT'),
                                               salt_length=int(os.environ.get('SALT_ROUNDS')))
        self.registered_on = datetime.datetime.now()
        self.admin = admin
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on
        self.first_name=first_name.title()
        self.last_name=last_name.title()
        self.phone=phone
        self.username=username
        self.paid=paid
        

    def __str__(self):
        return self.username




migrate()