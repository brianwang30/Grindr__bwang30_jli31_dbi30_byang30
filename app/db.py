import sqlite3
import random

DB_FILE = "database.db"

db = None
db = sqlite3.connect(DB_FILE)
c = db.cursor()
# Login information
c.execute("CREATE TABLE if not Exists users(ID INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, Did_Questions BOOLEAN);")
# Insult database
c.execute("CREATE TABLE if not Exists insult(lv5 TEXT, lv4 TEXT, lv3 TEXT, lv2 TEXT, lv1 TEXT);")
# Grassmeter
c.execute("CREATE TABLE if not Exists grassmeter(ID INTEGER PRIMARY KEY AUTOINCREMENT, Quiz_Grass INTEGER, Grass INTEGER, Game_Grass INTEGER);")
# Game accounts
c.execute("CREATE TABLE if not Exists game(ID INTEGER, Game TEXT, Game_Username TEXT);")
its = ["You probably live in your parents' basement@@", "Looks like all the grass you have touched were digital!@@", "This could go either way, what are you really?@@", "Are you too poor to afford a computer? Or are you lying on the quizes?@@", "You green as nature!@@"]
c.execute('INSERT or IGNORE INTO insult(lv5, lv4, lv3, lv2, lv1) VALUES (?, ?, ?, ?, ?);', (its[0], its[1], its[2], its[3],its[4]))
db.commit()
c.close()

def db_connect():
    global db
    db = sqlite3.connect(DB_FILE)
    return db.cursor()

def db_close():
    db.commit()
    db.close()

def create_user(username, password):
    c = db_connect()
    c.execute('INSERT INTO users(username, password, Did_Questions) VALUES (?, ?, ?);', (username, password, False))
    c.execute('INSERT INTO grassmeter(Quiz_Grass, Grass, Game_Grass) VALUES (?, ?, ?);', (0, 0, 0))
    db.commit()
    #db_close() Dont know what exactly the problem is but dont uncomment this for signup to work

def user_exist(username):
    c = db_connect()
    c.execute('SELECT username FROM users WHERE username = ?;', (username,))
    check = c.fetchone()
    #db_close() Dont know what exactly the problem is but dont uncomment this for signup to work
    if check is None:
        return False
    else:
        return True

def verify(username, password):
    c = db_connect()
    c.execute('SELECT username,password FROM users WHERE username=? AND password=?',(username, password))
    check = c.fetchone()
    db_close()
    if check:
        return True
    else:
        return False

def user_did_questions(username):
    c = db_connect()
    c.execute('SELECT Did_Questions FROM users WHERE username=?', (username,))
    did_questions = c.fetchone()
    
    print(username)
    print(did_questions[0])

    db_close()
    return did_questions[0]
    
def submit_questions(username):
    c = db_connect()
    c.execute('UPDATE users SET Did_Questions=? WHERE username=?', (True, username,))
    db_close()
    return None

def get_insult(grass_level):
    c = db_connect()
    c.execute('SELECT ' + str(grass_level) + ' FROM insult;')
    text = c.fetchone()[0]
    db_close()
    l = text.split('@@')
    return l[random.randint(0, len(l) - 1)]

def ID_exist(id):
    c = db_connect()
    c.execute('SELECT ID FROM users WHERE ID =?;', (id,))
    text = c.fetchone()
    #db_close() Dont know what exactly the problem is but dont uncomment this for signup to work
    if id is None:
        return False
    return True

def get_userID(username):
    c = db_connect()
    if not user_exist(username):
        return None
    c.execute('SELECT ID FROM users WHERE username =?;', (username,))
    text = c.fetchone()
    db_close()
    return text[0]

def get_grass(id):
    c = db_connect()
    if ID_exist(id):
        quiz = get_quiz_grass(id)
        game = get_game_grass(id)
        return quiz + game
    return "User doesn't exist (1)"

def get_game_grass(id):
    c = db_connect()
    if ID_exist(id):
        c.execute('SELECT Game_Grass FROM grassmeter WHERE ID = ?', (id,))
        text = c.fetchone()[0]
        return text
    return "User doesn't exist (2)"

def get_quiz_grass(id):
    c = db_connect()
    if ID_exist(id):
        c.execute('SELECT * FROM grassmeter WHERE ID=?;', (id,))
        text = c.fetchone()
        db_close()
        return text[1]
    return "User doesn't exist (3)"

def get_gameuser(id, game):
    c = db_connect()
    if 'apex' in game:
        c.execute('SELECT Game_Username FROM game WHERE ID=? AND instr(Game, ?) > 0;', (id, 'apex'))
    else:
        c.execute('SELECT Game_Username FROM game WHERE ID=? AND Game=?;', (id, game))
    text = c.fetchone()
    db_close()
    if text == None:
        return text
    return text[0]

def get_apex_platform(id, user):
    c = db_connect()
    c.execute('SELECT Game FROM game WHERE ID=? and Game_Username=?;', (id, user))
    return int(c.fetchone()[0][0])

def get_grasslv(id):
    c = db_connect()
    if ID_exist(id):
        grass = get_grass(id)
        if (grass > int("-5000")):
            return "lv5"
        elif (grass > int("-2500")):
            return "lv4"
        elif(grass > 0):
            return "lv3"
        elif(grass > 2500):
            return "lv2"
        else:
            return "lv1"


def update_account_grass(id, grass):
    c = db_connect()
    c.execute('UPDATE grassmeter SET Grass =? WHERE ID=?;', (grass, id))
    db_close()
    return None

def update_quiz_grass(id, grass):
    old = get_quiz_grass(id)
    c = db_connect()
    c.execute('UPDATE grassmeter SET Quiz_Grass =? WHERE ID=?;', (old + grass, id))
    db_close()
    return None

def update_grass(id, grass):
    update_quiz_grass(id, grass)
    old = get_grass(id)
    c = db_connect()
    c.execute('UPDATE grassmeter SET Grass =? WHERE ID=?;', (old + grass, id))
    db_close()
    return None

def update_game_grass(id, lv):
    c = db_connect()
    c.execute('UPDATE grassmeter SET Game_Grass =? WHERE ID=?;', (lv * 10, id))
    db_close()
    return None

def update_gameusername(id, game, game_username):
    c = db_connect()
    c.execute('SELECT game_username FROM game WHERE ID=? AND Game=?;', (id, game))
    check = c.fetchone()
    if (check != None):
        c.execute('UPDATE game SET Game_Username=? WHERE ID=? AND Game=?;', (game_username, id, game))
    else:
        c.execute('INSERT INTO game(ID, Game, Game_Username) VALUES (?,?,?);', (id, game, game_username))
    db_close()
    return None

def add_insult(text, grass_level):
    old = get_insult(grass_level)
    old = old + "@@" + text
    c = db_connect()
    c.execute('UPDATE insult SET ' + str(grass_level) + ' =?;', (old,))
    db_close()
    return None
