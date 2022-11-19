from datetime import datetime
from skill_job import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id): 
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    contact_no = db.Column(db.String(20), unique=True, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.contact_no}', '{self.gender}', '{self.role}')"

class Employer(db.Model):
    __tablename__ = 'employer'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    employer_name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Employer('{self.id}', '{self.user_id}', '{self.employer_name}')"

class Seeker(db.Model, UserMixin):
    __tablename__ = 'seeker'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    intrested_companies = db.Column(db.String(200)) # Employer 
    skills = db.Column(db.String(200))
    location = db.Column(db.String(200))

    def __repr__(self):
        return f"Seeker('{self.id}', '{self.user_id}', '{self.intrested_companies}', '{self.skills}', '{self.location}')"

class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # Employer's User_id's only
    job_title = db.Column(db.String(20), nullable=False)
    skills_needed = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    seekers = db.Column(db.String(200)) # Seekers user_id's only

    def __repr__(self):
        return f"Posts('{self.id}', '{self.user_id}', '{self.job_title}', '{self.skills_needed}', '{self.location}')"

class Skills(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Skills('{self.id}', '{self.skill_name}')"

