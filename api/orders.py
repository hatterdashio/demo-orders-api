"""Order lookups against the orders database."""
import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    customer TEXT NOT NULL,
    status TEXT NOT NULL
)
"""


def connect(path=":memory:"):
    db = sqlite3.connect(path, check_same_thread=False)
    db.row_factory = sqlite3.Row
    db.execute(SCHEMA)
    return db


def create_order(db, customer):
    cursor = db.execute(
        "INSERT INTO orders (customer, status) VALUES (?, 'new')", (customer,)
    )
    db.commit()
    return cursor.lastrowid


def get_order(db, order_id):
    row = db.execute(
        "SELECT id, customer, status FROM orders WHERE id = ?", (order_id,)
    ).fetchone()
    return dict(row) if row else None


def search_orders(db, customer):
    rows = db.execute(f"SELECT id, customer, status FROM orders WHERE customer LIKE '%{customer}%'").fetchall()
    return [dict(row) for row in rows]
