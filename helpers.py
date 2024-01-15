import requests
from random import sample, randint
from confid import key

def fetch_random_plant_data():
    """Make get request to perenual api"""
    random_page=get_random_page()
    payload={'key':key, 'page':random_page}
    response = requests.get(f"https://perenual.com/api/species-list", params=payload)
    print(f"***************url:{response.url}")
    all_plants=response.json().get('data',[])
    random_plants=get_random_plants(all_plants)
    return random_plants


def get_random_plants(all_plants):
    """Fetch 8 random plants"""
    list_size=min(len(all_plants),8)
    random_plants=sample(all_plants, k=list_size)
    return random_plants

def get_random_page():
    """generate random page number"""
    random_page=randint(1, 30)
    return random_page