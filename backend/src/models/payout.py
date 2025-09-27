from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Payout(BaseModel):
    id: Optional[int] = None
    user_id: int
    amount: float
    date: datetime = datetime.now()
    status: str # Enum: Pending, Completed, Failed
    method: str # e.g., PayPal, Bank Transfer
