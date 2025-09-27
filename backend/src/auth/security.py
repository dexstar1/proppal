from passlib.context import CryptContext
import secrets

# Setup the password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain-text password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hashes a plain-text password."""
    return pwd_context.hash(password)

def create_secure_token() -> str:
    """Creates a secure, URL-safe token."""
    return secrets.token_urlsafe(32)
