from database.database import connectToDb
import json


# fonction qui récupère les commandes pour le robot dans la bd
def getMissions(robot_id):
    conn = connectToDb()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT mission, isdone FROM MISSION
            WHERE robot_id = ?
            ORDER BY datetime DESC
            LIMIT 1
        """, (robot_id,))
        row = cursor.fetchone()
        if row:
            mission_data, isdone = row
            if isdone is None or isdone == 0 or isdone is False:
                tab = json.loads(mission_data)
                print(f"getMissions : {tab}")
                return tab
            else:
                print("getMissions : Mission déjà terminée (isdone=True)")
                return None
        else:
            return None
    finally:
        conn.close()

def getMissionId(robot_id):
    conn = connectToDb()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id FROM MISSION
            WHERE robot_id = ?
            ORDER BY datetime DESC
            LIMIT 1
        """, (robot_id,))
        row = cursor.fetchone()
        mission_id = row[0] if row else None
        return mission_id
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
    
