from fasthtml.common import *
from components.nav import Navbar
from components.sidebar import Sidebar
from components.card import Card

def ClientDashboard():
    return Div(
        Navbar(user_role="Client"),
        Div(
            Sidebar(user_role="Client"),
            Div(
                H1("Client Dashboard"),
                Div(
                    Card(title="Properties Viewed", content="75", card_cls="card mb-4"),
                    Card(title="Enquiries Made", content="12", card_cls="card mb-4"),
                    Card(title="Saved Properties", content="5", card_cls="card mb-4"),
                    cls="row row-cols-1 row-cols-md-3 g-4"
                ),
                id="main-content",
                cls="container-fluid mt-4"
            ),
            cls="d-flex"
        )
    )
