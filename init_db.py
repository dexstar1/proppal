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

    # Property Sales Table
    cursor.execute('DROP TABLE IF EXISTS property_sales')
    cursor.execute('''
    CREATE TABLE property_sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        property_id INTEGER NOT NULL,
        location_size TEXT NOT NULL,
        property_type TEXT NOT NULL,
        property_available INTEGER NOT NULL,
        payment_plan TEXT NOT NULL,
        property_corner TEXT NOT NULL,
        property_corner_total INTEGER DEFAULT 0,
        estate_first_sale TEXT NOT NULL,
        client_first_name TEXT NOT NULL,
        client_last_name TEXT NOT NULL,
        client_photo TEXT,
        client_identification TEXT NOT NULL,
        client_identification_upload_1 TEXT,
        client_identification_upload_2 TEXT,
        client_subscription_uploads TEXT,
        payment_reference TEXT NOT NULL,
        amount REAL NOT NULL,
        payment_uploads TEXT,
        payment_information TEXT,
        additional_information TEXT,
        realtor_id INTEGER NOT NULL,
        status TEXT DEFAULT 'pending',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (property_id) REFERENCES properties (id),
        FOREIGN KEY (realtor_id) REFERENCES users (id)
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