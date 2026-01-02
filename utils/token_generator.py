from database.db import get_connection

def generate_token():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT MAX(token_no) FROM orders")
    last = cur.fetchone()[0]
    conn.close()
    return 1 if last is None else last + 1
