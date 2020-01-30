"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.String(15),
                            nullable=False)
    last_name = db.Column(db.String(20),
                            nullable=False)
    image_url = db.Column(db.Text,
                            default="https://ih1.redbubble.net/image.456962028.0512/flat,128x128,075,f-pad,128x128,f8f8f8.u1.jpg")
    posts = db.relationship('Post')


class Post(db.Model):
    """User post."""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    user = db.relationship('User') 
    # #backref='posts'