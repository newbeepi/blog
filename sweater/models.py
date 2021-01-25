from datetime import datetime
from . import db, manager
from flask_login import UserMixin


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True)
    mail = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    posts = db.relationship('Post', backref=db.backref('author', lazy=True))

    def get_id(self):
        return str(self.user_id)

    def __init__(self, username, email, password):
        self.username = username
        self.mail = email
        self.password = password

    def __repr__(self):
        return self.username


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_name = db.Column(db.String, unique=True)
    post_text = db.Column(db.Text)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

    def __init__(self, post_name, post_text, user_id=2):
        self.post_text = post_text
        self.post_name = post_name
        self.user_id = user_id

    def __repr__(self):
        return self.post_name


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    author = db.relationship('User', backref=db.backref('comments', lazy=True))
    post = db.relationship('Post', backref=db.backref('comments', lazy=True))

    def __init__(self, text, user_id, post_id):
        self.text = text
        self.user_id = user_id
        self.post_id = post_id


@manager.user_loader
def load_user(user_id):
    return User.query.filter_by(user_id=user_id).first()