import sqlite3

def connect_to_db():
    con = sqlite3.connect("records.db")
    return con.cursor(), con