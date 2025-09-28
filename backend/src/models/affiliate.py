from typing import Optional

from pydantic import BaseModel


class AffiliateLink(BaseModel):
    id: Optional[int] = None
    affiliate_id: int
    code: str
    clicks: int = 0
    conversions: int = 0
