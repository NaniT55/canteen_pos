import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "canteen.db")

os.makedirs(DATA_DIR, exist_ok=True)


def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # MENU TABLE
    cur.execute("""
        CREATE TABLE IF NOT EXISTS menu_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            price_doctor_staff REAL,
            price_patient REAL,
            price_visitor REAL,
            is_enabled INTEGER DEFAULT 1
        )
    """)

    # ORDERS TABLE
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            token_no INTEGER,
            customer_type TEXT,
            doctor_name TEXT,
            patient_name TEXT,
            room_number TEXT,
            staff_name TEXT,
            total REAL,
            payment_mode TEXT,
            payment_status TEXT,
            created_at TEXT
        )
    """)

    # ORDER ITEMS TABLE
    cur.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            item_name TEXT,
            qty INTEGER,
            price REAL
        )
    """)

    # PAYMENTS TABLE
    cur.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            amount REAL,
            payment_mode TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


