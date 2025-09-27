from pydantic import BaseModel
from typing import Optional

class Lead(BaseModel):
    id: Optional[int] = None
    name: str
    email: str
    phone: str
    property_id: int
    realtor_id: int
    status: str # Enum: New, Contacted, Closed
