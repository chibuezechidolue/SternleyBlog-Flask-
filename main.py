from itsdangerous import URLSafeTimedSerializer
from flask import Flask,redirect,flash,url_for
from dotenv import load_dotenv
import os
from functools import wraps
from flask_login import current_user, login_required
from flask_mail import Message,Mail





load_dotenv()


app=Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///SternleyBlog.db"
# add additional flask config setting from in the config.py
app.config.from_object("config.Config")
mail=Mail(app)




# generate and confirm token function for Email confirmation
def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email



# login_required decoreator function    
def logout_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            flash("You are already authenticated.", "info")
            return redirect(url_for("index_page"))
        return func(*args, **kwargs)

    return decorated_function

# function to send emails
def send_email(to, subject,**kwargs):
    msg = Message(
        subject,
        recipients=[to],
        html=kwargs.get('template'),
        sender=app.config["MAIL_DEFAULT_SENDER"],
        body=kwargs.get('body')
    )
    mail.send(msg)