from cpsim_app.extensions import db
from flask_login import UserMixin

class SimDoc(db.Model):
    __tablename__ = 'sim'
    id = db.Column(db.Integer, primary_key=True)
    doc = db.Column(db.Text)
    cost = db.Column(db.Integer)
    time = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User')


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    school_email = db.Column(db.String, nullable=False)
    class_code = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=True)
    password = db.Column(db.String, nullable=False)
    is_teacher = db.Column(db.Boolean, default=False)