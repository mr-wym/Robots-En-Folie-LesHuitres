from database.database import connectToDb
from repository.InstructionsRepository import getMissionId


# fonction qui récupère les valeurs pour le robot dans la bd
def getTelemetry():
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TELEMETRY")
    rows = cursor.fetchall()
    conn.close()
# mettre ici directement le json
    return rows

# fonction qui récupère les valeurs pour le robot dans la bd selon le robot_id
def getTelemetryById(robot_id):
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TELEMETRY WHERE robot_id = ?", (robot_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# fonction qui initialise les valeurs pour le robot dans la bd
# def setTelemetry(vitesse, distance_ultrason, status_deplacement, ligne, pince_active, robot_id):
def setTelemetry(vitesse, dist, statusDeplacement, statusLigne, pinceValue, uuidNous):

    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO TELEMETRY (vitesse, dist, statusDeplacement, statusLigne, pinceValue, robot_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (vitesse, dist, statusDeplacement, statusLigne, pinceValue, uuidNous))
    conn.commit()
    conn.close()

def updateSummary(robot_id):
    mission_id = getMissionId(robot_id)
    print("updateSummary : ", mission_id)
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE MISSION SET IsDone = TRUE WHERE id = ?
    """, (mission_id,))
    conn.commit()
    conn.close()