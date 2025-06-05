import sqlite3
import os
from dotenv import load_dotenv


def init_db():
    load_dotenv()
    conn = connectToDb()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS COMMANDE (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT NOT NULL,
            commande TEXT NOT NULL,
            macAddress TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS TELEMETRIE (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            speed FLOAT NOT NULL,
            distance FLOAT NOT NULL,
            timestamp TEXT NOT NULL,
            pincevalue BOOLEAN NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ROBOTS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            macaddress TEXT NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM COMMANDE")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO COMMANDE (datetime, commande, macAddress) VALUES (?, ?, ?)
        """, [
            ("2025-06-01 10:00:00", "START", "AA:BB:CC:DD:EE:FF"),
            ("2025-06-01 10:01:00", "MOVE_FORWARD", "AA:BB:CC:DD:EE:FF"),
            ("2025-06-01 10:02:00", "STOP", "AA:BB:CC:DD:EE:FF"),
        ])

    cursor.execute("SELECT COUNT(*) FROM TELEMETRIE")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("""
            INSERT INTO TELEMETRIE (speed, distance, timestamp, pincevalue) VALUES (?, ?, ?, ?)
        """, [
            (1.5, 20.0, "2025-06-01 10:00:01", True),
            (1.7, 18.5, "2025-06-01 10:00:02", False),
            (0.0, 15.0, "2025-06-01 10:00:03", True)
        ])

    cursor.execute("SELECT COUNT(*) FROM ROBOTS")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO ROBOTS (macaddress) VALUES (?)
        """, ("AA:BB:CC:DD:EE:FF",))

        cursor.execute("""
            INSERT INTO ROBOTS (macaddress) VALUES (?)
        """, ("AA:BB:CCsdfsdf:DD:EE:FF",))

        cursor.execute("""
            INSERT INTO ROBOTS (macaddress) VALUES (?)
        """, ("AA:BB:CC:DD:EEsdfsd:FF",))


    conn.commit()
    conn.close()

def connectToDb():
    DB_NAME = os.getenv("DB_NAME")
    return sqlite3.connect(DB_NAME)
