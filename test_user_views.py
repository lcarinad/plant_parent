
import os
from flask import session
from unittest import TestCase
import requests
from models import db, User, Plant, Favorite

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

        self.testPlant=Plant.add_plant(api_id=1, name="European Silver Fir", image_url="https://perenual.com/storage/species_image/1_abies_alba/og/1536px-Abies_alba_SkalitC3A9.jpg", watering_freq=None, watering_value=None, watering_unit=None, sunlight=None)

        self.testPlant2=Plant.add_plant(api_id=2, name="Pyramidalis Silver Fir", image_url="https://perenual.com/storage/species_image/2_abies_alba_pyramidalis/thumbnail/49255769768_df55596553_b.jpg", watering_freq=None, watering_value=None, watering_unit=None, sunlight=None)

        db.session.commit()
        self.testUserFave=Favorite.add_fave(user_id=1000, plant_id=1, plant_api_id=1)
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

    def test_user_signup_with_existing_username(self):
        """Can user sign up with an existing username?"""
        with self.client as client:
            d={"username":"testUser", "email":"user2@test.com", "password":"hashy_pashy2", } 
            response = client.post("/signup", data=d, follow_redirects=True)
            html = response.text
            self.assertEqual(response.status_code, 200)
            self.assertIn("That username is already taken", html)
            self.assertNotIn("Welcome", html)

    def test_user_signup_with_existing_email(self):
        """Can user sign up with an existing email?"""
        with self.client as client:
            d={"username":"testUser1", "email":"messagetest@test.com", "password":"hashy_pashy2", } 
            response = client.post("/signup", data=d, follow_redirects=True)
            html = response.text
            self.assertEqual(response.status_code, 200)
            self.assertIn("That email address is already registered.", html)
            self.assertNotIn("Welcome", html)

    def test_session_info(self):
        """Is user saved in session?"""
        with self.client as client:
            d={"username":"testUser", "password":"Hashed_Password"} 
            resp = client.post("/login", data=d, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(session['curr_user'],1000 )

    def test_add_favorite(self):
        """Can a user add a plant to their favorites?"""
        user=User.query.get(1000)
        with self.client as client:
            with client.session_transaction() as session:
                session[CURR_USER_KEY]=user.id
            self.assertIsNone(Favorite.query.filter_by(user_id=1000, plant_id=2).first())
            response=client.post("/add_favorite/2", follow_redirects=True)
            self.assertEqual( '201 CREATED', response.status)
            self.assertIsNotNone(Favorite.query.filter_by(user_id=1000, plant_id=2).first())
            self.assertEqual(len(user.favorites), 2)

    def test_add_favorite_nonauth_user(self):
        """Can a user add a plant to their favorites if they are not signed in"""
        with self.client as client:
            with client.session_transaction() as change_session:
                change_session[CURR_USER_KEY]=None
            response=client.post("/add_favorite/2", follow_redirects=True)
            html=response.text
            self.assertIn("You must login to favorite a plant.", html)
            self.assertEqual(response.request.url, "http://localhost/login")           
            
    def test_delete_favorite(self):
        """Can a user delete a plant from their favorites?"""
        user=User.query.get(1000)
        with self.client as client:
            with client.session_transaction() as session:
                session[CURR_USER_KEY]=user.id
            self.assertIsNotNone(Favorite.query.filter_by(user_id=1000, plant_id=1).first())
            response=client.post("/delete_favorite/1", follow_redirects=True)
            self.assertEqual(200, response.status_code)
            self.assertIsNone(Favorite.query.filter_by(user_id=1000, plant_id=1).first())
            self.assertEqual(len(user.favorites), 0)