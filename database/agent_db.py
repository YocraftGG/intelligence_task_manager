from db_connection import DB_connection


class AgentDB:
    def create_agent(data):
        conn = DB_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        sql = """
            INSERT INTO Intelligence_db.agents 
            (name, specialty, is_active, completed_missions, failed_missions, agent_rank)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
        values = (
            data["name"], 
            data["specialty"], 
            data["is_active"], 
            data["completed_missions"], 
            data["failed_missions"], 
            data["agent_rank"]
        )

        cursor.execute(sql, values)
        conn.commit()
        
        new_id = cursor.lastrowid
        return AgentDB.get_agent_by_id(new_id)
    

    def get_all_agents():
        conn = DB_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Intelligence_db.agents")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()
        return rows


    def get_agent_by_id(id):
        conn = DB_connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM Intelligence_db.agents WHERE id = %s", (id,))
        row = cursor.fetchone()
        
        cursor.close()
        conn.close()
        return row


    def update_agent(id, data):
        conn = DB_connection.get_connection()
        cursor = conn.cursor()

        set_clause = ", ".join(f"{key} = %s" for key in data.keys())
        
        cursor.execute(
            f"UPDATE Intelligence_db.agents SET {set_clause} WHERE id = %s",
            list(data.values()) + [id]
        )
        conn.commit()

        updated = cursor.rowcount > 0
        
        cursor.close()
        conn.close()
        return updated
    

    def deactivate_agent(id):
        conn = DB_connection.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            UPDATE Intelligence_db.agents SET 
            is_active = FALSE WHERE id = %s
            """, (id,)
        )
        conn.commit()

        deactivated = cursor.rowcount > 0
        
        cursor.close()
        conn.close()
        return deactivated
    

    def increment_completed(id):
        conn = DB_connection.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            UPDATE Intelligence_db.agents SET 
            completed_missions = completed_missions + 1 WHERE id = %s
            """, (id,)
        )
        conn.commit()

        incremented = cursor.rowcount > 0
        
        cursor.close()
        conn.close()
        return incremented
    

    def increment_failed(id):
        conn = DB_connection.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            UPDATE Intelligence_db.agents SET 
            failed_missions = failed_missions + 1 WHERE id = %s
            """, (id,)
        )
        conn.commit()

        incremented = cursor.rowcount > 0
        
        cursor.close()
        conn.close()
        return incremented
    

    def get_agent_performance(id):
        conn = DB_connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute(
            """
            SELECT completed_missions AS completed, failed_missions AS failed
            FROM Intelligence_db.agents WHERE id = %s
            """, (id,)
        )
        row = cursor.fetchone()
        
        cursor.close()
        conn.close()

        total = row["completed"] + row["failed"]
        
        if total > 0: success_rate = int(row["completed"] / (total / 100))
        else: success_rate = 0

        return {
            "completed": row["completed"],
            "failed": row["failed"],
            "total": total,
            "success_rate": success_rate,
            }
    

    def count_active_agents():
        conn = DB_connection.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*) FROM Intelligence_db.agents 
            WHERE is_active = TRUE
            """
        )
        count = cursor.fetchone()[0]

        cursor.close()
        conn.close()
        return count