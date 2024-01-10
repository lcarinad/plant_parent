""" Seed file to make sample data for plant care app."""

from models import User, Plant, Favorite, db
from app import app

# Create all tables


# if tables aren't empty, empty them
User.query.delete()
Plant.query.delete()
Favorite.query.delete()

# Add user instances
user1 = User(username='user1', email='user1@example.com', password='password1')
user2 = User(username='user2', email='user2@example.com', password='password2')

# Add plant instances
plant1 = Plant(api_id=1, name='European Silver Fir', image_url='https://perenual.com/storage/species_image/2_abies_alba_pyramidalis/regular/49255769768_df55596553_b.jpg')
plant2 = Plant(api_id=2, name='Pyramidalis Silver Fir', image_url='https://perenual.com/storage/species_image/2_abies_alba_pyramidalis/regular/49255769768_df55596553_b.jpg')

# Add new objects to session, so they'll persist
db.session.add(user1)
db.session.add(user2)
db.session.add(plant1)
db.session.add(plant2)

# Commit the changes to the database
db.session.commit()

# Add favorite associations
favorite1 = Favorite(user_id=user1.id, plant_id=plant1.id)
favorite2 = Favorite(user_id=user2.id, plant_id=plant2.id)

# Add new favorite objects to session
db.session.add(favorite1)
db.session.add(favorite2)

# Commit the changes to the database
db.session.commit()
