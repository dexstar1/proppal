from typing import List, Optional

from pydantic import BaseModel


class Property(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    price: float
    images: List[str] = []
    realtor_id: int
    features: Optional[List[str]] = []
    address: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    area: Optional[str] = None
    zip_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    virtual_tour_url: Optional[str] = None
    property_type: Optional[str] = None
    property_status: Optional[str] = None
    labels: Optional[str] = None
    video_url: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    rooms: Optional[int] = None
    property_area_size: Optional[float] = None
    property_land_size: Optional[float] = None
    garages: Optional[int] = None
    year_built: Optional[int] = None
