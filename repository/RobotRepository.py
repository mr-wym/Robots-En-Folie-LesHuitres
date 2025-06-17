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
def setRobots(robot_id, alias):
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ROBOTS (robot_id, alias) VALUES (?, ?)
    """, (robot_id, alias, ))
    conn.commit()
    conn.close()

# fonction qui vérifier si l'adresse max existe déjà dans la bd
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
    # peut être au dessus rajouter le truc qui vérifier si l'alias existe déjà dans la bd

# def getRobotIdAlias(alias):
#     conn = connectToDb()
#     cursor = conn.cursor()
#     cursor.execute("SELECT macAddress FROM ROBOTS WHERE alias = ?", (alias,))
#     macAddress = cursor.fetchall()
#     conn.close()
#     if macAddress:
#         return macAddress[0]

#     return None

def getRobotIdAlias(alias):
    conn = connectToDb()
    try: 
        cursor = conn.cursor()
        result = cursor.execute("SELECT robot_id FROM robots WHERE alias = ?", (alias,)).fetchone()
        
        return result[0] if result else None

    finally:
        conn.close()
