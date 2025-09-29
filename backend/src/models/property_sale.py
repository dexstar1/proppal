from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, validator


class PropertySale(BaseModel):
    id: Optional[int] = None
    
    # Property Information (Section 01)
    property_id: int
    location_size: str
    property_type: str  # commercial, residential
    property_available: int
    payment_plan: str
    property_corner: str  # yes, no
    property_corner_total: int = 0
    estate_first_sale: str  # yes, no
    
    # Client Information (Section 02)
    client_first_name: str
    client_last_name: str
    client_photo: Optional[str] = None
    client_identification: str  # international_passport, nin_national_id, driver_licence
    client_identification_upload_1: Optional[str] = None
    client_identification_upload_2: Optional[str] = None
    client_subscription_uploads: Optional[List[str]] = []
    
    # Payment Information (Section 03)
    payment_reference: str  # existing, new
    amount: float
    payment_uploads: Optional[List[str]] = []
    payment_information: Optional[str] = None
    
    # Miscellaneous (Section 04)
    additional_information: Optional[str] = None
    
    # System fields
    realtor_id: int
    status: str = "pending"  # pending, approved, rejected
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    rejected_at: Optional[datetime] = None
    reject_reason: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be positive')
        return v
    
    @validator('property_available')
    def validate_property_available(cls, v):
        if v <= 0:
            raise ValueError('Property available count must be positive')
        return v
    
    @validator('property_corner_total')
    def validate_corner_total(cls, v, values):
        if values.get('property_corner') == 'yes' and v <= 0:
            raise ValueError('Corner piece total must be positive when corner piece is needed')
        return v


class PropertySaleInDB(PropertySale):
    """Property sale model as stored in database"""
    pass


class PropertySaleCreate(BaseModel):
    """Model for creating a new property sale"""
    property_id: int
    location_size: str
    property_type: str
    property_available: int
    payment_plan: str
    property_corner: str
    property_corner_total: int = 0
    estate_first_sale: str
    client_first_name: str
    client_last_name: str
    client_identification: str
    payment_reference: str
    amount: float
    payment_information: Optional[str] = None
    additional_information: Optional[str] = None


class PropertySaleUpdate(BaseModel):
    """Model for updating a property sale"""
    location_size: Optional[str] = None
    property_type: Optional[str] = None
    property_available: Optional[int] = None
    payment_plan: Optional[str] = None
    property_corner: Optional[str] = None
    property_corner_total: Optional[int] = None
    estate_first_sale: Optional[str] = None
    client_first_name: Optional[str] = None
    client_last_name: Optional[str] = None
    client_identification: Optional[str] = None
    payment_reference: Optional[str] = None
    amount: Optional[float] = None
    payment_information: Optional[str] = None
    additional_information: Optional[str] = None
    status: Optional[str] = None


class PropertySaleResponse(BaseModel):
    """Model for property sale API responses"""
    id: int
    property_id: int
    property_name: Optional[str] = None
    client_first_name: str
    client_last_name: str
    amount: float
    status: str
    created_at: datetime
    realtor_id: int
    realtor_name: Optional[str] = None