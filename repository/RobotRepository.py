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
def setRobots(macAddress, alias):
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ROBOTS (macaddress, alias) VALUES (?, ?)
    """, (macAddress, alias, ))
    conn.commit()
    conn.close()

# fonction qui vérifier si l'adresse max existe déjà dans la bd
def macAddressExists(macAddress, alias=None):
    conn = connectToDb()
    cursor = conn.cursor()
    if alias:
        cursor.execute("SELECT 1 FROM ROBOTS WHERE macaddress = ? AND alias = ?", (macAddress, alias))
    else:
        cursor.execute("SELECT 1 FROM ROBOTS WHERE macaddress = ?", (macAddress,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists
    # peut être au dessus rajouter le truc qui vérifier si l'alias existe déjà dans la bd

def getMacAddressAlias(alias):
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("SELECT macAddress FROM ROBOTS WHERE alias = ?", (alias,))
    macAddress = cursor.fetchall()
    conn.close()
    if macAddress:
        return macAddress[0]

    return None