import requests
from random import sample
from confid import key

def fetch_random_plant_data():
    """Make get request to perenual api and fetch 8 random plants"""
    payload={'key':key}
    response = requests.get(f"https://perenual.com/api/species-list", params=payload)
    all_plants=response.json().get('data',[])
    random_plants=sample(all_plants, 8)
    return random_plants


