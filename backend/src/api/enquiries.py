from app import app  # Import the main app instance

from ..models.enquiry import Enquiry


@app.post("/enquiries")
def create_enquiry(enquiry: Enquiry):
    # Placeholder for saving the new enquiry to the database
    enquiry.id = 1 # Assign a dummy ID
    return enquiry
