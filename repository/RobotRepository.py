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
def setRobots():
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ROBOTS (macadress) VALUES (?)
    """, ("AA:BB:CC:DD:EE:FF",))
    conn.commit()
    conn.close()
