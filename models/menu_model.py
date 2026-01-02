from database.db import get_connection

def normalize_category(category):
    return "Drinks" if category == "Cool Drinks" else category

def get_menu(only_enabled=True):
    conn = get_connection()
    cur = conn.cursor()

    if only_enabled:
        cur.execute("""
            SELECT id, name, category,
                   price_doctor_staff, price_patient, price_visitor,
                   stock, is_enabled
            FROM menu_items
            WHERE is_enabled = 1
            ORDER BY category, name
        """)
    else:
        cur.execute("""
            SELECT id, name, category,
                   price_doctor_staff, price_patient, price_visitor,
                   stock, is_enabled
            FROM menu_items
            ORDER BY category, name
        """)

    data = cur.fetchall()
    conn.close()
    return data


def add_menu_item(name, category, p_ds, p_patient, p_visitor):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO menu_items
        (name, category, price_doctor_staff, price_patient, price_visitor, stock)
        VALUES (?, ?, ?, ?, ?, 0)
    """, (name, category, p_ds, p_patient, p_visitor))

    conn.commit()
    conn.close()

def update_menu_item(item_id, name, category, p_ds, p_patient, p_visitor):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE menu_items
        SET name = ?,
            category = ?,
            price_doctor_staff = ?,
            price_patient = ?,
            price_visitor = ?
        WHERE id = ?
    """, (name, category, p_ds, p_patient, p_visitor, item_id))

    conn.commit()
    conn.close()


def delete_menu_item(item_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM menu_items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

def toggle_item_status(item_id, enabled):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE menu_items
        SET is_enabled = ?
        WHERE id = ?
    """, (1 if enabled else 0, item_id))

    conn.commit()
    conn.close()

