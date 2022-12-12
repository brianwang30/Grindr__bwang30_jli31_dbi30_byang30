from db import *
import sqlite3

#create_user("m",1)
id = get_userID("lol")
update_grass(id,20)
print(get_grass(id))
