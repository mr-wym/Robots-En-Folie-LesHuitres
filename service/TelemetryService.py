from repository.TelemetryRepository import getTelemetry, setTelemetry, updateSummary

# Fonction qui appelle getTelemetry qui va récupérer la telemetrie
def fetchTelemetry():
    rows = getTelemetry()
    return [
        {
            "id": row[0],
            "vitesse": row[1],
            "distance": row[2],
            "statut_deplacement": row[3],
            "statut_ligne": row[4],
            "status_pince": row[5],
            "robot_id": row[6]
        } for row in rows
    ]
    
# Fonction qui vérifie le bon format des données 
def setTelemetryAndVerif(vitesse, dist, statusDeplacement, statusLigne, pinceValue, uuidNous):

    if not isinstance(vitesse, (int, float)):
        raise ValueError("Vitesse must be a number")
    if not isinstance(dist, (int, float)):
        raise ValueError("Distance must be a number")
    if not isinstance(statusDeplacement, str):
        raise ValueError("Status deplacement must be a string")
    if not isinstance(statusLigne, int):
        raise ValueError("Ligne must be an integer")
    if not isinstance(pinceValue, bool):
        raise ValueError("Pince active must be a boolean")
    if not isinstance(uuidNous, str):
        raise ValueError("Robot ID must be a string")

    setTelemetry(vitesse, dist, statusDeplacement, statusLigne, pinceValue, uuidNous)

# Fonction qui vérifie le format des données 
def setSummaryAndVerif(robot_id):
    if not isinstance(robot_id, str):
        raise ValueError("Robot ID must be a string")
    
    print(f"Setting summary for robot {robot_id}")
    
    updateSummary(robot_id)
