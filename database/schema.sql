-- =========================
-- MENU ITEMS
-- =========================
CREATE TABLE IF NOT EXISTS menu_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,

    price_doctor_staff REAL,
    price_patient REAL,
    price_visitor REAL,

    stock INTEGER DEFAULT 0,
    is_enabled INTEGER DEFAULT 1
);

-- =========================
-- ORDERS
-- =========================
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    token_no INTEGER,
    customer_type TEXT,

    doctor_name TEXT,
    patient_name TEXT,
    room_number TEXT,
    staff_name TEXT,

    total REAL,

    payment_mode TEXT,      -- Cash / UPI / Unpaid
    payment_status TEXT,    -- PAID / UNPAID

    created_at TEXT
);

-- =========================
-- ORDER ITEMS
-- =========================
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    item_name TEXT,
    qty INTEGER,
    price REAL
);

-- =========================
-- INVENTORY LOGS
-- =========================
CREATE TABLE IF NOT EXISTS inventory_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT,
    change_qty INTEGER,
    reason TEXT,
    created_at TEXT
);


CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    amount REAL,
    payment_mode TEXT,       -- Cash / UPI
    paid_at TEXT
);