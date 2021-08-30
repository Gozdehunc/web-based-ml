import hashlib
import os
from appconfig import db
from flask_login import UserMixin



class User(db.Model,UserMixin):
    id =db.Column(db.Integer,primary_key=True)

    username = db.Column(db.String(80),unique=True,nullable=False)
    password = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String,unique=True,nullable=False)

    def __init__(self,username,password,email):
        self.username=username
        self.password = password
        self.email = email


    def __repr__(self):
        return f"{self.username}{self.email}"


def create_db(file_name):
    if not os.path.isfile(file_name):
        db.create_all()


def salt_password(password):

    salt ="fldfşldfşldfşdlşl"
    salted = salt+password
    password_hashed =hashlib.sha256(salted.encode("utf-8")).hexdigest()
    return password_hashed 


def register_user(username,email,password):

    password_hashed = salt_password(password)
    user1 = User(username=username,email=email,password=password_hashed)
    db.session.add(user1)
    db.session.commit()



def get_user(username,password):

    password_hashed = salt_password(password)
    user1 = User.query.filter_by(username=username).filter_by(password=password_hashed).first()
    return user1
