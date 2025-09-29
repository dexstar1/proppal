#!/usr/bin/env python3
import argparse
import sqlite3


def create_sample_properties(role: str = 'admin'):
    """Create sample properties for testing the sales functionality.

    By default, attaches properties to the admin user so realtors can view/use them for sales.
    Pass --role realtor to attach to a realtor instead.
    """
    conn = sqlite3.connect('proppal.db')
    cursor = conn.cursor()

    # Get the target user ID by role
    cursor.execute('SELECT id FROM users WHERE role = ?', (role,))
    user_row = cursor.fetchone()
    if not user_row:
        print(f"No user found with role '{role}'. Please ensure such a user exists (run init_db.py for admin).")
        conn.close()
        return

    owner_user_id = user_row[0]

    # Sample properties data (images left empty to avoid missing assets; features are comma-separated)
    sample_properties = [
        {
            "name": "LAVIDA PRIME ESTATE PHASE THREE",
            "description": "Premium residential land with excellent facilities and infrastructure. Located in a serene environment with 24/7 security.",
            "price": 2500000.00,
            "realtor_id": owner_user_id,
            "address": "Plot 45, Lavida Estate",
            "country": "Nigeria",
            "state": "Lagos",
            "city": "Ibeju-Lekki",
            "area": "Lekki",
            "zip_code": "101245",
            "property_type": "land",
            "property_status": "for sale",
            "labels": "buy and build",
            "images": "",
            "features": "Accessible Road,Approved Government Excision,Good title,24 Hours Security,Perimeter Fencing"
        },
        {
            "name": "LAVIDA EMPIRE DISTRICT 1&2",
            "description": "Luxury estate development with modern amenities including golf course, tennis court, and water treatment plant.",
            "price": 3200000.00,
            "realtor_id": owner_user_id,
            "address": "Empire District Road",
            "country": "Nigeria",
            "state": "Lagos",
            "city": "Ibeju-Lekki",
            "area": "Lekki",
            "zip_code": "101246",
            "property_type": "land",
            "property_status": "for sale",
            "labels": "off-plan",
            "images": "",
            "features": "Golf Course,Tennis Court(s),Water treatment plant,24/7 uninterrupted power supply,Beautiful Landscapes"
        },
        {
            "name": "MERCYLAND ESTATE PHASE 2",
            "description": "Affordable residential plots with flexible payment plans. Perfect for first-time buyers.",
            "price": 1800000.00,
            "realtor_id": owner_user_id,
            "address": "Mercyland Avenue",
            "country": "Nigeria",
            "state": "Ogun",
            "city": "Sagamu",
            "area": "Sagamu",
            "zip_code": "121001",
            "property_type": "land",
            "property_status": "for sale",
            "labels": "ready to move in",
            "images": "",
            "features": "Interlocked Road,Good drainage system,24 Hour Water Supply,Instant Allocation,Survey"
        },
        {
            "name": "DEPALMS LUXURIOUS APARTMENT",
            "description": "Modern apartment complex with state-of-the-art facilities, gym, swimming pool, and parking space.",
            "price": 45000000.00,
            "realtor_id": owner_user_id,
            "address": "15 Depalms Avenue",
            "country": "Nigeria",
            "state": "Lagos",
            "city": "Victoria Island",
            "area": "Victoria Island",
            "zip_code": "101241",
            "property_type": "apartment",
            "property_status": "for sale",
            "labels": "open house",
            "images": "",
            "features": "Central Business District,24/7 uninterrupted power supply,Balcony,Basketball Court",
            "bedrooms": 3,
            "bathrooms": 2,
            "rooms": 5,
            "property_area_size": 120.5,
            "garages": 2,
            "year_built": 2023
        },
        {
            "name": "ADUNNI ESTATE (PREMIUM CLASS)",
            "description": "High-end residential estate with premium finishes and exclusive amenities.",
            "price": 5500000.00,
            "realtor_id": owner_user_id,
            "address": "Adunni Premium Close",
            "country": "Nigeria",
            "state": "Lagos",
            "city": "Ajah",
            "area": "Ajah",
            "zip_code": "101248",
            "property_type": "land",
            "property_status": "for sale",
            "labels": "buy and build",
            "images": "",
            "features": "Governor's Consent,Approved Gazette,Building approval,Deed of Assignment,Contract of Sales"
        }
    ]

    # Insert sample properties
    for prop in sample_properties:
        cursor.execute(
            """
            INSERT INTO properties (
                name, description, price, images, realtor_id, features, address,
                country, state, city, area, zip_code, property_type, property_status,
                labels, bedrooms, bathrooms, rooms, property_area_size, garages, year_built
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                prop["name"], prop["description"], prop["price"], prop["images"],
                prop["realtor_id"], prop["features"], prop["address"], prop["country"],
                prop["state"], prop["city"], prop["area"], prop["zip_code"],
                prop["property_type"], prop["property_status"], prop["labels"],
                prop.get("bedrooms"), prop.get("bathrooms"), prop.get("rooms"),
                prop.get("property_area_size"), prop.get("garages"), prop.get("year_built")
            )
        )

    conn.commit()
    conn.close()

    print(f"Successfully created {len(sample_properties)} sample properties for {role} user ID {owner_user_id}")
    print("Properties created:")
    for i, prop in enumerate(sample_properties, 1):
        print(f"{i}. {prop['name']} - ₦{prop['price']:,.2f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create sample properties for testing")
    parser.add_argument("--role", choices=["admin", "realtor"], default="admin", help="Attach properties to this role (default: admin)")
    args = parser.parse_args()
    create_sample_properties(role=args.role)
