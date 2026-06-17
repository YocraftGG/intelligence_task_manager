import mysql.connector

class DB_connection:
    def get_connection():
        """Returns an active MySQL connection"""
        return mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="1234",
        )


    def create_database():
        """Creates Intelligence_db if it does not exist"""
        conn = DB_connection.get_connection()
        cursor = conn.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS Intelligence_db")
        conn.commit()

        cursor.close()
        conn.close()