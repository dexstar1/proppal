from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: Optional[int] = None
    email: str
    role: str # 'admin' or 'realtor'
    is_verified: bool = False

class UserInDB(User):
    hashed_password: str
    verification_token: Optional[str] = None
    reset_token: Optional[str] = None
    reset_token_expiry: Optional[datetime] = None
