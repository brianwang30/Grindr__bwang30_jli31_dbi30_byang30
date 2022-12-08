import requests
import random

#PokeApi Dict Lists name/sprite link/type(s )
def random_poke():
    info = {}
    rand_index = random.randrange(900)
    request_data = requests.get(f"https://pokeapi.co/api/v2/pokemon/400")
    data = request_data.json()

    #Name
    info["name"] = data["name"]
    #Sprite Link to a PNG
    info["sprite"] = data["sprites"]["other"]["official-artwork"]["front_default"]
    #type(s)
    type1 = data["types"][0]["type"]["name"]
    type2 = ""
    try:
        type2 = data["types"][1]["type"]["name"]
    except:
        None
    info["type"] = [type1, type2]
