from cpsim_app.extensions import db
from flask_login import UserMixin

class SimDoc(db.Model, UserMixin):
    __tablename__ = 'sim'
    id = db.Column(db.Integer, primary_key=True)
    doc = db.Column(db.Text)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    school_email = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=True)
    password = db.Column(db.String, nullable=False)

    # isTeacher = db.Column(db.Boolean)
    

user_sim_table = db.Table('user_sim',
    db.Column('sim_id', db.ForeignKey('sim.id')),
    db.Column('user_id', db.ForeignKey('user.id'))
)