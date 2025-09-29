import sqlite3
from datetime import datetime
from typing import Optional

DB_PATH = 'proppal.db'


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_realtor_profile_schema():
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS realtor_profiles (
            realtor_id INTEGER PRIMARY KEY,
            gender TEXT,
            date_of_birth TEXT,
            address TEXT,
            profile_picture TEXT,
            bank_name TEXT,
            account_number TEXT,
            account_name TEXT,
            updated_at TEXT,
            created_at TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def get_realtor_profile(realtor_id: int) -> Optional[sqlite3.Row]:
    ensure_realtor_profile_schema()
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM realtor_profiles WHERE realtor_id = ?", (realtor_id,))
    row = cur.fetchone()
    conn.close()
    return row


def is_realtor_profile_complete(realtor_id: int) -> bool:
    row = get_realtor_profile(realtor_id)
    if not row:
        return False
    required = [row['gender'], row['date_of_birth'], row['address'], row['bank_name'], row['account_number'], row['account_name']]
    return all(bool(x and str(x).strip()) for x in required)


def upsert_realtor_profile(realtor_id: int, gender: Optional[str], date_of_birth: Optional[str], address: Optional[str], profile_picture: Optional[str], bank_name: Optional[str], account_number: Optional[str], account_name: Optional[str]) -> None:
    ensure_realtor_profile_schema()
    now = datetime.now().isoformat()
    conn = _connect()
    cur = conn.cursor()
    # Try update
    cur.execute(
        """
        UPDATE realtor_profiles SET gender = COALESCE(?, gender), date_of_birth = COALESCE(?, date_of_birth),
               address = COALESCE(?, address), profile_picture = COALESCE(?, profile_picture), bank_name = COALESCE(?, bank_name),
               account_number = COALESCE(?, account_number), account_name = COALESCE(?, account_name), updated_at = ?
        WHERE realtor_id = ?
        """,
        (gender, date_of_birth, address, profile_picture, bank_name, account_number, account_name, now, realtor_id),
    )
    if cur.rowcount == 0:
        cur.execute(
            """
            INSERT INTO realtor_profiles (realtor_id, gender, date_of_birth, address, profile_picture, bank_name, account_number, account_name, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (realtor_id, gender, date_of_birth, address, profile_picture, bank_name, account_number, account_name, now, now),
        )
    conn.commit()
    conn.close()
