import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "canteen.db")

# Ensure data directory exists (cloud-safe)
os.makedirs(DATA_DIR, exist_ok=True)

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

