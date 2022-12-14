from api import *
import db
import sqlite3
import random
import pprint

DB_FILE = "database.db"


#Each mini quiz q gives 100 grass for a wrong answer, and -250 grass for a right one
#questions will be matching a name to a image

#makes a new question
#returns the image, then the answer choices, along with the correct answer choice
def new_quiz():
    #random choice between pokemon or anime
    #if random.randint(0, 1) > 0:
        #pokemon q
        right = random_poke()
        ans = []
        #prevent the right ansewr being picked again
        ans.append(right['name'])
        for i in range(3):
            wrong = random_poke()
            while wrong['name'] in ans or wrong['name'] in right:
                wrong = random_poke()
            ans.append(wrong['name'])

        random.shuffle(ans)
        ret = {}
        ret['img'] = right['sprite']
        ret['right'] = right['name']
        ret['ans'] = ans
        return ret


pprint.pprint(new_quiz())


#Anime quiz already calls all choices from api, so no need for a method


#changes your grass based on league level
#Doesnt work bc find_summoner_info changed
'''
def league_grass(id):
    username = ""
    if db.ID_exist(id):
        c = db.db_connect()
        c.execute('SELECT Game_Username FROM game WHERE id = ?;', (id,))
        username = str(c.fetchall()[0])[2: -3]
        grass_loss = find_summoner_level(username) * 10
        current_grass = db.get_grass(id)
        current_grass -= grass_loss
        db.update_grass(id, current_grass)
        #these db.py functions calls are the sussiest things ever god help me
    db.db_close()
'''
