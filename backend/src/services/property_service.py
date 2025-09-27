from typing import List, Optional
from ..models.property import Property

class PropertyService:
    def __init__(self):
        self.properties = [
            Property(id=1, name="Modern Apartment", description="A beautiful apartment", price=250000.0, location="New York", realtor_id=2),
            Property(id=2, name="Family House", description="Spacious family house", price=500000.0, location="Los Angeles", realtor_id=2),
        ]

    def get_all_properties(self) -> List[Property]:
        return self.properties

    def get_property_by_id(self, property_id: int) -> Optional[Property]:
        return next((prop for prop in self.properties if prop.id == property_id), None)

    def create_property(self, property: Property) -> Property:
        property.id = len(self.properties) + 1
        self.properties.append(property)
        return property

    def update_property(self, property_id: int, updated_property: Property) -> Optional[Property]:
        for i, prop in enumerate(self.properties):
            if prop.id == property_id:
                self.properties[i] = updated_property
                self.properties[i].id = property_id # Ensure ID remains the same
                return self.properties[i]
        return None

    def delete_property(self, property_id: int) -> bool:
        initial_len = len(self.properties)
        self.properties = [prop for prop in self.properties if prop.id != property_id]
        return len(self.properties) < initial_len
