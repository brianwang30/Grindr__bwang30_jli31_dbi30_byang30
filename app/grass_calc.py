from api import *

#Each mini quiz q gives 100 grass for a wrong answer, and -250 grass for a right one
#questions will be matching a name to a image

#makes a new question
#returns the image, then the answer choices, along with the correct answer choice
def new_quiz(userid):
    #random choice between pokemon or anime
    if random.randint(0, 1) > 0:
        #pokemon q
        right = random_poke()
        #prevent the right ansewr being picked again
        wrong1 = random_poke()
        for wrong1['name'] in right:
            wrong1 = random_poke()
        wrong2 = random_poke()
        for wrong2['name'] in right:
            wrong2 = random_poke()
        wrong3 = random_poke()
        for wrong3['name'] in right:
            wrong3 = random_poke()
        
        ret = {}
        ret['img'] = right['sprite']
        ret['right'] = right['name']
        ret['wrong'] = [wrong1['name'], wrong2['name'], wrong3['name']]
        return ret

    else:
        #anime q
        right = random_anime()
        wrong1 = random_anime()
        for wrong1['name'] in right:
            wrong1 = random_anime()
        wrong2 = random_anime()
        for wrong2['name'] in right:
            wrong2 = random_anime()
        wrong3 = random_anime()
        for wrong3['name'] in right:
            wrong3 = random_anime()
        
        ret = {}
        ret['img'] = right['image']
        ret['right'] = right['name']
        ret['wrong'] = [wrong1['name'], wrong2['name'], wrong3['name']]
        return ret
