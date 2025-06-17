from database.database import connectToDb


# fonction qui récupère les valeurs pour le robot dans la bd
def getTelemetry():
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TELEMETRY")
    rows = cursor.fetchall()
    conn.close()
# mettre ici directement le json
    return rows

# fonction qui initialise les valeurs pour le robot dans la bd
def setTelemetry(vitesse, distance_ultrason, status_deplacement, ligne, pince_active, robot_id):
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO TELEMETRY (vitesse, distance_ultrason, status_deplacement, ligne, pince_active, robot_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (vitesse, distance_ultrason, status_deplacement, ligne, pince_active, robot_id))
    conn.commit()
    conn.close()

def setSummary(robot_id):
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO TELEMETRY (robot_id) VALUES (?)
    """, (robot_id,))
    conn.commit()
    conn.close()