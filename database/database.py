import sqlite3
import os
from dotenv import load_dotenv
from uuid import uuid4

def init_db(): # Initialisation de la base de donnée
    load_dotenv()
    conn = connectToDb()
    cursor = conn.cursor()

    # Création de la table mission pour enregistrer les missions
    cursor.execute(""" 
        CREATE TABLE IF NOT EXISTS MISSION (
        id INTEGER PRIMARY KEY,
            datetime TEXT NOT NULL,
            mission TEXT NOT NULL,
            robot_id TEXT NOT NULL,
            isDone BOOLEAN DEFAULT FALSE
        )
    """)

    # Création de la table telemetry pour enregistrer la telemetry des robots
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TELEMETRY (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vitesse FLOAT NOT NULL,
            dist FLOAT NOT NULL,
            statusDeplacement TEXT NOT NULL,
            statusLigne INTEGER NOT NULL,
            pinceValue BOOLEAN NOT NULL,
            robot_id TEXT NOT NULL
        )
    """)

    # Création de la tlabe robots pour enregistrer les robots
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ROBOTS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            robot_id TEXT NOT NULL,
            alias TEXT
        )
    """)

    # Initialisatio n des uuid des robots des autres équipes
    uuidMrKrabs = "53d67923-704f-4b97-b6d4-64a0a04ca5de"
    uuidMrKrabsSimu = "54d67923-704f-4b97-b6d4-64a0a04ca5de"
    uuidMaxenceLaFourmis = "72a1834d-98ef-4b46-87f5-5e4c4e82e39a"
    uuidGhostEyes = "24dcc3a8-3de8-0000-0000-000000000000"
    uuidPathFinder = "255f30bc-46f7-41d4-ba1d-db76a0afd7f7"
    uuidRobotOSR = "efe16b56-45fa-47a3-8f05-04200828eea9"
    uuidPastaBot = "7f377006-cba5-5d50f-a058d-45c5ce970f10"

    # Ajout des alias et des uuid des robots dans la base de donnée
    cursor.execute("SELECT COUNT(*) FROM ROBOTS")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO ROBOTS (robot_id, alias) VALUES (?, ?)
        """, [
            (uuidMrKrabs, "MrKrabs"),
            (uuidMrKrabsSimu, "MrKrabsSimu"),
            (uuidMaxenceLaFourmis, "MaxenceLaFourmis"),
            (uuidGhostEyes, "GhostEyes"),
            (uuidPathFinder, "PathFinder"),
            (uuidRobotOSR, "RobotOSR"),
            (uuidPastaBot, "PastaBot"),
        ])


    conn.commit()
    conn.close()

# Fonction pour ce connecter a la base de donénes
def connectToDb():
    DB_NAME = os.getenv("DB_NAME")
    return sqlite3.connect(DB_NAME)
