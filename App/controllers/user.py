from App.models import User
from App.database import db
from .auth import login_user
from flask import current_app
from werkzeug.utils import secure_filename
import uuid as uuid
import os



def get_all_users():
    return User.query.all()

def create_user(firstName, lastName, username, email, password):
    newuser = User(firstName=firstName, lastName=lastName, username=username, email=email, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.toDict() for user in users]
    return users

def get_all_users():
    return User.query.all()

def get_user(username, email):
    users = User.query.filter_by(username=username).first()
    if not users:
        users = User.query.filter_by(email=email).first()
    if not users:
        return 
    return users


def is_user(username, email):
    users = User.query.filter_by(username=username).first()
    if users:
        return "Username"
    users = User.query.filter_by(email=email).first()
    if users:
        return "Email"
    return False

def add_profile_data(id, year, degree, department, faculty, job, profile_pic):
    users = User.query.filter_by(id=id).first()
    if year:
        users.year = year
    if degree:
        users.degree = degree
    if department:
        users.department = department
    if faculty:
        users.faculty = faculty
    if job:
        users.experience = job
    if profile_pic:
        pic_name = secure_filename(profile_pic.filename)
        pic_name = str(uuid.uuid1()) + '_' + pic_name
        users.profile_pic = pic_name
        profile_pic.save(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], pic_name))
    db.session.add(users)
    db.session.commit()
