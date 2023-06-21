import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    """Base configuration."""

    # main config
    SECRET_KEY = os.environ['SECRET_KEY']
    SECURITY_PASSWORD_SALT = os.environ['SECURITY_PASSWORD_SALT']
    DEBUG = False
    BCRYPT_LOG_ROUNDS = os.environ['SALT_ROUNDS']
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # mail settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    MAIL_USERNAME = os.environ['SENDING_EMAIL']
    MAIL_PASSWORD = os.environ['SENDING_EMAIL_PASSWORD']

    # mail accounts
    MAIL_DEFAULT_SENDER = os.environ['SENDING_EMAIL']
