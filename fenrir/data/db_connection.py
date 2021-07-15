import sqlite3
import os

""" This function will initialize the database on the users local hard drive. It will 
    create the tables needed. This will be run at start up.

"""
PATH_TO_DATABASE = os.path.join('db', 'fenrir.db')


def initialize_db():
    conn = sqlite3.connect(PATH_TO_DATABASE)
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS game_save (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_name text,
                    last_save text,
                    player_level integer,
                    x_location integer,
                    y_location integer       
                    )""")

    conn.commit()
    conn.close()


def connect_to_db():
    return sqlite3.connect(PATH_TO_DATABASE)
