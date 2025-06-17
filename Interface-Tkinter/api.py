import requests
from datetime import datetime
import re

urlBase = "http://localhost:8000/"

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


def preparationEnvoieRobot(macEntry, aliasEntry, labelRequest, updateDropdown_callback):
    macAddress = macEntry.get()
    macEntry.delete(0, 'end')
    aliasName = aliasEntry.get()
    aliasEntry.delete(0, 'end')

    payload = {
        "macAddress": macAddress,
        "alias": aliasName if aliasName else ""
    }

    urlFinal = urlBase + "robotInitialize"
    envoie(urlFinal, payload, labelRequest, updateDropdown_callback)

def preparationEnvoieMission(checkpoints, alias, labelRequest, updateDropdown_callback):
    # Construire la liste des missions à partir des checkpoints
    mission_list = [selected_cube.get().split(" - ")[0] for (_, selected_cube) in checkpoints]

    # Classe factice pour simuler l'interface attendue par la fonction envoie
    class MissionEntry:
        def get(self): return mission_list
        def delete(self, start, end): pass

    mission_entry = MissionEntry()
    payload = {
        "datetime": datetime.now().isoformat(),
        "mission": mission_entry.get(),
        "alias": alias if alias else ""
    }
    
    print(f"Payload envoyé : {payload}")

    urlFinal = urlBase + "setinstructions"
    mission_entry.delete(0, 'end')
    envoie(urlFinal, payload, labelRequest, updateDropdown_callback)

# def formatMac(event, champMacAdress):
#     contenu = champMacAdress.get()
#     contenu = re.sub(r'[^0-9a-fA-F]', '', contenu)[:12]
#     formate = ":".join([contenu[i:i+2] for i in range(0, len(contenu), 2)])
#     champMacAdress.delete(0, 'end')
#     champMacAdress.insert(0, formate.upper())
