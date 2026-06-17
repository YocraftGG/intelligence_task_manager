from db_connection import DB_connection
from agent_db import AgentDB


class MissionDB:
    def get_risk_level(data):
        risk_level = data["difficulty"] * 2 + data["importance"]

        if risk_level <= 9: return "LOW"
        elif risk_level <= 17: return "MEDIUM"
        elif risk_level <= 24: return "HIGH"
        else: return "CRITICAL"


    def create_mission(data):
        conn = DB_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        risk_level = MissionDB.get_risk_level(data)

        sql = """
            INSERT INTO Intelligence_db.missions 
            (title, description, location, difficulty, 
            importance, status, risk_level, assigned_agent_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
        values = (
            data["title"], 
            data["description"], 
            data["location"], 
            data["difficulty"], 
            data["importance"], 
            data["status"],
            risk_level,
            data["assigned_agent_id"]
        )

        cursor.execute(sql, values)
        conn.commit()
        
        new_id = cursor.lastrowid
        return MissionDB.get_mission_by_id(new_id)
    

    def get_all_missions():
        conn = DB_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM Intelligence_db.missions")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()
        return rows


    def get_mission_by_id(id):
        conn = DB_connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM Intelligence_db.missions WHERE id = %s", (id,))
        row = cursor.fetchone()
        
        cursor.close()
        conn.close()
        return row
    

    def assign_mission(m_id, a_id):
        conn = DB_connection.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            UPDATE Intelligence_db.missions SET 
            assigned_agent_id = %s, status = "ASSIGNED"
            WHERE id = %s
            """, (a_id, m_id)
        )
        conn.commit()

        assigned = cursor.rowcount > 0
        
        cursor.close()
        conn.close()
        return assigned
    

    def update_mission_status(id, status):
        conn = DB_connection.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            UPDATE Intelligence_db.missions SET 
            status = %s WHERE id = %s
            """, (status, id)
        )
        conn.commit()

        assigned = cursor.rowcount > 0
        
        cursor.close()
        conn.close()
        return assigned


    def get_open_missions_by_agent(id):
        conn = DB_connection.get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT * FROM Intelligence_db.missions
            WHERE assigned_agent_id = %s AND
            (status = "ASSIGNED" OR status = "IN_PROGRESS")
            """, (id,)
        )
        rows = cursor.fetchall()

        cursor.close()
        conn.close()
        return rows
    

    def count_all_missions():
        conn = DB_connection.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM Intelligence_db.missions")
        count = cursor.fetchone()[0]

        cursor.close()
        conn.close()
        return count
    

    def count_by_status(status):
        conn = DB_connection.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*) FROM Intelligence_db.missions
            WHERE status = %s
            """, (status,)
        )
        count = cursor.fetchone()[0]

        cursor.close()
        conn.close()
        return count
    

    def count_open_missions():
        conn = DB_connection.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*) FROM Intelligence_db.missions
            WHERE status = "ASSIGNED" OR status = "IN_PROGRESS"
            """
        )
        count = cursor.fetchone()[0]

        cursor.close()
        conn.close()
        return count
    

    def count_critical_missions():
        conn = DB_connection.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*) FROM Intelligence_db.missions
            WHERE risk_level = "CRITICAL"
            """
        )
        count = cursor.fetchone()[0]

        cursor.close()
        conn.close()
        return count


    def get_top_agent():
        conn = DB_connection.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*) FROM Intelligence_db.missions
            WHERE status = COMPLETED
            GROUP BY assigned_agent_id
            ORDER BY DESC
            LIMIT 1
            """
        )
        id = cursor.fetchone()[0]

        agent = AgentDB.get_agent_by_id(id)
        cursor.close()
        conn.close()
        return agent
    

print(MissionDB.get_all_missions())
# print(MissionDB.create_mission({
#     "title":"clean",
#     "description":"have to clean",
#     "location":"kitchen",
#     "difficulty":4,
#     "importance":3,
#     "status":"NEW",
#     "assigned_agent_id":None
# }))
print(MissionDB.count_critical_missions())
print(MissionDB.get_all_missions())