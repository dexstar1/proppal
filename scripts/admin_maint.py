import os
import sqlite3
import base64

DB_PATH = 'proppal.db'
IMG_DIR = os.path.join('public', 'assets', 'img', 'properties')
IMG_PATH = os.path.join(IMG_DIR, 'placeholder.png')
IMG_URL = '/assets/img/properties/placeholder.png'

# 1x1 transparent PNG
PLACEHOLDER_BASE64 = (
    'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4nGNgYGD4DwABBAEAU7ZciwAAAABJRU5ErkJggg=='
)

def ensure_placeholder_image():
    os.makedirs(IMG_DIR, exist_ok=True)
    if not os.path.exists(IMG_PATH):
        with open(IMG_PATH, 'wb') as f:
            f.write(base64.b64decode(PLACEHOLDER_BASE64))
        print(f"Created placeholder image at {IMG_PATH}")
    else:
        print(f"Placeholder image already exists at {IMG_PATH}")

def cleanup_and_update_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Delete non-admin properties
    cur.execute("DELETE FROM properties WHERE realtor_id NOT IN (SELECT id FROM users WHERE role = 'admin')")
    deleted = cur.rowcount

    # Force all admin properties to use placeholder image
    cur.execute("UPDATE properties SET images = ? WHERE realtor_id IN (SELECT id FROM users WHERE role = 'admin')", (IMG_URL,))
    updated = cur.rowcount

    conn.commit()
    conn.close()

    print(f"Deleted non-admin properties: {deleted}")
    print(f"Updated admin properties with placeholder images: {updated}")

if __name__ == '__main__':
    ensure_placeholder_image()
    cleanup_and_update_db()
