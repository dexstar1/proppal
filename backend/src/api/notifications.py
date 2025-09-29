import sqlite3
from datetime import datetime
from typing import List, Optional

DB_PATH = 'proppal.db'


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def ensure_notifications_schema():
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            type TEXT,
            related_sale_id INTEGER,
            link TEXT,
            created_at TEXT NOT NULL,
            is_read INTEGER NOT NULL DEFAULT 0
        )
        """
    )
    conn.commit()
    conn.close()


def create_notification(user_id: int, title: str, message: str, type: Optional[str] = None, related_sale_id: Optional[int] = None, link: Optional[str] = None) -> int:
    ensure_notifications_schema()
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO notifications (user_id, title, message, type, related_sale_id, link, created_at, is_read)
        VALUES (?, ?, ?, ?, ?, ?, ?, 0)
        """,
        (user_id, title, message, type, related_sale_id, link, datetime.now().isoformat()),
    )
    nid = cur.lastrowid
    conn.commit()
    conn.close()
    return nid


def get_notifications_for_user(user_id: int, unread_only: bool = False) -> List[sqlite3.Row]:
    ensure_notifications_schema()
    conn = _connect()
    cur = conn.cursor()
    if unread_only:
        cur.execute(
            """
            SELECT * FROM notifications
            WHERE user_id = ? AND is_read = 0
            ORDER BY created_at DESC
            """,
            (user_id,),
        )
    else:
        cur.execute(
            """
            SELECT * FROM notifications
            WHERE user_id = ?
            ORDER BY created_at DESC
            """,
            (user_id,),
        )
    rows = cur.fetchall()
    conn.close()
    return rows


def mark_notification_read(notification_id: int, user_id: int) -> bool:
    ensure_notifications_schema()
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE notifications SET is_read = 1
        WHERE id = ? AND user_id = ?
        """,
        (notification_id, user_id),
    )
    conn.commit()
    changed = cur.rowcount > 0
    conn.close()
    return changed


def mark_all_notifications_read(user_id: int) -> int:
    ensure_notifications_schema()
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE notifications SET is_read = 1
        WHERE user_id = ? AND is_read = 0
        """,
        (user_id,),
    )
    conn.commit()
    count = cur.rowcount
    conn.close()
    return count


def get_unread_count_for_user(user_id: int) -> int:
    ensure_notifications_schema()
    conn = _connect()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT COUNT(*) AS cnt FROM notifications WHERE user_id = ? AND is_read = 0
        """,
        (user_id,),
    )
    row = cur.fetchone()
    conn.close()
    return int(row[0]) if row else 0
