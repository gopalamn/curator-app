from . import db
import datetime
import json
import enum

class JSONEncodedDict(db.TypeDecorator):
    """Represents an immutable structure as a
    json encoded string
    Usage:: JSONEncodedDict(255)"""

    impl = db.VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), nullable=False, unique=True)
    username = db.Column(db.String(32))
    password_hash = db.Column(db.String(128), nullable=False)
    firstname = db.Column(db.String(32))
    lastname = db.Column(db.String(32))
    profile_pic = db.Column(db.Text)
    profile_pic_key = db.Column(db.Text)

class Individual_Book_Posts(db.Model):
    __tablename__ = 'individual_book_posts'

    book_post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_api_id = db.Column(db.String(32), nullable=False)
    user_id = db.Column(db.ForeignKey('users.user_id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    title = db.Column(db.String(128), nullable=False)
    cover_img = db.Column(db.Text)
    link = db.Column(db.Text)
    created_time = db.Column(db.DateTime, nullable=False)

class Link_Posts(db.Model):
    __tablename__ = 'link_posts'

    link_post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.ForeignKey('users.user_id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    link = db.Column(db.Text)
    img = db.Column(db.Text)
    description = db.Column(db.Text)
    title = db.Column(db.Text)
    created_time = db.Column(db.DateTime, nullable=False)
    hostname = db.Column(db.Text)