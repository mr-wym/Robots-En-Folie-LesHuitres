import sqlite3
import os
from dotenv import load_dotenv
from uuid import uuid4

def init_db():
    load_dotenv()
    conn = connectToDb()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS MISSION (
        id INTEGER PRIMARY KEY,
            datetime TEXT NOT NULL,
            mission TEXT NOT NULL,
            robot_id TEXT NOT NULL,
            isDone BOOLEAN DEFAULT FALSE
        )
    """)
            # id INTEGER PRIMARY KEY AUTOINCREMENT,

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


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ROBOTS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            robot_id TEXT NOT NULL,
            alias TEXT
        )
    """)

    # cursor.execute("SELECT COUNT(*) FROM MISSION")
    # if cursor.fetchone()[0] == 0:
    #     cursor.executemany("""
    #         INSERT INTO MISSION (datetime, mission, robot_id) VALUES (?, ?, ?)
    #     """, [
    #         ("2025-06-01 10:00:00", ["2", "2"], "AA:BB:CC:DD:EE:FF"),
    #         ("2025-06-01 10:01:00", ["2", "6"], "AA:BB:CC:DD:EE:FF"),
    #         ("2025-06-01 10:02:00", ["2", "5"], "AA:BB:CC:DD:EE:FF"),
    #     ])

    # cursor.execute("SELECT COUNT(*) FROM TELEMETRY")
    # if cursor.fetchone()[0] == 0:
    #     cursor.executemany("""
    #         INSERT INTO TELEMETRY (vitesse, distance_ultrason, status_deplacement, ligne, pince_active, robot_id) VALUES (?, ?, ?, ?, ?, ?)
    #     """, [
    #         (1.5, 20.0, "moving", 1, True, "AA:BB:CC:DD:EE:FF"),
    #         (1.7, 18.5, "moving", 2, False, "AA:BB:CC:DD:EE:FF"),
    #         (0.0, 15.0, "stopped", 3, True, "AA:BB:CC:DD:EE:FF")
    #     ])

    # uuid = str(uuid4())
    uuidMrKrabs = "53d67923-704f-4b97-b6d4-64a0a04ca5de"
    uuidMrKrabsSimu = "54d67923-704f-4b97-b6d4-64a0a04ca5de"
    uuidMaxenceLaFourmis = "72a1834d-98ef-4b46-87f5-5e4c4e82e39a"
    uuidGhostEyes = "24dcc3a8-3de8-0000-0000-000000000000"
    uuidPathFinder = "255f30bc-46f7-41d4-ba1d-db76a0afd7f7"
    uuidRobotOSR = "efe16b56-45fa-47a3-8f05-04200828eea9"
    uuidPastaBot = "7f377006-cba5-5d50f-a058d-45c5ce970f10"

    print(f"UUID generated: {uuidMrKrabs}")
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

def connectToDb():
    DB_NAME = os.getenv("DB_NAME")
    return sqlite3.connect(DB_NAME)
