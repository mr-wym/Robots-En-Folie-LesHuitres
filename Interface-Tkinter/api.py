import requests
from datetime import datetime
# Fichier qui contient toutes les fonctions pour les contacts avec l'api

urlBase = "http://localhost:8000/" # URL de l'api

# Fonction qui envoie a l'api
def envoie(urlFinal, payload, labelRequest, updateDropdown_callback):
    try:
        response = requests.post(urlFinal, json=payload)
        if response.status_code == 201:
            message = response.json().get("status", "")
            labelRequest.config(text=f"{message}", fg="green")
        elif response.status_code == 409:
            message = response.json().get("error", "")
            labelRequest.config(text=f"{message}", fg="red")
        else:
            labelRequest.config(text=f"{response.text}", fg="red")
        labelRequest.after(3000, lambda: labelRequest.config(text=""))
    except Exception as e:
        print(f"Erreur de connexion à l'API : {e}")
        labelRequest.config(text="Connexion à l'API échouée", fg="red")
    
    updateDropdown_callback()

# Fonction qui récupère la liste des alias des robots
def getRobotListAlias():
    try:
        response = requests.get(urlBase + "robots")
        if response.status_code == 200:
            data = response.json()
            rows = data.get("rows", [])
            return [robot.get("alias", "Inconnu") for robot in rows]
        else:
            return []
    except Exception as e:
        print(f"Erreur connexion API robots : {e}")
        return []

# Fonction qui récupère la telemetrie du robot
def getTelemetry():
    try:
        response = requests.get(urlBase + "telemetry")
        if response.status_code == 200:
            data = response.json()
            rows = data.get("rows", [])
            return rows
        else:
            return []
    except Exception as e:
        print(f"Erreur connexion API telemetry : {e}")
        return []

# Fonction de préparation des données avant l'envoie
def preparationEnvoieRobot(uuidEntry, aliasEntry, labelRequest, updateDropdown_callback):
    uuid = uuidEntry.get()
    uuidEntry.delete(0, 'end')
    aliasName = aliasEntry.get()
    aliasEntry.delete(0, 'end')

    payload = {
        "uuid": uuid,
        "alias": aliasName if aliasName else ""
    }

    print(f"Donnée envoyé : {payload}")

    urlFinal = urlBase + "robotInitialize"
    envoie(urlFinal, payload, labelRequest, updateDropdown_callback)

# Fonction de préparation des données avant l'envoie
def preparationEnvoieMission(checkpoints, alias, labelRequest, updateDropdown_callback):
    mission_list = [int(selected_cube.get().split(" - ")[0]) for (_, selected_cube) in checkpoints]

    class MissionEntry:
        def get(self): return mission_list
        def delete(self, start, end): pass

    mission_entry = MissionEntry()
    payload = {
        "datetime": datetime.now().isoformat(),
        "mission": mission_entry.get(),
        "alias": alias if alias else ""
    }
    
    print(f"Donnée envoyé : {payload}")

    urlFinal = urlBase + "setinstructions"
    mission_entry.delete(0, 'end')
    envoie(urlFinal, payload, labelRequest, updateDropdown_callback)
