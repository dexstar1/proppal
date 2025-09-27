from fasthtml.common import *
from components.nav import Nav
from components.sidebar import Sidebar
from components.card import Card

def AffiliateDashboard():
    return Div(
        Navbar(user_role="Affiliate"),
        Div(
            Sidebar(user_role="Affiliate"),
            Div(
                H1("Affiliate Dashboard"),
                Div(
                    Card(title="Referral Clicks", content="1200", card_cls="card mb-4"),
                    Card(title="Conversions", content="50", card_cls="card mb-4"),
                    Card(title="Total Earnings", content="$5,000", card_cls="card mb-4"),
                    cls="row row-cols-1 row-cols-md-3 g-4"
                ),
                id="main-content",
                cls="container-fluid mt-4"
            ),
            cls="d-flex"
        )
    )