import requests
from confid import key

def fetch_plant_data():
    """Make get request to perenual api"""
    payload={'key':key, 'page':1}
    response = requests.get(f"https://perenual.com/api/species-list", params=payload)
    return response.json().get('data',[])
