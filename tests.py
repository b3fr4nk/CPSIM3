import os
from unittest import TestCase

from datetime import date
 
from cpsim_app.extensions import app, db, bcrypt
from cpsim_app.models import User, SimDoc

"""
Run these tests with the command:
python -m unittest books_app.main.tests
"""

#################################################
# Setup
#################################################

def create_sim():
    sim = SimDoc(doc=f'{os.path.join(app.config["SIM_FOLDER"])}1.pkl', cost=10000, time=107)
    db.session.add(sim)
    db.session.commit()

def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(school_email='bob.crump@university.com', password=password_hash, class_code='abc', name='bob crump', is_teacher=False)
    db.session.add(user)
    db.session.commit()

#################################################
# Tests
#################################################

class Tests(TestCase):
    """Tests for authentication (login & signup)."""
 
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_signup(self):
        post_data = {
            'school_email':'bob.crump@university.com',
            'password':'password',
            'class_code':"abc"
        }
        self.app.post('/signup', data=post_data)
        user = User.query.all()
        self.assertIn(post_data['school_email'], f'{user}')

    def test_signup_existing_user(self):
        create_user()
        post_data = {
            'school_email':'bob.crump@university.com',
            'password':'password',
            'class_code':'abc'
        }
        response = self.app.post('/signup', data=post_data)
        self.assertIn(f'That school_email is taken. Please choose a different one.', response.get_data(as_text=True))

    def test_login_correct_password(self):
        create_user()
        post_data = {
            'school_email':'bob.crump@university.com',
            'password':'password'
        }
        response = self.app.post('/login', data=post_data)
        self.assertNotIn('Login', response.get_data(as_text=True))

    def test_login_nonexistent_user(self):
        post_data = {
            'school_email':'me3',
            'password':'passwords'
        }

        response = self.app.post('/login', data=post_data)
        self.assertIn("No user with that school_email. Please try again.", response.get_data(as_text=True))

    def test_login_incorrect_password(self):
        create_user()
        post_data = {
            'school_email':'bob.crump@university.com',
            'password':'incorrect'
        }
        response = self.app.post('/login', data=post_data)
        self.assertIn('Password doesn&#39;t match. Please try again', response.get_data(as_text=True))

    def test_logout(self):
        create_user()

        post_data = {
            'school_email':'bob.crump@university.com',
            'password':'password'
        }

        self.app.post('/login', data=post_data)
        response = self.app.get('/logout', follow_redirects=True)

        self.assertIn('Log In', response.get_data(as_text=True))

    def test_user_sim(self):
        create_user()
        create_sim()

        user = User.query.filter_by(school_email='bob.crump@university.com').first()

        result = SimDoc.query.filter_by(user_id=user.id).first()

        self.assertIsNotNone(result)
        