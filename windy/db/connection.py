import sqlite3
from windy.include_patterns.singleton import Singleton

def create_connection(dbfile='db.sqlite'):
    # connection=sqlite3.connect('db.sqlite')
    dbsqlite=DbSqlite3(dbfile)
    connection=dbsqlite.connection
    return connection

class DbSqlite3(metaclass=Singleton):
    def __init__(self,dbfile='db.sqlite'):
        self.dbfile=dbfile
        self.connection=self.get_connection()

    def get_connection(self):
        connection = sqlite3.connect('db.sqlite')
        return connection

