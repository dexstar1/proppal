import sqlite3
from datetime import datetime
from typing import List, Tuple

DB_PATH = 'proppal.db'


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_referrals_schema():
    """Ensure users table has referral-related columns."""
    conn = _connect()
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(users)")
    cols = {row[1] for row in cur.fetchall()}
    alters = []
    if 'referral_code' not in cols:
        alters.append("ALTER TABLE users ADD COLUMN referral_code TEXT")
    if 'referred_by' not in cols:
        alters.append("ALTER TABLE users ADD COLUMN referred_by INTEGER")
    if 'referred_at' not in cols:
        alters.append("ALTER TABLE users ADD COLUMN referred_at TEXT")
    if 'created_at' not in cols:
        alters.append("ALTER TABLE users ADD COLUMN created_at TEXT")
    for stmt in alters:
        try:
            cur.execute(stmt)
        except Exception:
            pass
    if alters:
        conn.commit()
    conn.close()


def get_or_create_referral_code(user_id: int) -> str:
    ensure_referrals_schema()
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT referral_code FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    code = row["referral_code"] if row else None
    if code and str(code).strip():
        conn.close()
        return code
    # Deterministic code based on user id
    code = f"RP{int(user_id):06d}"
    try:
        cur.execute("UPDATE users SET referral_code = ?, created_at = COALESCE(created_at, ?) WHERE id = ?", (code, datetime.now().isoformat(), user_id))
        conn.commit()
    finally:
        conn.close()
    return code


def set_referred_by(user_id: int, referral_code: str) -> bool:
    """Link a user to a referrer by referral code. Returns True if linked."""
    ensure_referrals_schema()
    if not referral_code or not str(referral_code).strip():
        return False
    code = referral_code.strip()
    conn = _connect()
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM users WHERE referral_code = ? AND role = 'realtor'", (code,))
        ref = cur.fetchone()
        if not ref:
            return False
        ref_id = int(ref["id"])
        if ref_id == int(user_id):
            return False
        # Only set if not already set
        cur.execute("UPDATE users SET referred_by = COALESCE(referred_by, ?), referred_at = COALESCE(referred_at, ?) WHERE id = ?",
                    (ref_id, datetime.now().isoformat(), user_id))
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()


def get_downlines(referrer_id: int) -> List[sqlite3.Row]:
    ensure_referrals_schema()
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT id, email, role, created_at, referred_at FROM users WHERE referred_by = ? ORDER BY referred_at DESC NULLS LAST", (referrer_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


def referrals_histogram_by_month(referrer_id: int) -> List[Tuple[str, int]]:
    """Return list of (YYYY-MM, count) for downline referrals."""
    ensure_referrals_schema()
    conn = _connect()
    cur = conn.cursor()
    # Use referred_at if present, else created_at
    cur.execute(
        """
        SELECT substr(COALESCE(referred_at, created_at), 1, 7) AS ym, COUNT(*) as cnt
        FROM users
        WHERE referred_by = ? AND COALESCE(referred_at, created_at) IS NOT NULL
        GROUP BY ym
        ORDER BY ym ASC
        """,
        (referrer_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return [(r["ym"], int(r["cnt"])) for r in rows]
