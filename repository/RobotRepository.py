import sqlite3
from database.database import connectToDb



def getValeurs():
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM VALEURS")
    rows = cursor.fetchall()
    conn.close()

    return rows

def setValeurs():
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO VALEURS (speed, distance, timestamp, pincevalue) VALUES (?, ?, ?, ?)
    """, (1.5, 20.0, "2025-06-01 10:00:01", True))
    conn.commit()
    conn.close()


def getCommandes():
    # peut être ici rajouter récupérer les commandes pour un robot précis
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM COMMANDE")
    rows = cursor.fetchall()
    conn.close()

    return rows

def setCommandes():
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO COMMANDE (datetime, commande) VALUES (?, ?)
    """, ("2025-06-01 10:00:00", "START"))
    conn.commit()
    conn.close()


def getRobots():
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ROBOTS")
    rows = cursor.fetchall()
    conn.close()

    return rows

def setRobots():
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO ROBOTS (macadress) VALUES (?)
    """, ("AA:BB:CC:DD:EE:FF",))
    conn.commit()
    conn.close()


# fonction qui récupère les commandes pour le robot dans la bd
# fonction qui récupère les robots dans la bd
# fonction qui initialise les commandes pour le robot dans la bd
# fonction qui initialise les robots dans la bd
# fonction qui initialise les valeurs pour le robot dans la bd
