import glob
import sqlite3
from sqlite3 import Error

class SqlProcess:
    def __init__(self, databaseName):
        try:
            sqliteConnection = sqlite3.connect(str(databaseName))
            self.connection = sqliteConnection
            cursor = sqliteConnection.cursor()
            print("Successfully Connected to SQLite")

        except sqlite3.Error as error:
            print("Error while tring to connect", error)

    def execute_query(self, query):
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            print(cursor.fetchall())
            print("Query executed successfully")
        except Error as e:
            print(f"The error '{e}' occurred")

    def insert_data(self, data):
        sql = ''' INSERT INTO library_data VALUES(?,?,?,?,?,?,?) '''
        cur = self.connection.cursor()
        try:
            cur.execute(sql, data)
            self.connection.commit()
            rows = cur.fetchall()
            for row in rows:
                print(row)
        except Error as e:
            print(f"The error '{e}' occurred")

    def query_tree(self, rgbValues):
        rgbValues = (rgbValues[0],rgbValues[0],rgbValues[1],rgbValues[1],rgbValues[2],rgbValues[2])
        sql = '''
                SELECT * FROM library_data
                WHERE Rmin<= ? AND Rmax>= ?
                AND Gmin<= ? AND Gmax>= ?
                AND Bmin<= ? AND Bmax>= ?;
        '''
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, rgbValues)
            self.connection.commit()
            rows = cursor.fetchall()
            for row in rows:
                return row
        except Error as e:
            print(f"The error '{e}' occurred")

    def printDB(self):
        query = '''SELECT * FROM library_data'''
        self.execute_query(query)
