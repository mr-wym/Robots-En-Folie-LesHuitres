from database.database import connectToDb
import json


# Fonction qui récupère les missions pour un robot précis dans la bd
def getMissions(robot_id):
    conn = connectToDb()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT mission FROM MISSION
            WHERE robot_id = ?
              AND (isdone IS NULL OR isdone = 0)
            ORDER BY datetime DESC
            LIMIT 1
        """, (robot_id,))
        row = cursor.fetchone()
        tab = json.loads(row[0]) if row else None
        print(f"getMissions : {tab}")
        return tab
    finally:
        conn.close()
        
# Fonction qui récupère toutes les missions
def getAllMissions(robot_id):
    conn = connectToDb()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT mission FROM MISSION
            WHERE robot_id = ?
            ORDER BY datetime DESC
            LIMIT 1
        """, (robot_id,))
        row = cursor.fetchone()
        tab = json.loads(row[0]) if row else None
        print(f"getMissions : {tab}")
        return tab
    finally:
        conn.close() 

# Fonction qui initialise une mission
def setMission(datetime, mission, robot_id):
    conn = connectToDb()
    cursor = conn.cursor()
    mission_str = json.dumps(mission)
    cursor.execute("""
        INSERT INTO MISSION (datetime, mission, robot_id) VALUES (?, ?, ?)
    """, (datetime, mission_str, robot_id))
    conn.commit()
    conn.close()

# Fonction qui vérifie si une mission existe déjà pour une datetime dans la bd
def missionExists(datetime, mission, robot_id):
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM MISSION WHERE datetime = ? AND mission = ? AND robot_id = ?", (datetime, mission, robot_id))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists
    
