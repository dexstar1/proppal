import sqlite3
import os
from dotenv import load_dotenv


DB_PATH = os.getenv('DB_PATH', "guestbook.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL,
            size TEXT NOT NULL, -- Comma-separated sizes
            featured_image TEXT NOT NULL,
            gallery_image TEXT NOT NULL,
            date_added TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()



def get_products():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, description, price, size, featured_image, gallery_image, date_added
        FROM products
        ORDER BY id DESC
    """)
    products = cursor.fetchall()
    conn.close()
    return products

def add_product(name, description, price, size, featured_image, gallery_image, date_added):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO products (name, description, price, size, featured_image, gallery_image, date_added)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, description, price, size, featured_image, gallery_image, date_added ))
    conn.commit()
    conn.close()

def update_product(product_id, name, description, price, size, featured_image, gallery_image):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE products
        SET name = ?, description = ?, price = ?, size = ?, featured_image = ?, gallery_image = ?
        WHERE id = ?
    """, (name, description, price, size, featured_image, gallery_image, product_id))
    conn.commit()
    conn.close()

def delete_message(product_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()