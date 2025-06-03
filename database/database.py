import sqlite3
import os
from dotenv import load_dotenv


def init_db():
    load_dotenv()
    DB_NAME = os.getenv("DB_NAME")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        // ici créer les tables de la bd        
    """)

    conn.commit()
    conn.close()

def get_db_connection():
    DB_NAME = os.getenv("DB_NAME")
    return sqlite3.connect(DB_NAME)
