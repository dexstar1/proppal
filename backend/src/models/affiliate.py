from pydantic import BaseModel
from typing import Optional

class AffiliateLink(BaseModel):
    id: Optional[int] = None
    affiliate_id: int
    code: str
    clicks: int = 0
    conversions: int = 0
