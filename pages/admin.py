from fasthtml.common import *
from components.nav import Navbar
from components.sidebar import Sidebar
from components.card import Card

def AdminDashboard():
    return Div(
        Navbar(user_role="Admin"),
        Div(
            Sidebar(user_role="Admin"),
            Div(
                H1("Admin Dashboard"),
                Div(
                    Card(title="Total Users", content="1000", card_cls="card mb-4"),
                    Card(title="Total Properties", content="500", card_cls="card mb-4"),
                    Card(title="Pending Payouts", content="$10,000", card_cls="card mb-4"),
                    cls="row row-cols-1 row-cols-md-3 g-4"
                ),
                id="main-content",
                cls="container-fluid mt-4"
            ),
            cls="d-flex"
        )
    )
