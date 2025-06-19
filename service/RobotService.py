from repository.RobotRepository import getRobots
from repository.RobotRepository import setRobots

# Fonciton qi appel getRobots pour retourner les robots 
def fetchRobots():
    rows = getRobots()
    return [
        {
            "id": row[0],
            "macaddress": row[1],
            "alias": row[2]
        } for row in rows
    ]

# Fonction qui vérifie le format des données
def setRobotAndVerify(robot_id, alias):
    
    if not isinstance(robot_id, int):
        raise ValueError("robot_id must be an integer")
    if not isinstance(alias, str):
        raise ValueError("alias must be a string")
    
    setRobots(robot_id, alias)
