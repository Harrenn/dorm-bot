import sqlite3
from contextlib import contextmanager

DB_PATH = 'dorm.db'

@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.commit()
        conn.close()

def init_db():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS renters(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                group_name TEXT,
                start_date TEXT,
                end_date TEXT
            )"""
        )
        cur.execute(
            """CREATE TABLE IF NOT EXISTS transactions(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                renter_id INTEGER,
                type TEXT,
                amount REAL,
                description TEXT,
                date TEXT,
                FOREIGN KEY(renter_id) REFERENCES renters(id)
            )"""
        )


def add_renter(name: str, group_name: str | None = None, start_date: str | None = None):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT OR IGNORE INTO renters(name, group_name, start_date) VALUES (?, ?, ?)",
            (name, group_name, start_date)
        )
        return cur.lastrowid


def record_transaction(renter_name: str, typ: str, amount: float, description: str, date: str):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM renters WHERE name = ?", (renter_name,))
        row = cur.fetchone()
        if not row:
            raise ValueError(f"Renter {renter_name} not found")
        renter_id = row[0]
        cur.execute(
            "INSERT INTO transactions(renter_id, type, amount, description, date) VALUES (?,?,?,?,?)",
            (renter_id, typ, amount, description, date)
        )
        return cur.lastrowid


def get_balance(renter_name: str):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM renters WHERE name = ?", (renter_name,))
        row = cur.fetchone()
        if not row:
            raise ValueError(f"Renter {renter_name} not found")
        renter_id = row[0]
        cur.execute(
            "SELECT SUM(amount) FROM transactions WHERE renter_id = ?", (renter_id,)
        )
        total = cur.fetchone()[0]
        return total or 0.0
