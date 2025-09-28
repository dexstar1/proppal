from typing import Optional

from pydantic import BaseModel


class Enquiry(BaseModel):
    id: Optional[int] = None
    message: str
    property_id: int
    client_id: int
    status: str # Enum: Pending, Answered
