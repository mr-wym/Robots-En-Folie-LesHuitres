from repository.InstructionsRepository import getMissions
import json

# ici mettre regle métier pour les valeurs, commandes et robots

def fetchMission(robot_id=None):
    rows = getMissions(robot_id)
    # rows = [json.loads(row[0]) for row in rows]
    print(rows)
    return rows


# mettre le json a la toute fin c'est a dire dans le controller
