from fasthtml.common import *
from components.card import Card
from components.layout import Layout
from starlette.requests import Request
from backend.src.models.property import Property
from typing import List, Optional, Any
from routes.admin import execute_db, _parse_property_from_row

def realtor_dashboard_content(user_role: str = "Realtor"):
    """Content-only version for HTMX requests"""
    return Div(
        H4("Welcome"),
        H1(user_role),
        H6("At a glance, view you account summary and statistics"),
        Div(
            Card(
                title="Total earnings overall",
                content="2250000",
                card_cls="card mb-4 col-12 col-xl-6 shadow"
            ),
            Div(
                 Div(
                    Card(
                    title="My Referrals",
                    content="37",
                    card_cls="card mb-4 col-12 col-xl-6 shadow mx-2"
                    ),
                    Card(
                    title="Transactions",
                    content="61",
                    card_cls="card mb-4 col-12 col-xl-6 shadow mx-2"
                    ),
                    cls="row"
                ),cls="col-xl-6 shadow"
            ), cls="dashboard-content row"
        ),
        Div(
            Card(
                title="Total property sales",
                content="15",
                card_cls="card mb-4 col-12 col-md-6 col-xl-3 shadow mx-2"
            ),
            Card(
                title="Total pending sales",
                content="0",
                card_cls="card mb-4 col-12 col-md-6 col-xl-3 shadow mx-2"
            ),
            Card(
                title="Total approved sales",
                content="13",
                card_cls="card mb-4 col-12 col-md-6 col-xl-3 shadow mx-2"
            ),
            cls="dashboard-content row"
        ),
        Div(
            Card(
                title="Total withdrawal",
                content="2400000",
                card_cls="card mb-4 col-12 col-md-6 col-xl-3 shadow mx-2"
            ),
            Card(
                title="Total received",
                content="2150000",
                card_cls="card mb-4 col-12 col-md-6 col-xl-3 shadow mx-2"
            ),
            Card(
                title="Total downline commission",
                content="100,000",
                card_cls="card mb-4 col-12 col-md-6 col-xl-3 shadow mx-2"
            ),
            cls="dashboard-content row"
        ),
        cls="container-fluid"
    )

def realtor_dashboard(request: Request):
    """Full layout version for direct URL visits"""
    if request.headers.get("HX-Request"):
        return realtor_dashboard_content()
    return Layout(realtor_dashboard_content(), user_role="Realtor")

def get_all_properties() -> List[Property]:
    """Fetches all properties from the database."""
    rows = execute_db("SELECT * FROM properties ORDER BY id DESC", fetchall=True)
    return [_parse_property_from_row(row) for row in rows if row]

def get_property_by_id(property_id: int) -> Optional[Property]:
    row = execute_db("SELECT * FROM properties WHERE id = ?", (property_id,), fetchone=True)
    return _parse_property_from_row(row) if row else None

def realtor_properties_content(request: Request):
    properties = get_all_properties()
    return Div(
        H1("My Properties"),
        P("View all available property listings."),
        Table(
            Thead(Tr(Th("S/N"), Th("Image"), Th("Title"), Th("Location"), Th("Price"), Th("Actions"))),
            Tbody(*[Tr(
                Td(f"{i + 1}"),
                Td(Img(src=prop.images[0], cls="img-thumbnail", style="max-width: 70px;") if prop.images else "No Image"),
                Td(prop.name),
                Td(f"{prop.city or ''}, {prop.state or ''}"),
                Td(f"${prop.price:,.2f}"),
                Td(
                    A(I(cls="fe fe-eye"), hx_get=f"/realtor/properties/{prop.id}", hx_target="#main-content", cls="text-info me-3", title="View"),
                )
            ) for i, prop in enumerate(properties)]),
            cls="table table-striped"
        ),
        cls="container-fluid"
    )

def realtor_properties(request: Request):
    if request.headers.get("HX-Request"):
        return realtor_properties_content(request)
    return Layout(realtor_properties_content(request), user_role="Realtor")

def realtor_property_view_content(property_id: int) -> Any:
    """Content for viewing a single property."""
    prop = get_property_by_id(property_id)
    if not prop:
        return Div(H1("Property Not Found"), cls="alert alert-danger")

    location_parts = [prop.address, prop.city, prop.state, prop.country, prop.zip_code]
    full_location = ", ".join(filter(None, location_parts))

    return Div(
        H1(prop.name),
        Div(
            Div(H4("Status & Labels"), P(f"Status: {prop.property_status or 'N/A'}"), P(f"Type: {prop.property_type or 'N/A'}"), P(f"Label: {prop.labels or 'N/A'}"), cls="mb-4"),
            Div(H4("Details"), P(prop.description), P(f"Location: {full_location}"), P(f"Price: ${prop.price:,.2f}"), cls="mb-4"),
            Div(H4("Features"), P(", ".join(prop.features)) if prop.features else P("None"), cls="mb-4"),
            Div(H4("Images"), *[Img(src=img, cls="img-thumbnail me-2 mb-2", style="max-width: 200px") for img in prop.images], cls="mb-4"),
            Button("Back to Properties", cls="btn btn-secondary", hx_get="/realtor/properties", hx_target="#main-content"),
        ),
        cls="container-fluid"
    )

def realtor_property_view(request: Request):
    property_id = int(request.path_params['property_id'])
    return realtor_property_view_content(property_id)

def realtor_referrals_content():
    return Div(
        H1("My Referrals"),
        P("Track and manage your referrals."),
        cls="container-fluid"
    )

def realtor_referrals(request: Request):
    if request.headers.get("HX-Request"):
        return realtor_referrals_content()
    return Layout(realtor_referrals_content(), user_role="Realtor")

def realtor_commissions_content():
    return Div(H1("My Commissions"))

def realtor_commissions(request: Request):
    if request.headers.get("HX-Request"):
        return realtor_commissions_content()
    return Layout(realtor_commissions_content(), user_role="Realtor")

def realtor_payouts_content():
    return Div(H1("My Payouts"))

def realtor_payouts(request: Request):
    if request.headers.get("HX-Request"):
        return realtor_payouts_content()
    return Layout(realtor_payouts_content(), user_role="Realtor")
    