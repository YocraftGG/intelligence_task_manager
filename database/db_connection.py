import mysql.connector

class DB_connection:
    def get_connection():
        """Returns an active MySQL connection"""
        return mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="1234",
            database="Intelligence_db"
        )