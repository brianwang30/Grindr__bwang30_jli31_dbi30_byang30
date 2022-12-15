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
c.execute("CREATE TABLE if not Exists grassmeter(ID INTEGER PRIMARY KEY AUTOINCREMENT, Quiz_Grass INTEGER, Grass INTEGER);")
# Game accounts
c.execute("CREATE TABLE if not Exists game(ID INTEGER PRIMARY KEY AUTOINCREMENT, Game TEXT, Game_Username TEXT);")
its = ["You have never touched grass...", "you're terrible", "mmm not bad", "getting there", "as green as nature!"]
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
    c.execute('INSERT INTO grassmeter(Quiz_Grass, Grass) VALUES (?, ?);', (0, 0))
    c.execute('INSERT INTO game(Game, Game_Username) VALUES (?,?);', ("LOL", ""))
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

def get_insult(grass_level):
    c = db_connect()
    c.execute('SELECT ' + str(grass_level) + ' FROM insult;')
    text = c.fetchone()
    db_close()
    #l = text.split(';') 
    return text#l[random.randint(0, len(l) - 1)]

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
        c.execute('SELECT * FROM grassmeter WHERE ID=?;', (id,))
        text = c.fetchone()
        db_close()
        return text[2]
    return "User doesn't exists"

def get_quiz_grass(id):
    c = db_connect()
    if ID_exist(id):
        c.execute('SELECT * FROM grassmeter WHERE ID=?;', (id,))
        text = c.fetchone()
        db_close()
        return text[1]
    return "User doesn't exists"

def get_gameuser(id):
    c = db_connect()
    if ID_exist(id):
        c.execute('SELECT Game_Username FROM game WHERE ID =?', (id,))
        text = c.fetchone()
        db_close()
        return text[0]
    return "User doesn't exist"


def update_account_grass(id, grass):
    c = db_connect()
    c.execute('UPDATE grassmeter SET Grass =? WHERE ID=?;', (grass, id))
    db_close()
    return None

def update_quiz_grass(id, grass):
    old = get_quiz_grass(id)
    c = db_connect()
    c.execute('UPDATE grassmeter SET Quiz_Grass =? WHERE ID=?;', (old + grass,))
    db_close()
    return None

def update_grass(id, grass):
    update_quiz_grass(id, grass)
    old = get_grass(id)
    c = db_connect()
    c.execute('UPDATE grassmeter SET Grass =? WHERE ID=?;', (old + grass, id))
    db_close()
    return None 

def update_gameusername(id, game_username):
    c = db_connect()
    c.execute('UPDATE game SET Game_Username =? WHERE ID=?', (game_username,id))
    db_close()
    return None

