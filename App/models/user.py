from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String, nullable=False)
    lastName = db.Column(db.String, nullable=False)
    username =  db.Column(db.String, nullable=False, unique=True)
    email =  db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    year = db.Column(db.Integer, nullable= True)
    degree = db.Column(db.Integer, nullable= True)
    department = db.Column(db.String, nullable=True)
    faculty = db.Column(db.String, nullable=True)
    experience = db.Column(db.String, nullable=True)
    profile_pic = db.Column(db.String, nullable=True)
    



    def __init__(self, firstName, lastName, username, email, password):
        self.firstName = firstName
        self.lastName = lastName
        self.username = username
        self.email = email
        self.set_password(password)

    def toDict(self):
        return{
            'id': self.id,
            'username': self.username,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'email': self.email,
            'year': self.year,
            'degree': self.degree,
            'department': self.department,
            'faculty': self.faculty,
            'profile_pic': self.profile_pic,
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

