
import os
from flask import session
from unittest import TestCase
from confid import key
from models import db, User, Plant, Favorite

os.environ['DATABASE_URL']="postgresql:///plant-db-test"

from app import app, CURR_USER_KEY
app.config["TESTING"]=True

db.create_all()
app.app_context().push()
app.config['WTF_CSRF_ENABLED'] = False

class FavoriteViewsTestCase(TestCase):
    """Test views for favoriting plants"""
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

   
    def test_add_favorite(self):
        """Can an user add a plant to their favorites?"""
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
        """A user should not have access to add a favorite if they are not signed in"""
        with self.client as client:
            with client.session_transaction() as session:
             session[CURR_USER_KEY]=None
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

    def test_view_favorites(self):
        """Can an auth user view a list of their favorite plants"""
        user=User.query.get(1000)
        with self.client as client:
            with client.session_transaction() as session:
                session[CURR_USER_KEY]=user.id
            response=client.get(f"/users/{user.id}/favorites")
            self.assertEqual(200, response.status_code)
            self.assertIn('Parents claim no favorites', response.text)

    def test_no_favorites_msg(self):
        """If a user clicks view faves link but no plants are favorited, a msg should flash"""
        user=User.query.get(1000)

        with self.client as client:
            with client.session_transaction() as session:
                session[CURR_USER_KEY]=user.id
            client.post('/delete_favorite/1')
            self.assertEqual(0, len(user.favorites))
            response=client.get(f'/users/{user.id}/favorites')
            html=response.text
            self.assertIn("You do not have any plants favorited at this time.", html)

    def test_view_favorites_nonauth_user(self):
        """A user should not have access to view favorites list if they are not signed in"""
        with self.client as client:
            with client.session_transaction() as session:
                session[CURR_USER_KEY]=None
            response=client.get(f"/users/1000/favorites", follow_redirects=True)
            html=response.text
            self.assertIn("You must login to view", html)
            self.assertEqual(response.request.url, "http://localhost/login")     


  