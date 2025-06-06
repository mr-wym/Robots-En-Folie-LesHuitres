from repository.RobotRepository import getRobots
# ici mettre regle métier pour les valeurs, commandes et robots


def fetchRobots():
    rows = getRobots()
    return [
        {
            "id": row[0],
            "macaddress": row[1],
            "alias": row[2]
        } for row in rows
    ]
