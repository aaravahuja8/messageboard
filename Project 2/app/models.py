from flask_login import UserMixin
from . import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = "users"
    username = db.Column(db.String(256), primary_key=True, index=True)
    password = db.Column(db.String(256))
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    email = db.Column(db.String(64))
    joindate = db.Column(db.DateTime)
    postcount = db.Column(db.Integer)
    posts = db.relationship("Post", backref="user")

    def get_id(self):
        return (self.username)

    def __repr__(self):
        return f'<User "{self.username}">'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    title = db.Column(db.String(256))
    content = db.Column(db.Text)
    time = db.Column(db.DateTime)
    username = db.Column(db.String(256), db.ForeignKey('users.username'))
    commentcount = db.Column(db.Integer)
    comments =  db.relationship("Comment", backref="post")
    def __repr__(self):
        return f'<Event "{self.id}">'

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    content = db.Column(db.Text)
    time = db.Column(db.DateTime)
    postid = db.Column(db.Integer, db.ForeignKey('posts.id'))
    username = db.Column(db.String(256), db.ForeignKey('users.username'))