import os
import sqlite3

db_name = 'MasterMind.db'
path = os.path.dirname(os.path.abspath(__file__))


class db_connection:

    @staticmethod
    def select_query(query: str, data=None):
        conn = sqlite3.connect(os.path.join(path, db_name))
        cursor = conn.cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        returnable = cursor.fetchall()
        conn.close()
        return returnable

    @staticmethod
    def query(query: str, data=None):
        conn = sqlite3.connect(os.path.join(path, db_name))
        cursor = conn.cursor()
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        conn.commit()
        conn.close()

