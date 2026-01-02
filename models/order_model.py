from database.db import get_connection
from datetime import datetime

def save_order(
    token,
    customer,
    total,
    payment_mode,
    payment_status,
    doctor_name=None,
    patient_name=None,
    room_number=None,
    staff_name=None
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO orders (
            token_no, customer_type,
            doctor_name, patient_name, room_number, staff_name,
            total, payment_mode, payment_status, created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        token, customer,
        doctor_name, patient_name, room_number, staff_name,
        total, payment_mode, payment_status,
        datetime.now().isoformat()
    ))

    order_id = cur.lastrowid
    conn.commit()
    conn.close()
    return order_id

def save_order_items(order_id, cart):
    conn = get_connection()
    cur = conn.cursor()
    for item, qty, price in cart:
        cur.execute("""
            INSERT INTO order_items VALUES (NULL, ?, ?, ?, ?)
        """, (order_id, item, qty, price))
    conn.commit()
    conn.close()

from database.db import get_connection

def mark_orders_paid(order_ids, payment_mode):
    """
    Marks given order IDs as PAID and updates payment mode
    """

    if not order_ids:
        return

    conn = get_connection()
    cur = conn.cursor()

    placeholders = ",".join(["?"] * len(order_ids))

    cur.execute(
        f"""
        UPDATE orders
        SET payment_status = 'PAID',
            payment_mode = ?
        WHERE id IN ({placeholders})
        """,
        [payment_mode] + order_ids
    )

    conn.commit()
    conn.close()


def add_payment(order_id, amount, payment_mode):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO payments (order_id, amount, payment_mode, paid_at)
        VALUES (?, ?, ?, ?)
    """, (order_id, amount, payment_mode, datetime.now().isoformat()))

    conn.commit()
    conn.close()


def get_paid_amount(order_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM payments
        WHERE order_id = ?
    """, (order_id,))

    paid = cur.fetchone()[0]
    conn.close()
    return paid


def finalize_order_if_paid(order_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT total FROM orders WHERE id = ?", (order_id,))
    total = cur.fetchone()[0]

    cur.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM payments
        WHERE order_id = ?
    """, (order_id,))
    paid = cur.fetchone()[0]

    if paid >= total:
        cur.execute("""
            UPDATE orders
            SET payment_status = 'PAID'
            WHERE id = ?
        """, (order_id,))

    conn.commit()
    conn.close()
