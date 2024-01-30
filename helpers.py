import requests, json
from random import sample, randint
from confid import key
from models import Plant


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

def fetch_search_terms(q=None, indoor=None, edible=None, watering=None, sunlight=None,order=None, page=None):
    """Make get request to return search terms"""
    if edible == True:
        edible=1
    if indoor == True:
        indoor=1
    payload={'key':key,'q':q,'indoor':indoor,'edible':edible,'watering':watering, 'sunlight':sunlight,'order':order, 'page':page }

    response = requests.get(f"https://perenual.com/api/species-list", params=payload)
    unusable_results=response.json().get('data',[])
    results=[]

    for result in unusable_results:
        if 'id' in result and result['id'] <=3000:
            results.append(result)
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
    random_idx=randint(1, len(messages)-1)

    return messages[random_idx]

def add_plant(plant_data):
    """Add plant to db"""
    
    api_id=plant_data.get('id')
    name=plant_data.get('common_name')
    watering_freq=plant_data.get('watering')
    watering_benchmark=plant_data.get("watering_general_benchmark")
    if watering_benchmark:
        watering_value = watering_benchmark.get("value", "N/A")
        watering_unit = watering_benchmark.get("unit", "N/A")
    sunlight=plant_data.get("sunlight")
    image_na_url="https://upload.wikimedia.org/wikipedia/commons/d/d1/Image_not_available.png?20210219185637"

    default_image=plant_data.get('default_image')
    image_url = image_na_url

    if default_image and 'thumbnail' in default_image:
        image_url = default_image['thumbnail']

    plant=Plant.add_plant(api_id=api_id, name=name, image_url=image_url, watering_freq=watering_freq, watering_value=watering_value, watering_unit=watering_unit, sunlight=sunlight)
    return plant