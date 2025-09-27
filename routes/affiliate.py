from fasthtml.common import *
from components.card import Card
from components.layout import Layout
from starlette.requests import Request

def affiliate_dashboard_content():
    """Content-only version for HTMX requests"""
    return Div(
        H1("Affiliate Dashboard"),
        Div(
            Card(
                title="Total Referrals",
                content="156 Referrals",
                card_cls="card mb-4"
            ),
            Card(
                title="Active Commissions",
                content="$2,450",
                card_cls="card mb-4"
            ),
            Card(
                title="Pending Payouts",
                content="$750",
                card_cls="card mb-4"
            ),
            cls="dashboard-content"
        ),
        cls="container-fluid"
    )

def affiliate_dashboard(request: Request):
    """Full layout version for direct URL visits"""
    if request.headers.get("HX-Request"):
        return affiliate_dashboard_content()
    return Layout(affiliate_dashboard_content(), user_role="Affiliate")

def affiliate_referrals_content():
    return Div(
        H1("My Referrals"),
        Table(
            Thead(
                Tr(
                    Th("Referral ID"),
                    Th("Date"),
                    Th("Status"),
                    Th("Commission")
                )
            ),
            Tbody(
                Tr(
                    Td("#REF001"),
                    Td("2023-09-21"),
                    Td("Completed"),
                    Td("$150")
                )
            ),
            cls="table table-striped"
        ),
        cls="container-fluid"
    )

def affiliate_referrals(request: Request):
    if request.headers.get("HX-Request"):
        return affiliate_referrals_content()
    return Layout(affiliate_referrals_content(), user_role="Affiliate")

def affiliate_commissions_content():
    return Div(
        H1("Commission History"),
        Table(
            Thead(
                Tr(
                    Th("Transaction ID"),
                    Th("Date"),
                    Th("Amount"),
                    Th("Status")
                )
            ),
            Tbody(
                Tr(
                    Td("#TRX001"),
                    Td("2023-09-21"),
                    Td("$150"),
                    Td("Paid")
                )
            ),
            cls="table table-striped"
        ),
        cls="container-fluid"
    )

def affiliate_commissions(request: Request):
    if request.headers.get("HX-Request"):
        return affiliate_commissions_content()
    return Layout(affiliate_commissions_content(), user_role="Affiliate")

def affiliate_payouts_content():
    return Div(
        H1("Payout Settings"),
        Form(
            Div(
                Label("Payout Method"),
                Select(
                    Option("Bank Transfer", value="bank"),
                    Option("PayPal", value="paypal"),
                    cls="form-select"
                ),
                cls="mb-3"
            ),
            Div(
                Label("Minimum Payout Amount"),
                Input(type="number", value="100", cls="form-control"),
                cls="mb-3"
            ),
            Button("Save Settings", type="submit", cls="btn btn-primary"),
            cls="card p-4"
        ),
        cls="container-fluid"
    )

def affiliate_payouts(request: Request):
    if request.headers.get("HX-Request"):
        return affiliate_payouts_content()
    return Layout(affiliate_payouts_content(), user_role="Affiliate")