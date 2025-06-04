from repository.RobotRepository import getValeurs, getCommandes, getRobots

def fetchValeurs():
    rows = getValeurs()
    return [
        {
            "id": row[0],
            "speed": row[1],
            "distance": row[2],
        } for row in rows
    ]

def fetchCommandes():
    rows = getCommandes()
    return [
        {
            "id": row[0],
            "datetime": row[1],
            "commande": row[2],
        } for row in rows
    ]

def fetchRobots():
    rows = getRobots()
    return [
        {
            "id": row[0],
            "macadress": row[1],
        } for row in rows
    ]
