import sqlite3

DB_FILE = "database.db"

db = None
db = sqlite3.connect(DB_FILE)
c = db.cursor()
# Login information
c.execute("CREATE TABLE if not Exists users(ID INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, Did_Questions BOOLEAN);")
# Insult database
c.execute("CREATE TABLE if not Exists insult(Insult_ID INTEGER PRIMARY KEY AUTOINCREMENT, Insult_Text TEXT, Grass_Level INTEGER, API_INFO TEXT);")
# Grass meter
c.execute("CREATE TABLE if not Exists grassmeter(ID INTEGER PRIMARY KEY AUTOINCREMENT, Quiz_Grass INTEGER, Grass INTEGER);")
# Game accounts
c.execute("CREATE TABLE if not Exists game(ID INTEGER PRIMARY KEY AUTOINCREMENT, Game TEXT, Game_Username);")
db.commit()
db.close()

def db_connect():
    global db
    db = sqlite3.connect(DB_FILE)
    return db.cursor()

def db_close():
    db.commit()
    db.close()

def create_user(username, password):
    c = db_connect()
    c.execute('INSERT INTO users(username, password) VALUES (?, ?);', (username, password))
    db_close()

def user_exist(username):
    c = db_connect()
    c.execute('SELECT username FROM users WHERE username = ?;', (username,))
    check = c.fetchone()
    db_close()
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
    c.execute('SELECT Insult_Text FROM insult WHERE Grass_Level =?;' ,(grass_level,))
    text = c.fetchone()
    db_close()
    return text[1] 
        
def get_userID(username):
    c = db_connect()
    if not user_exist(username):
        return False
    c.execute('SELECT ID FROM users WHERE username =?;', (username,))
    text = c.fetchone()
    db_close()
    return text[0]

def ID_exist(id):
    c = db_connect()
    c.execute('SELECT ID FROM users WHERE id =?;', (id,))
    text = c.fetchone()
    db_close()

    if id is None:
        return False
    return True

def get_grass(id):
    c = db_connect()
    if ID_exist():
        c.execute('SELECT Grass FROM grassmeter WHERE id =?', (id,))
        text = c.fetchone()
        db_close()
        return text[2]
    return False

def update_grass(id, grass):
    c = db_connect()
    old = get_grass(id)
    if ID_exist:
        c.execute('UPDATE grassmeter SET grass =? WHERE id=?', (old + grass, id))
        db_close()
    return False
    