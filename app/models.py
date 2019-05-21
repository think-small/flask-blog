from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

#  Users table
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    bio = db.Column(db.Text, default="I'm so cool")
    bday = db.Column(db.DateTime, nullable=True)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    visited = db.Column(db.Integer, default="0")
    last_visit = db.Column(db.DateTime)
    posts = db.relationship('Posts', backref='author', lazy=True)

    def __repr__(self):
        return f"Users('{self.username}', '{self.email}', '{self.image_file}')"

#  Posts table
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    content = db.Column(db.Text, nullable=False)   
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __repr__(self):
        return f"Posts('{self.title}', '{self.date_posted}')"
