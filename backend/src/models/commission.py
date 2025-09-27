from pydantic import BaseModel
from typing import Optional

class Commission(BaseModel):
    id: Optional[int] = None
    affiliate_id: int
    amount: float
    status: str # Enum: Pending, Paid
    conversion_id: Optional[int] = None # Foreign Key to a conversion event
