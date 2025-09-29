import asyncio
import sqlite3
import json
from datetime import datetime
from typing import List, Optional
from backend.src.models.property_sale import PropertySale, PropertySaleInDB, PropertySaleResponse


def _get_property_sales_by_realtor_sync(realtor_id: int) -> List[PropertySaleResponse]:
    """Fetch all property sales for a specific realtor"""
    conn = sqlite3.connect('proppal.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT ps.*, p.name as property_name, u.email as realtor_email
        FROM property_sales ps
        LEFT JOIN properties p ON ps.property_id = p.id
        LEFT JOIN users u ON ps.realtor_id = u.id
        WHERE ps.realtor_id = ?
        ORDER BY ps.created_at DESC
    """, (realtor_id,))
    
    rows = cursor.fetchall()
    conn.close()
    
    sales = []
    for row in rows:
        sale = PropertySaleResponse(
            id=row['id'],
            property_id=row['property_id'],
            property_name=row['property_name'],
            client_first_name=row['client_first_name'],
            client_last_name=row['client_last_name'],
            amount=row['amount'],
            status=row['status'],
            created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else datetime.now(),
            realtor_id=row['realtor_id'],
            realtor_name=row['realtor_email']
        )
        sales.append(sale)
    
    return sales


async def get_property_sales_by_realtor(realtor_id: int) -> List[PropertySaleResponse]:
    """Async wrapper for getting property sales by realtor"""
    return await asyncio.to_thread(_get_property_sales_by_realtor_sync, realtor_id)


def _get_property_sale_by_id_sync(sale_id: int) -> Optional[PropertySaleInDB]:
    """Fetch a property sale by ID"""
    conn = sqlite3.connect('proppal.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM property_sales WHERE id = ?", (sale_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
    
    # Convert JSON strings back to lists
    client_subscription_uploads = json.loads(row['client_subscription_uploads']) if row['client_subscription_uploads'] else []
    payment_uploads = json.loads(row['payment_uploads']) if row['payment_uploads'] else []
    
    return PropertySaleInDB(
        id=row['id'],
        property_id=row['property_id'],
        location_size=row['location_size'],
        property_type=row['property_type'],
        property_available=row['property_available'],
        payment_plan=row['payment_plan'],
        property_corner=row['property_corner'],
        property_corner_total=row['property_corner_total'],
        estate_first_sale=row['estate_first_sale'],
        client_first_name=row['client_first_name'],
        client_last_name=row['client_last_name'],
        client_photo=row['client_photo'],
        client_identification=row['client_identification'],
        client_identification_upload_1=row['client_identification_upload_1'],
        client_identification_upload_2=row['client_identification_upload_2'],
        client_subscription_uploads=client_subscription_uploads,
        payment_reference=row['payment_reference'],
        amount=row['amount'],
        payment_uploads=payment_uploads,
        payment_information=row['payment_information'],
        additional_information=row['additional_information'],
        realtor_id=row['realtor_id'],
        status=row['status'],
        approved_by=row['approved_by'] if 'approved_by' in row.keys() else None,
        approved_at=datetime.fromisoformat(row['approved_at']) if ('approved_at' in row.keys() and row['approved_at']) else None,
        rejected_at=datetime.fromisoformat(row['rejected_at']) if ('rejected_at' in row.keys() and row['rejected_at']) else None,
        reject_reason=row['reject_reason'] if 'reject_reason' in row.keys() else None,
        created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else datetime.now(),
        updated_at=datetime.fromisoformat(row['updated_at']) if row['updated_at'] else datetime.now()
    )


async def get_property_sale_by_id(sale_id: int) -> Optional[PropertySaleInDB]:
    """Async wrapper for getting property sale by ID"""
    return await asyncio.to_thread(_get_property_sale_by_id_sync, sale_id)


def _create_property_sale_sync(sale_data: dict) -> PropertySaleInDB:
    """Create a new property sale"""
    conn = sqlite3.connect('proppal.db')
    cursor = conn.cursor()
    
    # Convert lists to JSON strings for storage
    client_subscription_uploads = json.dumps(sale_data.get('client_subscription_uploads', []))
    payment_uploads = json.dumps(sale_data.get('payment_uploads', []))
    
    cursor.execute("""
        INSERT INTO property_sales (
            property_id, location_size, property_type, property_available,
            payment_plan, property_corner, property_corner_total, estate_first_sale,
            client_first_name, client_last_name, client_photo, client_identification,
            client_identification_upload_1, client_identification_upload_2,
            client_subscription_uploads, payment_reference, amount, payment_uploads,
            payment_information, additional_information, realtor_id, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        sale_data['property_id'], sale_data['location_size'], sale_data['property_type'],
        sale_data['property_available'], sale_data['payment_plan'], sale_data['property_corner'],
        sale_data['property_corner_total'], sale_data['estate_first_sale'],
        sale_data['client_first_name'], sale_data['client_last_name'],
        sale_data.get('client_photo'), sale_data['client_identification'],
        sale_data.get('client_identification_upload_1'), sale_data.get('client_identification_upload_2'),
        client_subscription_uploads, sale_data['payment_reference'], sale_data['amount'],
        payment_uploads, sale_data.get('payment_information'),
        sale_data.get('additional_information'), sale_data['realtor_id'], 'pending'
    ))
    
    conn.commit()
    sale_id = cursor.lastrowid
    conn.close()
    
    # Return the created sale
    return _get_property_sale_by_id_sync(sale_id)


