import asyncio
import sqlite3
from typing import Optional

from backend.src.auth.security import create_secure_token, get_password_hash
from backend.src.models.user import UserInDB


def _get_user_by_id_sync(user_id: int) -> Optional[UserInDB]:
    conn = sqlite3.connect('proppal.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user_row = cursor.fetchone()
    conn.close()
    if user_row:
        return UserInDB(**user_row)
    return None

async def get_user_by_id(user_id: int) -> Optional[UserInDB]:
    """Fetches a user by their ID asynchronously."""
    return await asyncio.to_thread(_get_user_by_id_sync, user_id)

def _get_verification_status(email: str) -> Optional[UserInDB]:
    conn = sqlite3.connect('proppal.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user_row = cursor.fetchone()
    conn.close()
    if user_row:
        return UserInDB(**user_row)
    return None

async def get_verification_status(email: str):
    return _get_verification_status(email)

def _get_user_by_email_sync(email: str) -> Optional[UserInDB]:
    conn = sqlite3.connect('proppal.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user_row = cursor.fetchone()
    conn.close()
    if user_row:
        return UserInDB(**user_row)
    return None

async def get_user_by_email(email: str) -> Optional[UserInDB]:
    """Fetches a user by their email asynchronously."""
    return await asyncio.to_thread(_get_user_by_email_sync, email)

def _create_realtor_user_sync(email: str, password: str) -> tuple[UserInDB, str]:
    """Creates a new user with the 'realtor' role and a verification token."""
    hashed_password = get_password_hash(password)
    role = "realtor"
    is_verified = False
    verification_token = create_secure_token()

    conn = sqlite3.connect('proppal.db')
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (email, hashed_password, role, is_verified, "
            "verification_token) VALUES (?, ?, ?, ?, ?)",
            (email, hashed_password, role, is_verified, verification_token),
        )
        conn.commit()
        user_id = cursor.lastrowid
    finally:
        conn.close()

    user = UserInDB(
        id=user_id,
        email=email,
        hashed_password=hashed_password,
        role=role,
        is_verified=is_verified,
        verification_token=verification_token
    )
    return user, verification_token

async def create_realtor_user(email: str, password: str) -> tuple[UserInDB, str]:
    return await asyncio.to_thread(_create_realtor_user_sync, email, password)

# ... (set_password_reset_token, get_user_by_reset_token,
# update_user_password are fine) ...

def verify_user_by_token(token: str) -> bool:
    """Verifies a user by their token and clears the token."""
    conn = sqlite3.connect('proppal.db')
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET is_verified = 1, verification_token = NULL "
        "WHERE verification_token = ?",
        (token,),
    )
    conn.commit()
    updated_rows = cursor.rowcount
    conn.close()
    return updated_rows > 0
