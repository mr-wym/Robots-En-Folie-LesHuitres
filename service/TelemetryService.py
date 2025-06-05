from repository.TelemetryRepository import getValeurs
# ici mettre regle métier pour les valeurs, commandes et robots

def fetchValeurs():
    rows = getValeurs()
    return [
        {
            "id": row[0],
            "speed": row[1],
            "distance": row[2],
        } for row in rows
    ]