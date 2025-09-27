from fasthtml.common import *
from ..models.property import Property
from ..services.property_service import PropertyService
from app import app # Import the main app instance

property_service = PropertyService() # Initialize the service

@app.get("/properties")
def get_properties():
    return property_service.get_all_properties()

@app.post("/properties")
def create_property(property: Property):
    return property_service.create_property(property)