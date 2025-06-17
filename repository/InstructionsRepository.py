from database.database import connectToDb
import json


# fonction qui récupère les commandes pour le robot dans la bd
def getMissions(robot_id):
    conn = connectToDb()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT mission FROM MISSION WHERE robot_id = ?", (robot_id,))
        rows = cursor.fetchall()
        print(f"getMissions: {rows}")
        return rows
    finally:
            conn.close()

# fonction qui initialise les commandes pour le robot dans la bd
def setMissions(datetime, mission, robot_id):
    conn = connectToDb()
    cursor = conn.cursor()
    mission_str = json.dumps(mission)
    cursor.execute("""
        INSERT INTO MISSION (datetime, mission, robot_id) VALUES (?, ?, ?)
    """, (datetime, mission_str, robot_id))
    conn.commit()
    conn.close()

# fonction qui vérifie si une commande existe déjà pour une datetime dans la bd
def missionExists(datetime, mission, robot_id):
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM MISSION WHERE datetime = ? AND mission = ? AND robot_id = ?", (datetime, mission, robot_id))
    # cursor.execute("SELECT 1 FROM MISSION WHERE mission = ?", (mission,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists
