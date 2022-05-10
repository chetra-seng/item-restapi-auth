import os

DEBUG = True
SQLALCHEMY_DATABASE_URI = "sqlite:///data.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
SECRET_KEY = os.environ['SECRET_KEY']
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
GITHUB = {
    'consumer_key': os.environ['GITHUB_CLIENT_ID'],
    'consumer_secret': os.environ['GITHUB_SECRET_KEY']
}
