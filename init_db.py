import sqlite3
from passlib.context import CryptContext

def init_db():
    conn = sqlite3.connect('proppal.db')
    cursor = conn.cursor()

    # Properties Table
    cursor.execute('DROP TABLE IF EXISTS properties')
    cursor.execute('''
    CREATE TABLE properties (
        id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, description TEXT NOT NULL, price REAL NOT NULL, images TEXT, realtor_id INTEGER, features TEXT, address TEXT, country TEXT, state TEXT, city TEXT, area TEXT, zip_code TEXT, latitude REAL, longitude REAL, virtual_tour_url TEXT, property_type TEXT, property_status TEXT, labels TEXT, video_url TEXT, bedrooms INTEGER, bathrooms INTEGER, rooms INTEGER, property_area_size REAL, property_land_size REAL, garages INTEGER, year_built INTEGER
    )
    ''')

    # Users Table
    cursor.execute('DROP TABLE IF EXISTS users')
    cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        hashed_password TEXT NOT NULL,
        role TEXT NOT NULL,
        is_verified BOOLEAN NOT NULL DEFAULT 0,
        verification_token TEXT,
        reset_token TEXT,
        reset_token_expiry DATETIME
    )
    ''')

    # Create default admin user
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    admin_email = "admin@proppal.com"
    admin_password = "admin"
    hashed_password = pwd_context.hash(admin_password)
    cursor.execute('INSERT INTO users (email, hashed_password, role, is_verified) VALUES (?, ?, ?, ?)', (admin_email, hashed_password, 'admin', 1))

    conn.commit()
    conn.close()
    print("Database initialized successfully!")
    print("Admin user created: admin@proppal.com / admin")

if __name__ == '__main__':
    init_db()