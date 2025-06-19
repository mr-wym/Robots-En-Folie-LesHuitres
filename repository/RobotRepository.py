from database.database import connectToDb


# Fonction qui récupère les robots dans la bd
def getRobots():
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ROBOTS")
    rows = cursor.fetchall()
    conn.close()

    return rows

# Fonction qui initialise les robots dans la bd
def setRobots(robot_id, alias):
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ROBOTS (robot_id, alias) VALUES (?, ?)
    """, (robot_id, alias, ))
    conn.commit()
    conn.close()

# Fonction qui vérifier si l'adresse max existe déjà dans la bd
def robotIdExists(robotId, alias=None):
    conn = connectToDb()
    cursor = conn.cursor()
    if alias:
        cursor.execute("SELECT 1 FROM ROBOTS WHERE robot_id = ? AND alias = ?", (robotId, alias))
    else:
        cursor.execute("SELECT 1 FROM ROBOTS WHERE robot_id = ?", (robotId,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists
    
# Fonction qui récupère l'id du robot en fonction de son alias 
def getRobotIdAlias(alias):
    conn = connectToDb()
    try: 
        cursor = conn.cursor()
        result = cursor.execute("SELECT robot_id FROM robots WHERE alias = ?", (alias,)).fetchone()
        
        return result[0] if result else None

    finally:
        conn.close()
