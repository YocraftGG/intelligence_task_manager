import mysql.connector

class DB_connection:
    @staticmethod
    def get_connection():
        """Returns an active MySQL connection"""
        return mysql.connector.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="1234",
        )


    @staticmethod
    def create_database():
        """Creates Intelligence_db if it does not exist"""
        conn = DB_connection.get_connection()
        cursor = conn.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS Intelligence_db")
        conn.commit()

        cursor.close()
        conn.close()
    

    @staticmethod
    def create_tables():
        conn = DB_connection.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Intelligence_db.agents(
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50),
                specialty VARCHAR(50),
                is_active BOOLEAN DEFAULT TRUE ,
                completed_missions INT DEFAULT 0,
                failed_missions INT DEFAULT 0,
                agent_rank ENUM("Junior", "Senior", "Commander")
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Intelligence_db.missions(
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(50),
                description TEXT,
                location VARCHAR(250),
                difficulty INT,
                importance INT,
                status VARCHAR(50) DEFAULT "NEW",
                risk_level VARCHAR(50),
                assigned_agent_id INT DEFAULT NULL
            )
            """
        )
        conn.commit()

        cursor.close()
        conn.close()