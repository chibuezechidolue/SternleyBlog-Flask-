from flask_sqlalchemy import SQLAlchemy
import os
from main import app
from werkzeug.security import generate_password_hash
import datetime

db = SQLAlchemy(app)


class User(db.Model):
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

    def __init__(self, email, password, confirmed,first_name,last_name,phone,username,
                 paid=False, admin=False, confirmed_on=None):
        self.email = email
        
        self.password = generate_password_hash(password=password,method=os.environ.get('SECURITY_PASSWORD_SALT'),
                                               salt_length=int(os.environ.get('SALT_ROUNDS')))
        self.registered_on = datetime.datetime.now()
        self.admin = admin
        self.confirmed = confirmed
        self.confirmed_on = confirmed_on
        self.first_name=first_name
        self.last_name=last_name
        self.phone=phone
        self.username=username
        self.paid=paid

    def __str__(self):
        return self.username


def migrate():
    with app.app_context():
        db.create_all()

migrate()