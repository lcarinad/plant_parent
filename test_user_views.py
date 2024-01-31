
import os
from unittest import TestCase
import requests
from models import db, User, Plant

os.environ['DATABASE_URL']="postgresql:///plant-db-test"

from app import app, CURR_USER_KEY
app.config["TESTING"]=True

db.create_all()
app.app_context().push()
app.config['WTF_CSRF_ENABLED'] = False

class UserViewsTestCase(TestCase):
    """Test user views."""
    def setUp(self):
        """Add sample user"""
        db.drop_all()
        db.create_all()
        db.session.commit()

        self.client = app.test_client()

        self.testUser = User.signup(username="testUser", email="messagetest@test.com", password="Hashed_Password" )
        self.testUser.id=1000

        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction"""
        response=super().tearDown()
        db.session.rollback()
        return response
    #######################################################################
    #Testing signup

    def test_user_signup_display(self):
        """Does signup form show up?"""
        resp = self.client.get('/signup')
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('We are going to need some info!', html)

    def test_user_signup_valid(self):
        """Can user signup with valid credentials?"""
        with self.client as client:
            d={"username":"user1", "email":"user1@test.com", "password":"hashy_pashy", } 

            response = client.post('/signup', data=d, follow_redirects=True)   
            html = response.text

            self.assertEqual(response.status_code, 200)
            self.assertIn("Welcome user1", html)
            self.assertIn("our picks", html)
            #verifying user can be queried in db
            user = User.query.filter_by(username="user1").one()
            self.assertEqual("user1", user.username)