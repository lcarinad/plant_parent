import os
from unittest import TestCase

from models import User, Plant, Favorite

os.environ['DATABASE_URL']="postgresql:///plant-db-test"
from app import app, db, CURR_USER_KEY

app.config["TESTING"]=True

db.create_all()
app.app_context().push()
app.config['WTF_CSRF_ENABLED'] = True

class TestModels(TestCase):
    def setUp(self):
        """Run before every test."""
        db.drop_all()
        db.create_all()

        self.user = User.signup(username="testUser", email="test@test.com", password="hashedpassword")
        db.session.commit()

        self.plant = Plant.add_plant(api_id=1, name="Test Plant", image_url="https://example.com/image.jpg",
                                     watering_freq="frequent", watering_value="5-7", watering_unit="days", sunlight="full_sun")
        db.session.commit()

    def tearDown(self):
        """Run after every test."""
        db.session.rollback()

    def test_user_model(self):
        """Does basic user model work?"""
        user = User.query.get(self.user.id)
        self.assertEqual(user.username, "testUser")
        self.assertEqual(user.email, "test@test.com")

    def test_plant_model(self):
        """Does basic plant model work?"""
        plant = Plant.query.get(self.plant.id)
        self.assertEqual(plant.id, 1)
        self.assertEqual(plant.api_id, 1)
        self.assertEqual(plant.name, "Test Plant")
        self.assertEqual(plant.image_url, "https://example.com/image.jpg")

    def test_favorite_model(self):
        """Does basic favorite model work?"""
        favorite = Favorite.add_fave(user_id=self.user.id, plant_id=self.plant.id, plant_api_id=1)
        db.session.commit()

        fav_user = User.query.get(self.user.id)
        self.assertIn(self.plant, fav_user.favorites)

    def test_user_model_after_editing(self):
        """Does user model update when an auth user submits edit form?"""
        user=User.query.get(self.user.id)
        with app.test_client() as client:
            with client.session_transaction() as session:
                session[CURR_USER_KEY]=user.id
            form_data={'username':'testUser','password':'hashedpassword', 'pref_sunlight':'sun-part_shade'}
            resp=client.post(f"/users/profile/{user.id}/edit", data=form_data, follow_redirects=True)
            self.assertEqual(200, resp.status_code)

            self.assertIn("You updated your profile", resp.text)
            updated_user=User.query.get(user.id)
            self.assertEqual(updated_user.pref_sunlight, 'sun-part_shade')



