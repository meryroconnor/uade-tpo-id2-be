import mysql.connector
from decouple import config

MYSQL_HOST = config("MYSQL_HOST")
MYSQL_PORT = config("MYSQL_PORT")
MYSQL_USER = config("MYSQL_USER")
MYSQL_PASS = config("MYSQL_PASS")
MYSQL_DB_NAME = config("MYSQL_DB_NAME")

class MysqlConn(object):

    connection = None

    def __init__(self):
        if self.connection is None:
            try:
                self.connection = mysql.connector.connect(
                    host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASS, database=MYSQL_DB_NAME)
            except Exception as error:
                print("Error: Connection not established {}".format(error))
            else:
                print("Connection established")

    def getConnection(self):
        return self.connection

    def fetch(self, query, data):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, data)
            rows = cursor.fetchall()
            result = []
            for row in rows:
                item = {}
                for i, col in enumerate(cursor.description):
                    item[col[0]] = row[i]
                result.append(item)
            cursor.close()
            return result
        except Exception as error:
            raise Exception(error)

    def insert(self, query, data):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, data)
            rowId = cursor.lastrowid
            self.connection.commit()
            cursor.close()
            return rowId
        except Exception as error:
            raise Exception(error)
