from database.database import connectToDb


# fonction qui récupère les commandes pour le robot dans la bd
def getCommandes():
    # peut être ici rajouter récupérer les commandes pour un robot précis
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM COMMANDE")
    rows = cursor.fetchall()
    conn.close()

    return rows

# fonction qui initialise les commandes pour le robot dans la bd
def setCommandes():
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO COMMANDE (datetime, commande) VALUES (?, ?)
    """, ("2025-06-01 10:00:00", "START"))
    conn.commit()
    conn.close()