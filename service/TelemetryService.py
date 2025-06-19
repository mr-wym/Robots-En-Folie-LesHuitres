from repository.TelemetryRepository import getTelemetry, setTelemetry, updateSummary
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


def setSummaryAndVerif(robot_id):
    if not isinstance(robot_id, str):
        raise ValueError("Robot ID must be a string")
    
    print(f"Setting summary for robot {robot_id}")
    
    updateSummary(robot_id)

# def setSummaryFinishAndVerif(robot_id):
#     if not isinstance(robot_id, str):
#         raise ValueError("Robot ID must be a string")
    
#     # Here you would implement the logic to set the summary for the robot
#     # For now, we will just print a message
#     print(f"Setting summary finish for robot {robot_id}")
    
#     # In a real application, you would save this summary to a database or perform some other action
#     # For example:
#     # saveSummaryToDatabase(robot_id)

#     updateSummary(robot_id)