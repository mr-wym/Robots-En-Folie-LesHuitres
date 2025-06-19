from database.database import connectToDb
from repository.InstructionsRepository import getMissionId


# Fpnction qui récupère les telemetry 
def getTelemetry():
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TELEMETRY")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Fonction qui récupère les telemetry pour le robot selon le robot_id
def getTelemetryById(robot_id):
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TELEMETRY WHERE robot_id = ?", (robot_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# Fonction qui initialise les telemetry pour le robot dans la bd
def setTelemetry(vitesse, dist, statusDeplacement, statusLigne, pinceValue, uuidNous):
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO TELEMETRY (vitesse, dist, statusDeplacement, statusLigne, pinceValue, robot_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (vitesse, dist, statusDeplacement, statusLigne, pinceValue, uuidNous))
    conn.commit()
    conn.close()

# Fonction qui met a jour la mission pour la passer a fait quand elle est finie
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