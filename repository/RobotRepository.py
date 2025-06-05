from database.database import connectToDb


# fonction qui récupère les robots dans la bd
def getRobots():
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ROBOTS")
    rows = cursor.fetchall()
    conn.close()

    return rows

# fonction qui initialise les robots dans la bd
def setRobots(macAddress):
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ROBOTS (macadress) VALUES (?)
    """, (macAddress,))
    conn.commit()
    conn.close()

# fonctio qui vérifier si l'adresse max existe déjà dans la bd
def macAddressExists(macAddress):
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM ROBOTS WHERE macadress = ?", (macAddress,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists
