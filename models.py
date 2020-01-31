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
    posts = db.relationship('Post', cascade="all, delete")


class Post(db.Model):
    """User post."""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    user = db.relationship('User') 

    tags = db.relationship('Tag',
                            secondary="posts_tags",
                            backref="posts",
                            cascade="all, delete")

    posts_tags = db.relationship('PostTag', cascade="all, delete")


class Tag(db.Model):
    """ Tags. """

    __tablename__ = "tags"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    name = db.Column(db.String(12), nullable=False)

    posts_tags = db.relationship('PostTag', cascade="all, delete")


class PostTag(db.Model):
    """ Post Tags. """

    __tablename__ = "posts_tags" 

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))
    __table_args__ = (
        db.UniqueConstraint('post_id', 'tag_id', name='unique_post_tag'),
    )
