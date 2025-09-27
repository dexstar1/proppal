from fasthtml.common import *
from components.card import Card
from components.layout import Layout
from starlette.requests import Request


def client_dashboard_content():
    """Content-only version for HTMX requests"""
    return Div(
        H1("Dashboard Content"),
        Div(
            Card(
                title="Quick Stats",
                content="Your activity overview",
                card_cls="card mb-4"
            ),
            Card(
                title="Recent Properties",
                content="Properties you've viewed",
                card_cls="card mb-4"
            ),
            cls="dashboard-content"
        ),
        cls="container-fluid"
    )


def client_dashboard(request: Request):
    """Full layout version for direct URL visits"""
    if request.headers.get("HX-Request"):
        # HTMX request - return content only
        return client_dashboard_content()
    # Regular request - return full layout
    return Layout(client_dashboard_content(), user_role="Client")


def client_properties_content():
    return Div(
        H1("Available Properties"),
        # Properties content
        cls="container-fluid"
    )


def client_properties(request: Request):
    if request.headers.get("HX-Request"):
        return client_properties_content()
    return Layout(client_properties_content(), user_role="Client")


def client_enquiries_content():
    return Div(
        H1("My Enquiries"),
        P("View your property enquiries"),
        cls="container mt-4"
    )


def client_enquiries(request: Request):
    if request.headers.get("HX-Request"):
        return client_enquiries_content()
    return Layout(client_enquiries_content(), user_role="Client")