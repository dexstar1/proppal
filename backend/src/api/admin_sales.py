import sqlite3
from datetime import datetime
from typing import List, Optional, Dict, Any
from backend.src.api.notifications import create_notification, ensure_notifications_schema

DB_PATH = 'proppal.db'


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _ensure_property_sales_columns():
    """Ensure approval-related columns exist on property_sales."""
    conn = _connect()
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(property_sales)")
    cols = {row[1] for row in cur.fetchall()}

    to_add = []
    if 'approved_by' not in cols:
        to_add.append("ALTER TABLE property_sales ADD COLUMN approved_by INTEGER")
    if 'approved_at' not in cols:
        to_add.append("ALTER TABLE property_sales ADD COLUMN approved_at TEXT")
    if 'rejected_at' not in cols:
        to_add.append("ALTER TABLE property_sales ADD COLUMN rejected_at TEXT")
    if 'reject_reason' not in cols:
        to_add.append("ALTER TABLE property_sales ADD COLUMN reject_reason TEXT")

    for stmt in to_add:
        cur.execute(stmt)
    if to_add:
        conn.commit()
    conn.close()


def _ensure_commission_payouts_table():
    """Create commission_payouts table if it doesn't exist and ensure columns exist."""
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS commission_payouts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER NOT NULL,
            realtor_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            commission_rate REAL, -- fraction e.g. 0.1
            method TEXT,         -- e.g. bank_transfer, paypal
            reference TEXT,      -- external reference/txn id
            metadata TEXT,       -- JSON string for extra data
            notes TEXT,          -- optional notes
            status TEXT NOT NULL DEFAULT 'pending', -- pending, paid, failed
            payout_type TEXT DEFAULT 'primary', -- 'primary' or 'upline'
            created_at TEXT NOT NULL,
            paid_at TEXT,
            processed_by INTEGER,
            FOREIGN KEY(sale_id) REFERENCES property_sales(id)
        )
        """
    )
    # Ensure new columns exist for older DBs
    cur.execute("PRAGMA table_info(commission_payouts)")
    cols = {row[1] for row in cur.fetchall()}
    alters = []
    if 'commission_rate' not in cols:
        alters.append("ALTER TABLE commission_payouts ADD COLUMN commission_rate REAL")
    if 'method' not in cols:
        alters.append("ALTER TABLE commission_payouts ADD COLUMN method TEXT")
    if 'reference' not in cols:
        alters.append("ALTER TABLE commission_payouts ADD COLUMN reference TEXT")
    if 'metadata' not in cols:
        alters.append("ALTER TABLE commission_payouts ADD COLUMN metadata TEXT")
    if 'notes' not in cols:
        alters.append("ALTER TABLE commission_payouts ADD COLUMN notes TEXT")
    if 'payout_type' not in cols:
        alters.append("ALTER TABLE commission_payouts ADD COLUMN payout_type TEXT DEFAULT 'primary'")
    for stmt in alters:
        cur.execute(stmt)
    if alters:
        conn.commit()
    conn.commit()
    conn.close()


def ensure_admin_sales_schema():
    _ensure_property_sales_columns()
    _ensure_commission_payouts_table()


# Queries

def get_all_sales() -> List[sqlite3.Row]:
    ensure_admin_sales_schema()
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT ps.*, p.name as property_name, u.email as realtor_email
        FROM property_sales ps
        LEFT JOIN properties p ON ps.property_id = p.id
        LEFT JOIN users u ON ps.realtor_id = u.id
        ORDER BY ps.created_at DESC
        """
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def get_sale_by_id(sale_id: int) -> Optional[sqlite3.Row]:
    ensure_admin_sales_schema()
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT ps.*, p.name as property_name, u.email as realtor_email
        FROM property_sales ps
        LEFT JOIN properties p ON ps.property_id = p.id
        LEFT JOIN users u ON ps.realtor_id = u.id
        WHERE ps.id = ?
        """,
        (sale_id,),
    )
    row = cur.fetchone()
    conn.close()
    return row


def approve_sale_and_create_payout(sale_id: int, admin_id: int, commission_rate: float) -> Dict[str, Any]:
    """Approve a pending sale and create a commission payout record.
    commission_rate is a fraction (e.g., 0.1 for 10%).
    Returns {updated: bool, payout_id: Optional[int]}.
    """
    ensure_admin_sales_schema()
    now = datetime.now().isoformat()

    conn = _connect()
    cur = conn.cursor()

    # Fetch sale
    cur.execute("SELECT * FROM property_sales WHERE id = ?", (sale_id,))
    sale = cur.fetchone()
    if not sale:
        conn.close()
        return {"updated": False, "payout_id": None, "error": "Sale not found"}

    if sale["status"] == "approved":
        # Idempotent: still ensure payout exists or create if missing
        cur.execute(
            "SELECT id FROM commission_payouts WHERE sale_id = ? AND payout_type = 'primary'",
            (sale_id,),
        )
        existing = cur.fetchone()
        if existing:
            # Ensure upline payout exists too
            try:
                cur.execute("SELECT referred_by FROM users WHERE id = ?", (sale["realtor_id"],))
                urow = cur.fetchone()
                referrer_id = int(urow["referred_by"]) if urow and urow["referred_by"] is not None else None
                if referrer_id and referrer_id != int(sale["realtor_id"]):
                    cur.execute("SELECT id FROM commission_payouts WHERE sale_id = ? AND payout_type = 'upline'", (sale_id,))
                    up = cur.fetchone()
                    if not up:
                        upline_amount = round(float(sale["amount"] or 0) * 0.05, 2)
                        cur.execute(
                            """
                            INSERT INTO commission_payouts (sale_id, realtor_id, amount, commission_rate, status, payout_type, created_at)
                            VALUES (?, ?, ?, ?, 'pending', 'upline', ?)
                            """,
                            (sale_id, referrer_id, upline_amount, 0.05, now),
                        )
                        conn.commit()
            except Exception:
                pass
            conn.close()
            return {"updated": True, "payout_id": existing["id"]}

    amount = float(sale["amount"]) if sale["amount"] is not None else 0.0
    commission_amount = round(amount * commission_rate, 2)

    # Approve sale
    cur.execute(
        """
        UPDATE property_sales
        SET status = 'approved', approved_by = ?, approved_at = ?, updated_at = ?
        WHERE id = ?
        """,
        (admin_id, now, now, sale_id),
    )

    # Create primary payout (pending)
    cur.execute(
        """
        INSERT INTO commission_payouts (sale_id, realtor_id, amount, commission_rate, status, payout_type, created_at)
        VALUES (?, ?, ?, ?, 'pending', 'primary', ?)
        """,
        (sale_id, sale["realtor_id"], commission_amount, commission_rate, now),
    )
    payout_id = cur.lastrowid

    # Create upline payout (5%) if referred
    try:
        cur.execute("SELECT referred_by FROM users WHERE id = ?", (sale["realtor_id"],))
        urow = cur.fetchone()
        referrer_id = int(urow["referred_by"]) if urow and urow["referred_by"] is not None else None
        if referrer_id and referrer_id != int(sale["realtor_id"]):
            cur.execute("SELECT id FROM commission_payouts WHERE sale_id = ? AND payout_type = 'upline'", (sale_id,))
            exist_upline = cur.fetchone()
            if not exist_upline:
                upline_amount = round(amount * 0.05, 2)
                cur.execute(
                    """
                    INSERT INTO commission_payouts (sale_id, realtor_id, amount, commission_rate, status, payout_type, created_at)
                    VALUES (?, ?, ?, ?, 'pending', 'upline', ?)
                    """,
                    (sale_id, referrer_id, upline_amount, 0.05, now),
                )
    except Exception:
        pass

    conn.commit()
    conn.close()

    # Notify realtor about approval and payout
    try:
        ensure_notifications_schema()
        title = "Sale Approved"
        msg = f"Your sale #{sale_id} has been approved. Commission: ₦{commission_amount:,.2f} at {commission_rate*100:.2f}%"
        link = f"/realtor/sales/{sale_id}"
        create_notification(int(sale["realtor_id"]), title, msg, type="sale_approved", related_sale_id=sale_id, link=link)
    except Exception:
        pass

    return {"updated": True, "payout_id": payout_id}


def reject_sale(sale_id: int, admin_id: int, reason: Optional[str] = None) -> bool:
    ensure_admin_sales_schema()
    now = datetime.now().isoformat()
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE property_sales
        SET status = 'rejected', approved_by = ?, rejected_at = ?, updated_at = ?, reject_reason = ?
        WHERE id = ?
        """,
        (admin_id, now, now, reason, sale_id),
    )
    conn.commit()
    changed = cur.rowcount > 0
    conn.close()

    # Notify realtor about rejection
    if changed:
        try:
            sale = get_sale_by_id(sale_id)
            if sale:
                ensure_notifications_schema()
                title = "Sale Rejected"
                reason_text = f" Reason: {reason}" if reason else ""
                msg = f"Your sale #{sale_id} was rejected.{reason_text}"
                link = f"/realtor/sales/{sale_id}"
                create_notification(int(sale["realtor_id"]), title, msg, type="sale_rejected", related_sale_id=sale_id, link=link)
        except Exception:
            pass

    return changed


