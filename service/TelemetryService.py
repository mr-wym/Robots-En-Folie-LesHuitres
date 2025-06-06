from repository.TelemetryRepository import getTelemetry
# ici mettre regle métier pour les valeurs, commandes et robots

def fetchTelemetry():
    rows = getTelemetry()
    return [
        {
            "id": row[0],
            "speed": row[1],
            "distance": row[2],
        } for row in rows
    ]