from repository.CommandeRepository import getCommandes
# ici mettre regle métier pour les valeurs, commandes et robots


def fetchCommandes():
    rows = getCommandes()
    return [
        {
            "id": row[0],
            "datetime": row[1],
            "commande": row[2],
        } for row in rows
    ]


# mettre le json a la toute fin c'est a dire dans le controller
