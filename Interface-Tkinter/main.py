import tkinter as tk
import json
# Fichier qui gère l'affichage de l'interface

from api import (
    preparationEnvoieRobot,
    preparationEnvoieMission,
    getTelemetry,
    getRobotListAlias,
)

# Création de la fenpetre
windows = tk.Tk()
windows.title("Controlleur REFRIGERATEUR")
windows.geometry("1000x1000")

checkpoints = []

# Fonction qui met a jout le dropdown de selection des robots
def updateDropdown():
    robotList = getRobotListAlias()
    if not robotList:
        robotList = ["Aucun robot"]
    menu = dropdown["menu"]
    menu.delete(0, "end")
    for alias in robotList:
        menu.add_command(label=alias, command=lambda value=alias: selected_alias.set(value))
    selected_alias.set(robotList[0])

# Fonction qui suprime un checkpoint dans la liste de préparation de mission
def supprimerCheckpoint(checkpoint_frame):
    for i, (frame, var) in enumerate(checkpoints):
        if frame == checkpoint_frame:
            frame.destroy()
            checkpoints.pop(i)
            break

# Fonction qui ajoute un checkpoint a la liste de préparation de mission
def ajouterCheckpoint():
    checkpoint_frame = tk.Frame(frameListeCheckpoints, highlightbackground="black", highlightthickness=2, bd=0)

    checkpoint_frame.pack(pady=5, padx=10, fill="x", anchor="w")


    selected_cube = tk.StringVar(value=cube_options[0][0])
    dropdown_cube = tk.OptionMenu(checkpoint_frame, selected_cube, *(opt[0] for opt in cube_options))
    dropdown_cube.pack(side=tk.LEFT, padx=5, pady=5)

    bouton_supprimer = tk.Button(checkpoint_frame, text="Supprimer", command=lambda: supprimerCheckpoint(checkpoint_frame))
    bouton_supprimer.pack(side=tk.LEFT, padx=5)

    checkpoints.append((checkpoint_frame, selected_cube))

# Frame d'ajout du robot
frameAjoutRobot = tk.Frame(windows)
frameAjoutRobot.pack(pady=10)

# Label "Ajouter un robot"
labelAjoutRobot = tk.Label(frameAjoutRobot, text="Ajouter un robot :")
labelAjoutRobot.pack(anchor='w')

# Label de le réponce de l'api
labelResultRequest1 = tk.Label(frameAjoutRobot, text="", fg="green")
labelResultRequest1.pack(anchor='w')

# Champ pour renseigner l'uid du robot
champRobotId = tk.Entry(frameAjoutRobot, width=17)
champRobotId.pack(side=tk.LEFT, padx=(0, 10))

# Champ pour renseigner l'alias du robot
champAlias = tk.Entry(frameAjoutRobot, width=17)
champAlias.pack(side=tk.LEFT, padx=(0, 10))

champRobotId.bind("<Return>", lambda event: preparationEnvoieRobot(champRobotId, champAlias, labelResultRequest1, updateDropdown))
champAlias.bind("<Return>", lambda event: preparationEnvoieRobot(champRobotId, champAlias, labelResultRequest1, updateDropdown))

# Bouton d'envoie de ajouter robot
boutonAjouterRobot = tk.Button(frameAjoutRobot, text="Envoyer", command=lambda: preparationEnvoieRobot(champRobotId, champAlias, labelResultRequest1, updateDropdown))
boutonAjouterRobot.pack(side=tk.LEFT)



# Frame mission
frameMission = tk.Frame(windows)
frameMission.pack(pady=10)

# Label "Mission pou rle robot"
labelMissionRobot = tk.Label(frameMission, text="Mission pour le robot :")
labelMissionRobot.pack(anchor='w')

# Label résultat de la réponce de l'api
labelResultRequest2 = tk.Label(frameMission, text="", fg="green")
labelResultRequest2.pack(anchor='w')

# Sous frame mission
sousFrameMission = tk.Frame(frameMission)
sousFrameMission.pack()

robotList = getRobotListAlias()
if not robotList:
    robotList = ["Aucun robot"]
selected_alias = tk.StringVar(value=robotList[0])
dropdown = tk.OptionMenu(sousFrameMission, selected_alias, *robotList)
dropdown.pack(side=tk.LEFT, padx=5)

# Liste des cubes avec les couleurs
cube_options = [
    ("2 - Jaune", "2"),
    ("3 - Rouge", "3"),
    ("6 - Rose", "6"),
    ("7 - Violet", "7"),
    ("10 - Vert", "10"),
]

# Frarme de checkpoint
frameCheckpoints = tk.Frame(windows)
frameCheckpoints.pack(pady=10, fill="x", anchor="w")

# Boutton pour ajouter des checkpoint
boutonAjoutCheckpoint = tk.Button(sousFrameMission, text="Ajouter checkpoint", command=ajouterCheckpoint)
boutonAjoutCheckpoint.pack(side=tk.LEFT, padx=5)

# Frame de liste des check point
frameListeCheckpoints = tk.Frame(frameCheckpoints)
frameListeCheckpoints.pack(fill="x", anchor="w")

# Bouton pour envoyer une mission
boutonEnvoieMission = tk.Button(sousFrameMission, text="Envoyer mission", command=lambda: preparationEnvoieMission(checkpoints, selected_alias.get(), labelResultRequest2, updateDropdown))
boutonEnvoieMission.pack(pady=10)
boutonEnvoieMission.pack(side=tk.LEFT, padx=5)



# Frame telemetry
frameTelemetry = tk.Frame(windows, highlightbackground="black", highlightthickness=2, bd=0)
frameTelemetry.pack(pady=20, padx=10, fill="x", anchor="w")

# Label "Telemetry"
labelTelemetry = tk.Label(frameTelemetry, text="Telemetry", font=("Arial", 14, "bold"))
labelTelemetry.pack(anchor='w', padx=5, pady=5)

telemetryText = tk.Text(frameTelemetry, height=10, width=80, state="disabled")
telemetryText.pack(padx=5, pady=5)

telemetry = getTelemetry()
telemetryText.config(state="normal")
telemetryText.delete("1.0", tk.END)
telemetryText.insert(tk.END, json.dumps(telemetry, indent=4, ensure_ascii=False))
telemetryText.config(state="disabled")
