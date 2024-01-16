import requests, json
from random import sample, randint
from confid import key


def fetch_random_plant_data():
    """Make get request to perenual api"""
    random_page=get_random_page()
    payload={'key':key, 'page':random_page}
    response = requests.get(f"https://perenual.com/api/species-list", params=payload)
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

def fetch_search_terms(term):
    """Make get request to return search terms"""
    payload={'key':key,'q':term }
    response = requests.get(f"https://perenual.com/api/species-list", params=payload)
    results=response.json().get('data',[])
    return results

def fetch_plant_details(plant_id):
    """Make get request to return plant details"""
    print(f"************************************plant id:{plant_id}")
    payload={'key':key}
    response = requests.get(f"https://perenual.com/api/species/details/{plant_id}", params=payload)

    if response.status_code==200:
        plant_data=json.loads(response.text)
        return plant_data
    else:
        return None