def get_payouts() -> List[sqlite3.Row]:
    ensure_admin_sales_schema()
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT cp.*, u.email as realtor_email, ps.amount as sale_amount, p.name as property_name
        FROM commission_payouts cp
        LEFT JOIN property_sales ps ON cp.sale_id = ps.id
        LEFT JOIN users u ON cp.realtor_id = u.id
        LEFT JOIN properties p ON ps.property_id = p.id
        ORDER BY cp.created_at DESC
        """
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def get_commissions_by_realtor(realtor_id: int) -> List[sqlite3.Row]:
    ensure_admin_sales_schema()
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT cp.*, ps.amount as sale_amount, p.name as property_name
        FROM commission_payouts cp
        LEFT JOIN property_sales ps ON cp.sale_id = ps.id
        LEFT JOIN properties p ON ps.property_id = p.id
        WHERE cp.realtor_id = ?
        ORDER BY cp.created_at DESC
        """,
        (realtor_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def approve_commission(commission_id: int, admin_id: int) -> bool:
    """Approve a commission payout; credit realtor wallet and mark status approved."""
    ensure_admin_sales_schema()
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT realtor_id, amount, status FROM commission_payouts WHERE id = ?", (commission_id,))
    row = cur.fetchone()
    if not row or row["status"] != 'pending':
        conn.close()
        return False
    now = datetime.now().isoformat()
    cur.execute(
        "UPDATE commission_payouts SET status = 'approved', paid_at = ?, processed_by = ? WHERE id = ?",
        (now, admin_id, commission_id),
    )
    conn.commit()
    conn.close()
    # Credit wallet and notify
    try:
        from backend.src.api.wallets import credit_wallet, ensure_wallets_schema
        from backend.src.api.notifications import create_notification, ensure_notifications_schema
        ensure_wallets_schema(); ensure_notifications_schema()
        credit_wallet(int(row['realtor_id']), float(row['amount']))
        create_notification(int(row['realtor_id']), 'Commission Approved', f"Your commission (₦{float(row['amount']):,.2f}) has been approved.", type='commission_approved')
    except Exception:
        pass
    return True


def reject_commission(commission_id: int, admin_id: int) -> bool:
    ensure_admin_sales_schema()
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT realtor_id, status FROM commission_payouts WHERE id = ?", (commission_id,))
    row = cur.fetchone()
    if not row or row["status"] != 'pending':
        conn.close()
        return False
    now = datetime.now().isoformat()
    cur.execute(
        "UPDATE commission_payouts SET status = 'rejected', paid_at = ?, processed_by = ? WHERE id = ?",
        (now, admin_id, commission_id),
    )
    conn.commit()
    conn.close()
    try:
        from backend.src.api.notifications import create_notification, ensure_notifications_schema
        ensure_notifications_schema()
        create_notification(int(row['realtor_id']), 'Commission Rejected', 'Your commission has been rejected.', type='commission_rejected')
    except Exception:
        pass
    return True


essential_payout_statuses = {"pending", "paid", "failed"}


def get_pending_sales_count() -> int:
    ensure_admin_sales_schema()
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS cnt FROM property_sales WHERE status = 'pending'")
    row = cur.fetchone()
    conn.close()
    return int(row[0]) if row else 0


def get_pending_payouts_count() -> int:
    ensure_admin_sales_schema()
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS cnt FROM commission_payouts WHERE status = 'pending'")
    row = cur.fetchone()
    conn.close()
    return int(row[0]) if row else 0


def mark_payout_paid(payout_id: int, admin_id: int, method: Optional[str] = None, reference: Optional[str] = None, notes: Optional[str] = None, metadata: Optional[str] = None) -> bool:
    ensure_admin_sales_schema()
    now = datetime.now().isoformat()
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE commission_payouts
        SET status = 'paid', paid_at = ?, processed_by = ?, method = COALESCE(?, method), reference = COALESCE(?, reference), notes = COALESCE(?, notes), metadata = COALESCE(?, metadata)
        WHERE id = ? AND status = 'pending'
        """,
        (now, admin_id, method, reference, notes, metadata, payout_id),
    )
    conn.commit()
    changed = cur.rowcount > 0
    conn.close()

    # Notify payout paid
    if changed:
        try:
            ensure_notifications_schema()
            conn2 = _connect()
            cur2 = conn2.cursor()
            cur2.execute("SELECT sale_id, realtor_id, amount FROM commission_payouts WHERE id = ?", (payout_id,))
            row = cur2.fetchone()
            conn2.close()
            if row:
                # Credit realtor wallet
                try:
                    from backend.src.api.wallets import credit_wallet, ensure_wallets_schema
                    ensure_wallets_schema()
                    credit_wallet(int(row['realtor_id']), float(row['amount']))
                except Exception:
                    pass
                # Notify
                title = "Payout Completed"
                msg = f"Your commission payout for sale #{row['sale_id']} (₦{float(row['amount']):,.2f}) has been marked as paid."
                link = "/realtor/withdraw"
                create_notification(int(row["realtor_id"]), title, msg, type="payout_paid", related_sale_id=int(row['sale_id']), link=link)
        except Exception:
            pass

    return changed
