from fasthtml.common import *
from ..models.enquiry import Enquiry
from app import app # Import the main app instance

@app.post("/enquiries")
def create_enquiry(enquiry: Enquiry):
    # Placeholder for saving the new enquiry to the database
    enquiry.id = 1 # Assign a dummy ID
    return enquiry