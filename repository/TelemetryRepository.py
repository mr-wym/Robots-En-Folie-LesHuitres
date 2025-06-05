from database.database import connectToDb


# fonction qui récupère les valeurs pour le robot dans la bd
def getValeurs():
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TELEMETRIE")
    rows = cursor.fetchall()
    conn.close()
# mettre ici directement le json
    return rows

# fonction qui initialise les valeurs pour le robot dans la bd
def setValeurs():
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO TELEMETRIE (speed, distance, timestamp, pincevalue) VALUES (?, ?, ?, ?)
    """, (1.5, 20.0, "2025-06-01 10:00:01", True))
    conn.commit()
    conn.close()
