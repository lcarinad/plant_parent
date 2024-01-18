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
    """generate random page number. Free api allows query to id 3000, 30 plants/page"""
    random_page=randint(1, 100)
    return random_page

def fetch_search_terms(term=None,indoor_pref=None,edible_pref=None,watering_pref=None,sun_pref=None,order=None, page=None):
    """Make get request to return search terms"""
    payload={'key':key,'q':term,'indoor':indoor_pref,'edible':edible_pref,'watering':watering_pref, 'sunlight':sun_pref,'order':order, 'page':page }

    response = requests.get(f"https://perenual.com/api/species-list", params=payload)
    results=response.json().get('data',[])

    return results

def fetch_plant_details(plant_id):
    """Make get request to return plant details"""
    payload={'key':key}
    response = requests.get(f"https://perenual.com/api/species/details/{plant_id}", params=payload)

    if response.status_code==200:
        plant_data=json.loads(response.text)
        return plant_data
    else:
        return None
    
def get_logout_msg():
    messages =["Blossom back soon, we'll miss your photosynthesis!🌿👋", "Rooting for your return! See you in the plant-osphere! 🌱🚀", "Take a leaf, but don't stay away too long! 🍃👀","Farewell, green thumb! We'll be here, photosynthesizing without you! 🌞🌿", "Branch out and explore, but don't forget your roots! 🌍🌳", "Time to leaf, but remember, you're always in our plant-astic garden! 🌸👋", "May your journeys be as fruitful as a well-nurtured garden! 🌺🚀","Signing off for now! Your absence will be felt in our plantiverse! 🌿😢"]
    random_idx=randint(0, len(messages))

    return messages[random_idx]
