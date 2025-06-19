from repository.InstructionsRepository import getMissions, setMission

# Fonction qui trie va appeler getMissions qui va récupérer les missions pour un robot 
def fetchMission(robot_id=None):
    rows = getMissions(robot_id)
    print(rows)
    return rows


# Fonction qui vérifie le bon format des données
def setMissionAndVerif(datetime_value, mission, uuid):
    
    if not isinstance(datetime_value, str):
        raise ValueError("Datetime must be a string")
    if not isinstance(mission, str):
        raise ValueError("Mission must be a string")
    if not isinstance(uuid, str):
        raise ValueError("UUID must be a string")
    
    setMission(datetime_value, mission, uuid)