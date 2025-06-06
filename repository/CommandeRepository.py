from database.database import connectToDb


# fonction qui récupère les commandes pour le robot dans la bd
def getCommandes():
    # peut être ici rajouter récupérer les commandes pour un robot précis
    # en fonction d'une variable et quand pas définie on renvoie tout les robots
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM COMMANDE")
    rows = cursor.fetchall()
    conn.close()

    return rows

# fonction qui initialise les commandes pour le robot dans la bd
def setCommandes(datetime, commandeValue, macAddress):
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO COMMANDE (datetime, commande, macAddress) VALUES (?, ?, ?)
    """, (datetime, commandeValue, macAddress))
    conn.commit()
    conn.close()

# fonction qui vérifie si une commande existe déjà pour une datetime dans la bd
def commandeExists(datetime, commande, macAddress):
    conn = connectToDb()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM COMMANDE WHERE datetime = ? AND commande = ? AND macAddress = ?", (datetime, commande, macAddress))
    # cursor.execute("SELECT 1 FROM COMMANDE WHERE commande = ?", (commande,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists
