from fasthtml.common import *
from components.nav import Navbar
from components.sidebar import Sidebar
from components.card import Card

def RealtorDashboard():
    return Div(
        Navbar(user_role="Realtor"),
        Div(
            Sidebar(user_role="Realtor"),
            Div(
                H1("Realtor Dashboard"),
                Div(
                    Card(title="My Properties", content="50", card_cls="card mb-4"),
                    Card(title="New Leads", content="15", card_cls="card mb-4"),
                    Card(title="Pending Enquiries", content="8", card_cls="card mb-4"),
                    cls="row row-cols-1 row-cols-md-3 g-4"
                ),
                id="main-content",
                cls="container-fluid mt-4"
            ),
            cls="d-flex"
        )
    )
