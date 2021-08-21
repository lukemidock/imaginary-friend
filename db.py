import os
import sqlite3

class Database:

    def __init__(self, db_uri):
        self.engine = create_engine('sqlite:///%s', db_uri)