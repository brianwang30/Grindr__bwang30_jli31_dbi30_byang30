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
c.execute("CREATE TABLE if not Exists grassameter(ID INTEGER PRIMARY KEY AUTOINCREMENT, Quiz_Grass INTEGER, Grass INTEGER);")
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
    check = c.fetchone();
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

        