async def create_property_sale(sale_data: dict) -> PropertySaleInDB:
    """Async wrapper for creating property sale"""
    return await asyncio.to_thread(_create_property_sale_sync, sale_data)


def _update_property_sale_sync(sale_id: int, sale_data: dict) -> Optional[PropertySaleInDB]:
    """Update an existing property sale"""
    conn = sqlite3.connect('proppal.db')
    cursor = conn.cursor()
    
    # Build dynamic update query
    update_fields = []
    values = []
    
    for field, value in sale_data.items():
        if value is not None:
            if field in ['client_subscription_uploads', 'payment_uploads'] and isinstance(value, list):
                value = json.dumps(value)
            update_fields.append(f"{field} = ?")
            values.append(value)
    
    if not update_fields:
        conn.close()
        return _get_property_sale_by_id_sync(sale_id)
    
    # Add updated_at field
    update_fields.append("updated_at = ?")
    values.append(datetime.now().isoformat())
    values.append(sale_id)
    
    query = f"UPDATE property_sales SET {', '.join(update_fields)} WHERE id = ?"
    cursor.execute(query, values)
    conn.commit()
    conn.close()
    
    return _get_property_sale_by_id_sync(sale_id)


async def update_property_sale(sale_id: int, sale_data: dict) -> Optional[PropertySaleInDB]:
    """Async wrapper for updating property sale"""
    return await asyncio.to_thread(_update_property_sale_sync, sale_id, sale_data)


def _delete_property_sale_sync(sale_id: int) -> bool:
    """Delete a property sale"""
    conn = sqlite3.connect('proppal.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM property_sales WHERE id = ?", (sale_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted


async def delete_property_sale(sale_id: int) -> bool:
    """Async wrapper for deleting property sale"""
    return await asyncio.to_thread(_delete_property_sale_sync, sale_id)


def _get_available_properties_for_realtor_sync(realtor_id: int) -> List[dict]:
    """Get properties available for sale by realtor.

    Returns only properties created by admin user(s).
    """
    conn = sqlite3.connect('proppal.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name, property_type, city, state, price
        FROM properties
        WHERE realtor_id IN (SELECT id FROM users WHERE role = 'admin')
        ORDER BY name
        """
    )

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


async def get_available_properties_for_realtor(realtor_id: int) -> List[dict]:
    """Async wrapper for getting available properties for realtor"""
    return await asyncio.to_thread(_get_available_properties_for_realtor_sync, realtor_id)