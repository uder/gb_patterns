import sqlite3

def create_connection():
    connection=sqlite3.connect('db.sqlite')
    return connection
