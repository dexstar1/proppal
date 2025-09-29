import sqlite3
from datetime import datetime
from typing import Optional, List

DB_PATH = 'proppal.db'


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_wallets_schema():
    """Create wallets and withdrawal_requests tables if they don't exist."""
    conn = _connect()
    cur = conn.cursor()

    # Wallets table: one row per realtor
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS wallets (
            realtor_id INTEGER PRIMARY KEY,
            balance REAL NOT NULL DEFAULT 0,
            updated_at TEXT
        )
        """
    )

    # Withdrawal requests table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS withdrawal_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            realtor_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            method TEXT,
            account TEXT,
            notes TEXT,
            status TEXT NOT NULL DEFAULT 'pending', -- pending, approved, rejected
            created_at TEXT NOT NULL,
            decided_at TEXT,
            processed_by INTEGER
        )
        """
    )

    conn.commit()
    conn.close()


def _get_or_create_wallet(realtor_id: int) -> float:
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT balance FROM wallets WHERE realtor_id = ?", (realtor_id,))
    row = cur.fetchone()

    if row is None:
        cur.execute(
            "INSERT INTO wallets (realtor_id, balance, updated_at) VALUES (?, 0, ?)",
            (realtor_id, datetime.now().isoformat()),
        )
        conn.commit()
        balance = 0.0
    else:
        balance = float(row["balance"]) if row["balance"] is not None else 0.0

    conn.close()
    return balance


def get_wallet_balance(realtor_id: int) -> float:
    ensure_wallets_schema()
    return _get_or_create_wallet(realtor_id)


def credit_wallet(realtor_id: int, amount: float) -> None:
    ensure_wallets_schema()
    conn = _connect()
    cur = conn.cursor()
    # Ensure exists
    _ = _get_or_create_wallet(realtor_id)
    # Credit
    cur.execute(
        "UPDATE wallets SET balance = COALESCE(balance, 0) + ?, updated_at = ? WHERE realtor_id = ?",
        (amount, datetime.now().isoformat(), realtor_id),
    )
    conn.commit()
    conn.close()


def debit_wallet(realtor_id: int, amount: float) -> bool:
    ensure_wallets_schema()
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT balance FROM wallets WHERE realtor_id = ?", (realtor_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return False
    bal = float(row["balance"]) if row["balance"] is not None else 0.0
    if bal < amount:
        conn.close()
        return False
    cur.execute(
        "UPDATE wallets SET balance = balance - ?, updated_at = ? WHERE realtor_id = ?",
        (amount, datetime.now().isoformat(), realtor_id),
    )
    conn.commit()
    conn.close()
    return True


def create_withdraw_request(realtor_id: int, amount: float, method: Optional[str], account: Optional[str], notes: Optional[str]) -> int:
    ensure_wallets_schema()
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO withdrawal_requests (realtor_id, amount, method, account, notes, status, created_at)
        VALUES (?, ?, ?, ?, ?, 'pending', ?)
        """,
        (realtor_id, amount, method, account, notes, datetime.now().isoformat()),
    )
    req_id = cur.lastrowid
    conn.commit()
    conn.close()
    return req_id


def get_withdraw_requests() -> List[sqlite3.Row]:
    ensure_wallets_schema()
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT wr.*, u.email as realtor_email
        FROM withdrawal_requests wr
        LEFT JOIN users u ON wr.realtor_id = u.id
        ORDER BY wr.created_at DESC
        """
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def get_withdraw_requests_by_realtor(realtor_id: int) -> List[sqlite3.Row]:
    ensure_wallets_schema()
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM withdrawal_requests WHERE realtor_id = ? ORDER BY created_at DESC",
        (realtor_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def approve_withdraw_request(request_id: int, admin_id: int) -> bool:
    ensure_wallets_schema()
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT realtor_id, amount, status FROM withdrawal_requests WHERE id = ?", (request_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return False
    if row["status"] != 'pending':
        conn.close()
        return False
    realtor_id = int(row["realtor_id"]) if row["realtor_id"] is not None else None
    amount = float(row["amount"]) if row["amount"] is not None else 0.0

    # Check and debit wallet
    cur.execute("SELECT balance FROM wallets WHERE realtor_id = ?", (realtor_id,))
    wrow = cur.fetchone()
    bal = float(wrow["balance"]) if wrow and wrow["balance"] is not None else 0.0
    if bal < amount:
        conn.close()
        return False

    # Debit and mark approved
    cur.execute(
        "UPDATE wallets SET balance = balance - ?, updated_at = ? WHERE realtor_id = ?",
        (amount, datetime.now().isoformat(), realtor_id),
    )
    cur.execute(
        "UPDATE withdrawal_requests SET status = 'approved', decided_at = ?, processed_by = ? WHERE id = ?",
        (datetime.now().isoformat(), admin_id, request_id),
    )
    conn.commit()
    conn.close()
    return True


def reject_withdraw_request(request_id: int, admin_id: int) -> bool:
    ensure_wallets_schema()
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT status FROM withdrawal_requests WHERE id = ?", (request_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return False
    if row["status"] != 'pending':
        conn.close()
        return False
    cur.execute(
        "UPDATE withdrawal_requests SET status = 'rejected', decided_at = ?, processed_by = ? WHERE id = ?",
        (datetime.now().isoformat(), admin_id, request_id),
    )
    conn.commit()
    conn.close()
    return True
