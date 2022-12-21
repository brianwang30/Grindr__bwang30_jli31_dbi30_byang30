import requests
import json
import pprint
import random
import os

pp = pprint.PrettyPrinter(indent=4)

#PokeApi Dict Lists name/sprite link/type(s)
def random_poke():
    info = {}
    rand_index = random.randrange(900) #around the max amount of pokemon
    request_data = requests.get(f"https://pokeapi.co/api/v2/pokemon/{rand_index}")
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
    return info

def random_anime():
    info = {}
    dir = os.getcwd()
    print(dir)
    if dir[len(dir)-3:] != 'app':
        os.chdir("app/")

    random_anime_ranks = []
    for i in range(4):
        random_anime_ranks.append(random.randrange(500))

    url = "https://api.myanimelist.net/v2/anime/ranking?ranking_type=all&limit=500" # Taking the top ranking anime and selecting a random one (500 is max)
    data = ""
    client_id = "" #Pulling api key
    try: #check for if text file for key exist
        with open("keys/key_MAL.txt", "r") as file:
            api_key = file.read().strip()
            client_id = api_key
            data = json.loads(requests.get(url, headers={"X-MAL-CLIENT-ID": client_id}).text)

            #Thowing this into try statement bc i dont know a better way data can be empty if the api key is wrong but there wasntg any check so It would crash the program
            choice_number = 0
            for i in random_anime_ranks:
                anime_data = data["data"][i]
                info[f"anime{choice_number}"] = []
                #Name
                info[f'anime{choice_number}'].append(anime_data["node"]["title"])
                #Picture
                info[f'anime{choice_number}'].append(anime_data["node"]["main_picture"]["large"])
                choice_number += 1
    except:
        print("No API key provided.")
    return info

def find_summoner_info(user):
    info = {}
    dir = os.getcwd()
    if dir[len(dir)-3:] != 'app':
        os.chdir("app/")

    try: #check for if text file for key exist
        with open("keys/key_Riot.txt", "r") as file:
            api_key = file.read().strip()
            token = api_key
            url = f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{user}"
            data = json.loads(requests.get(url, headers = {"X-Riot-Token" : token}).text)
            url = f'https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{data["id"]}'
            mastery_data = json.loads(requests.get(url, headers = {"X-Riot-Token" : token}).text)

            info["Name"] = user
            info["Level"] = data["summonerLevel"]
            info["id"] = data["id"]
            info["champion"] = mastery_data[0]["championId"]
            info['points'] = mastery_data[0]["championPoints"]
    except:
        print("No API key provided.")
    return info

def apexL_info(platform, username): #Platforms: 1 = XBOX 2 = PSN 5 = Origin / PC
    dir = os.getcwd()
    if dir[len(dir)-3:] != 'app':
        os.chdir("app/")

    level = 0
    try:
        with open("keys/key_Apex.txt", "r") as file:
            token = file.read().strip()
            url = f'https://public-api.tracker.gg/apex/v1/standard/profile/{platform}/{username}'
            data = json.loads(requests.get(url, headers = {'TRN-Api-Key': token }).text) #set up retrieving token level is at metadata level
            print("hi")
            level = data['data']['metadata']['level']
    except:
        print('error in retrieving info')
    return level
