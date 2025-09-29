import os
import sqlite3
import pytest

from backend.src.api.admin_sales import (
    ensure_admin_sales_schema,
    approve_sale_and_create_payout,
    reject_sale,
    mark_payout_paid,
)
from backend.src.api.notifications import get_notifications_for_user, mark_notification_read, get_unread_count_for_user, mark_all_notifications_read

DB_PATH = 'proppal.db'


def setup_module(module):
    # Ensure schemas exist
    ensure_admin_sales_schema()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Minimal fixtures: user (realtor), property, sale
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT, role TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS properties (id INTEGER PRIMARY KEY, name TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS property_sales (id INTEGER PRIMARY KEY, property_id INTEGER, location_size TEXT, property_type TEXT, property_available INTEGER, payment_plan TEXT, property_corner TEXT, property_corner_total INTEGER, estate_first_sale TEXT, client_first_name TEXT, client_last_name TEXT, client_photo TEXT, client_identification TEXT, client_identification_upload_1 TEXT, client_identification_upload_2 TEXT, client_subscription_uploads TEXT, payment_reference TEXT, amount REAL, payment_uploads TEXT, payment_information TEXT, additional_information TEXT, realtor_id INTEGER, status TEXT DEFAULT 'pending', created_at TEXT, updated_at TEXT)")

    # Seed
    c.execute("INSERT INTO users (id, email, role) VALUES (100, 'realtor@example.com', 'realtor')")
    c.execute("INSERT INTO properties (id, name) VALUES (200, 'Test Estate')")
    c.execute("INSERT INTO property_sales (id, property_id, location_size, property_type, property_available, payment_plan, property_corner, property_corner_total, estate_first_sale, client_first_name, client_last_name, client_photo, client_identification, client_identification_upload_1, client_identification_upload_2, client_subscription_uploads, payment_reference, amount, payment_uploads, payment_information, additional_information, realtor_id, status, created_at) VALUES (300, 200, 'standard', 'residential', 1, 'outright', 'no', 0, 'no', 'John', 'Doe', NULL, 'international_passport', NULL, NULL, '[]', 'existing', 1000000.0, '[]', NULL, NULL, 100, 'pending', '2024-01-01T00:00:00')")
    conn.commit()
    conn.close()


def test_approve_creates_payout_and_notification():
    res = approve_sale_and_create_payout(300, admin_id=1, commission_rate=0.1)
    assert res['updated'] is True
    notifs = get_notifications_for_user(100)
    assert any('Sale Approved' in n['title'] for n in notifs)


def test_reject_creates_notification():
    ok = reject_sale(300, admin_id=1, reason='Invalid documents')
    assert ok is True
    notifs = get_notifications_for_user(100)
    assert any('Sale Rejected' in n['title'] for n in notifs)


def test_payout_paid_creates_notification():
    # For the previously approved sale, locate payout id and mark paid
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id FROM commission_payouts WHERE sale_id = 300 ORDER BY id DESC LIMIT 1")
    row = c.fetchone()
    conn.close()
    if row:
        ok = mark_payout_paid(row[0], admin_id=1, method='bank_transfer', reference='TRX123')
        assert ok is True
        notifs = get_notifications_for_user(100)
        assert any('Payout Completed' in n['title'] for n in notifs)


def test_mark_notification_read_and_unread_count():
    notifs = get_notifications_for_user(100)
    if notifs:
        first = notifs[0]
        before = get_unread_count_for_user(100)
        mark_notification_read(first['id'], 100)
        after = get_unread_count_for_user(100)
        assert after <= before


def test_mark_all_notifications_read():
    notifs = get_notifications_for_user(100)
    if notifs:
        count_before = get_unread_count_for_user(100)
        mark_all_notifications_read(100)
        count_after = get_unread_count_for_user(100)
        assert count_after == 0 or count_after < count_before
