from fasthtml.common import *
from components.card import Card
from components.layout import Layout
from starlette.requests import Request

def realtor_dashboard_content():
    """Content-only version for HTMX requests"""
    return Div(
        H1("Realtor Dashboard"),
        Div(
            Card(
                title="Active Listings",
                content="12 Properties",
                card_cls="card mb-4"
            ),
            Card(
                title="Total Leads",
                content="48 New Leads",
                card_cls="card mb-4"
            ),
            Card(
                title="Pending Enquiries",
                content="8 Pending Responses",
                card_cls="card mb-4"
            ),
            cls="dashboard-content"
        ),
        cls="container-fluid"
    )

def realtor_dashboard(request: Request):
    """Full layout version for direct URL visits"""
    if request.headers.get("HX-Request"):
        return realtor_dashboard_content()
    return Layout(realtor_dashboard_content(), user_role="Realtor")

def realtor_properties_content():
    return Div(
        H1("My Properties"),
        P("Manage your property listings"),
        # Add property management table/grid here
        cls="container-fluid"
    )

def realtor_properties(request: Request):
    if request.headers.get("HX-Request"):
        return realtor_properties_content()
    return Layout(realtor_properties_content(), user_role="Realtor")

def realtor_leads_content():
    return Div(
        H1("Lead Management"),
        P("Track and manage your leads"),
        # Add leads table here
        cls="container-fluid"
    )

def realtor_leads(request: Request):
    if request.headers.get("HX-Request"):
        return realtor_leads_content()
    return Layout(realtor_leads_content(), user_role="Realtor")

def realtor_enquiries_content():
    return Div(
        H1("Property Enquiries"),
        P("Manage property enquiries from clients"),
        # Add enquiries table here
        cls="container-fluid"
    )

def realtor_enquiries(request: Request):
    if request.headers.get("HX-Request"):
        return realtor_enquiries_content()
    return Layout(realtor_enquiries_content(), user_role="Realtor")