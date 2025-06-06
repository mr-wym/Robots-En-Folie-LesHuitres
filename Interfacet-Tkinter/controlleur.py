import tkinter as tk
import requests
from datetime import datetime
import re

urlBase = "http://localhost:8000/api/"

## mettre dans l'API et la base de donnée le champ pour l'alias des robots en fonciton de leurs adresses mac
## rajouter un champ à côté du champ de saisie de ladresse mac pour pouvoir renseigner un alias et 
# je veux pas que cet alias soit obligatoire mais juste qu'on puisse le mettre si on le souhaite
# je veux que le dropdown récupère donc tout les alias des robots et pas seulement les macs dans l'API

windows = tk.Tk()
windows.title("Controlleur REFRIGERATEUR")
windows.geometry("500x500")

def preparationEnvoieRobot(mac: tk.Entry, alias: tk.Entry, labelConfirmation):
    macAddress = mac.get()
    mac.delete(0, tk.END)
    aliasName = alias.get()
    alias.delete(0, tk.END)

    payload = {
        "macAddress": macAddress,
        "alias": aliasName if aliasName else ""
    }

    print(f"Payload envoyé : {payload}")
    urlFinal = urlBase + "robotInitialize"
    print(f"final url : {urlFinal}")

    envoie(urlFinal, payload, labelConfirmation)


def preparationEnvoieCommande(commande, alias: tk.Entry, labelConfirmation):

    payload = {
        "datetime": datetime.now().isoformat(),
        "commande": commande.get(),
        "alias": alias if alias else ""
    }

    print(f"Payload envoyé : {payload}")
    urlFinal = urlBase + "commandeInitialize"
    print(f"final url : {urlFinal}")

    commande.delete(0, tk.END)

    envoie(urlFinal, payload, labelConfirmation)


def envoie(urlFinal, payload, labelConfirmation):
    # QUAND JUSTE UNE ERREUR AFFICHER JUSTE L'ERREUR PAR TOUTE LA TRUC
    try:
        response = requests.post(urlFinal, json=payload)
        if response.status_code == 201:
            print(f"Commande envoyée avec succès à {urlFinal}")
            # labelConfirmation.config(text="Ajout réussi !", fg="green")
            message = response.json().get("status", "")
            labelConfirmation.config(text=f"{message}", fg="green")
        elif response.status_code == 409:
            print(f"Conflit : {response.status_code} - {response.text}")
            message = response.json().get("error", "")
            labelConfirmation.config(text=f"{message}", fg="red")
            # labelConfirmation.config(text=f"{response.text}", fg="red")
        else:
            print(f"Response : {response.status_code} - {response.text}")
            labelConfirmation.config(text=f"{response.text}", fg="red")

            # message = response.json().get("error", "")
            # labelConfirmation.config(text=f"{message}", fg="red")


        labelConfirmation.after(3000, lambda: labelConfirmation.config(text=""))
        
    except Exception as e:
        print(f"Erreur de connexion à l'API : {e}")
        labelConfirmation.config(text="Connexion à l'API échouée", fg="red")

    # Rafraîchir l'interface
    robot_list = getRobotList()
    if not robot_list:
        robot_list = ["Aucun robot"]  # valeur de secours

    # Mettre à jour le menu déroulant
    menu = dropdown["menu"]
    menu.delete(0, "end")
    for alias in robot_list:
        menu.add_command(label=alias, command=lambda value=alias: selected_alias.set(value))

    # Réinitialiser la sélection
    selected_alias.set(robot_list[0])

def formatMac(event):
    contenu = champ1.get()

    contenu = re.sub(r'[^0-9a-fA-F]', '', contenu)
    contenu = contenu[:12]
    formate = ":".join([contenu[i:i+2] for i in range(0, len(contenu), 2)])
    champ1.delete(0, tk.END)
    champ1.insert(0, formate.upper())

def getRobotList():
    try:
        response = requests.get(urlBase + "robots")
        # print(f"Response robots : {response.status_code} - {response.text}")
        if response.status_code == 200:
            data = response.json()
            rows = data.get("rows", [])
            return [robot.get("alias", "Inconnu") for robot in rows]
        else:
            print(f"Erreur API robots : {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print(f"Erreur connexion API robots : {e}")
        return []
    

def placeHolder(entry, placeholder_text):
    ## pas faire de fonction avec des fonctions dedans tout séparer
    entry.insert(0, placeholder_text)
    entry.config(fg='grey')

    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, tk.END)
            entry.config(fg='black')

    def on_focus_out(event):
        if entry.get() == '':
            entry.insert(0, placeholder_text)
            entry.config(fg='grey')

    entry.bind('<FocusIn>', on_focus_in)
    entry.bind('<FocusOut>', on_focus_out)

frame1 = tk.Frame(windows)
frame1.pack(pady=10)

label1 = tk.Label(frame1, text="Ajouter un robot :")
label1.pack(anchor='w')

labelConfirmation1 = tk.Label(frame1, text="", fg="green")
labelConfirmation1.pack(anchor='w')

sous_frame1 = tk.Frame(frame1)
sous_frame1.pack()

champ1 = tk.Entry(frame1, width=17)
champ1.pack(side=tk.LEFT, padx=(0, 10))

champ3 = tk.Entry(frame1, width=17)
champ3.pack(side=tk.LEFT, padx=(0, 10))

placeHolder(champ1, "AA:BB:CC:DD:EE:FF")
placeHolder(champ3, "Alias")

# champ1.bind("<Return>", lambda event: envoyer_texte(champ3, "robotInitialize", labelConfirmation1))

champ1.bind("<KeyRelease>", formatMac)

champ1.bind("<Return>", lambda event: preparationEnvoieRobot(champ1, champ3, labelConfirmation1))
champ3.bind("<Return>", lambda event: preparationEnvoieRobot(champ1, champ3, labelConfirmation1))


bouton1 = tk.Button(frame1, text="Envoyer", command=lambda: preparationEnvoieRobot(champ1, champ3, labelConfirmation1))
bouton1.pack(side=tk.LEFT)


frame2 = tk.Frame(windows)
frame2.pack(pady=10)

label2 = tk.Label(frame2, text="Commande pour le robot :")
label2.pack(anchor='w')

labelConfirmation2 = tk.Label(frame2, text="", fg="green")
labelConfirmation2.pack(anchor='w')

sous_frame2 = tk.Frame(frame2)
sous_frame2.pack()

champ2 = tk.Entry(frame2, width=30)
champ2.pack(side=tk.LEFT, padx=(0, 10))

robot_list = getRobotList()
if not robot_list:
    robot_list = ["Aucun robot"]  # valeur de secours

selected_alias = tk.StringVar(value=robot_list[0])

dropdown = tk.OptionMenu(sous_frame2, selected_alias, *robot_list)
dropdown.pack(side=tk.LEFT)

champ2.bind("<Return>", lambda event: preparationEnvoieCommande(champ2, selected_alias.get(), labelConfirmation2))


bouton2 = tk.Button(frame2, text="Envoyer", command=lambda: preparationEnvoieCommande(champ2, selected_alias.get(), labelConfirmation2))
bouton2.pack(side=tk.LEFT)


windows.mainloop()
