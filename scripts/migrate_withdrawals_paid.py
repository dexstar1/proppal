import os
import sqlite3
import sys


def main():
    # Resolve DB path relative to repo root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    db_path = os.path.join(repo_root, 'proppal.db')

    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        sys.exit(1)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Ensure table exists
    cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='withdrawal_requests'")
    if cur.fetchone()[0] == 0:
        print("No withdrawal_requests table found. Nothing to migrate.")
        conn.close()
        return

    # Count before
    cur.execute("SELECT COUNT(*) FROM withdrawal_requests WHERE status='approved'")
    before = cur.fetchone()[0]

    # Update
    cur.execute("UPDATE withdrawal_requests SET status='paid' WHERE status='approved'")
    updated = cur.rowcount
    conn.commit()

    # Count after
    cur.execute("SELECT COUNT(*) FROM withdrawal_requests WHERE status='paid'")
    after = cur.fetchone()[0]

    conn.close()
    print(f"approved_before={before} updated={updated} paid_after={after}")


if __name__ == '__main__':
    main()
