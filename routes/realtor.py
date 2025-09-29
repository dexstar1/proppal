from fasthtml.common import *
from components.card import Card
from components.layout import Layout
from starlette.requests import Request
from routes.realtor_sales import realtor_sales_route_handler
from backend.src.models.property import Property
from typing import List, Optional, Any
from routes.admin import execute_db, _parse_property_from_row

from backend.src.api.wallets import get_wallet_balance

from backend.src.api.admin_sales import get_commissions_by_realtor, get_all_sales
from backend.src.api.wallets import get_withdraw_requests_by_realtor

def realtor_dashboard_content(user_role: str = "Realtor", wallet_balance: float = 0.0, commissions: list = None, stats: dict | None = None, withdraws: list | None = None):
    """Content-only version for HTMX requests"""
    commissions = commissions or []
    stats = stats or {}
    referrals_count = stats.get('referrals_count', 0)
    transactions_count = stats.get('transactions_count', 0)
    total_sales = stats.get('total_sales', 0)
    pending_sales = stats.get('pending_sales', 0)
    approved_sales = stats.get('approved_sales', 0)
    total_withdrawn = stats.get('total_withdrawn', 0.0)
    total_commission_amount = stats.get('total_commission_amount', 0.0)
    withdraws = withdraws or []

    def commission_rows():
        if not commissions:
            return Tr(Td("No commissions", colspan="4", cls="text-center text-muted py-3"))
        rows = []
        for c in commissions[:5]:
            rows.append(Tr(
                Td(f"Sale #{c['sale_id']}"),
                Td(f"₦{float(c['amount']):,.2f}"),
                Td(Span(c['status'].title(), cls=f"badge bg-{'success' if c['status']=='approved' else 'warning' if c['status']=='pending' else 'danger'}")),
                Td(c['created_at'] or ''),
            ))
        return Fragment(*rows)
    return Div(
        P("Welcome"),
        H1(user_role),
        P("At a glance, view you account summary and statistics"),
        Div(
            Div(
                Div(
                    Div(
                        Card(
                        title="Wallet Balance",
                        content=f"₦{wallet_balance:,.2f}",
                        card_cls="card mb-4 col-12 shadow"
                        ),
                        cls="row"
                    ),
                    Div(
                        Card(
                        title="My Referrals",
                        content=str(referrals_count),
                        card_cls="card mb-4 col-12 col-md-6 col-xl-6 shadow"
                        ),
                        Card(
                        title="Transactions",
                        content=str(transactions_count),
                        card_cls="card mb-4 col-12 col-md-6 col-xl-6 shadow"
                        ),
                        cls="row"
                    ), 
                    cls="col-12"
                ), 
                cls="col-12 col-xl-5 shadow"
            ),  
            Div(
                Div(
                    Card(
                        title="Total property sales",
                        content=str(total_sales),
                        card_cls="card mb-4 col-12 col-md-6 col-xl-5 shadow mx-2"
                    ),
                    Card(
                        title="Total pending sales",
                        content=str(pending_sales),
                        card_cls="card mb-4 col-12 col-md-6 col-xl-5 shadow mx-2"
                    ),
                    Card(
                        title="Total approved sales",
                        content=str(approved_sales),
                        card_cls="card mb-4 col-12 col-md-6 col-xl-5 shadow mx-2"
                    ),
                    Card(
                        title="Total withdrawal",
                        content=f"₦{total_withdrawn:,.2f}",
                        card_cls="card mb-4 col-12 col-md-6 col-xl-5 shadow mx-2"
                    ),
                    Card(
                        title="Total commission earned",
                        content=f"₦{total_commission_amount:,.2f}",
                        card_cls="card mb-4 col-12 col-md-6 col-xl-5 shadow mx-2"
                    ),
                    Card(
                        title="Total downline commission",
                        content="₦0.00",
                        card_cls="card mb-4 col-12 col-md-6 col-xl-5 shadow mx-2"
                    ),
                    cls="dashboard-content row"
                ),
                cls="col-12 col-xl-7"
            ),
                Card(
                    title="My Commissions",
                    content=Table(
                        Thead(Tr(Th("Sale"), Th("Amount"), Th("Status"), Th("Created"))),
                        Tbody(commission_rows()),
                        cls="table table-sm"
                    ),
                    card_cls="card mb-4 col-12 shadow"
                ),
                Card(
                    title="My Transactions (Withdrawals)",
                    content=Table(
                        Thead(Tr(Th("Amount"), Th("Method"), Th("Status"), Th("Requested"), Th("Decided"))),
                        Tbody(
                            *(Tr(
                                Td(f"₦{float(w['amount']):,.2f}"),
                                Td(w['method'] or ''),
                                Td(Span((w['status'] or '').title(), cls=f"badge bg-{'success' if w['status']=='approved' else 'warning' if w['status']=='pending' else 'danger'}")),
                                Td(w['created_at'] or ''),
                                Td(w['decided_at'] or '')
                            ) for w in withdraws) if withdraws else Tr(Td("No withdrawals", colspan="5", cls="text-center text-muted py-3"))
                        ),
                        cls="table table-sm"
                    ),
                    card_cls="card mb-4 col-12 shadow"
                ),
            cls="row"
            ),
            cls="container-fluid"
        )

def realtor_dashboard(request: Request):
    """Full layout version for direct URL visits"""
    user = request.scope.get('user')
    bal = get_wallet_balance(user.id) if user else 0.0
    comms = get_commissions_by_realtor(user.id) if user else []

    # Compute stats
    total_commission_amount = sum(float(c['amount']) for c in comms if c['status'] == 'approved') if comms else 0.0
    # Sales stats from all sales filtered by current realtor
    from backend.src.api.admin_sales import get_all_sales
    sales_rows = get_all_sales()
    my_sales = [r for r in sales_rows if user and r['realtor_id'] == user.id]
    total_sales = len(my_sales)
    pending_sales = len([r for r in my_sales if r['status'] == 'pending'])
    approved_sales = len([r for r in my_sales if r['status'] == 'approved'])

    # Withdrawals
    from backend.src.api.wallets import get_withdraw_requests_by_realtor
    my_withdraws = get_withdraw_requests_by_realtor(user.id) if user else []
    total_withdrawn = sum(float(w['amount']) for w in my_withdraws if w['status'] == 'approved') if my_withdraws else 0.0

    stats = {
        'referrals_count': 0,
        'transactions_count': total_sales,
        'total_sales': total_sales,
        'pending_sales': pending_sales,
        'approved_sales': approved_sales,
        'total_withdrawn': total_withdrawn,
        'total_commission_amount': total_commission_amount,
    }

    if request.headers.get("HX-Request"):
        return realtor_dashboard_content(wallet_balance=bal, commissions=comms, stats=stats, withdraws=my_withdraws)
    return Layout(realtor_dashboard_content(wallet_balance=bal, commissions=comms, stats=stats, withdraws=my_withdraws), user_role="Realtor")

def get_all_properties() -> List[Property]:
    """Fetch only properties created by admin users for realtors to view."""
    rows = execute_db(
        """
        SELECT * FROM properties
        WHERE realtor_id IN (SELECT id FROM users WHERE role = 'admin')
        ORDER BY id DESC
        """,
        fetchall=True
    )
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

def realtor_commissions_content(user_id: int):
    rows = get_commissions_by_realtor(user_id)
    def row_to_tr(c):
        return Tr(
            Td(f"Sale #{c['sale_id']}"),
            Td(f"₦{float(c['amount']):,.2f}"),
            Td(Span(c['status'].title(), cls=f"badge bg-{'success' if c['status']=='approved' else 'warning' if c['status']=='pending' else 'danger'}")),
            Td(c['created_at'] or ''),
        )
    table = Table(
        Thead(Tr(Th("Sale"), Th("Amount"), Th("Status"), Th("Created"))),
        Tbody(*(row_to_tr(c) for c in rows) if rows else Tr(Td("No commissions", colspan="4", cls="text-center text-muted py-4"))),
        cls="table table-striped table-hover"
    )
    return Div(H1("My Commissions", cls="mb-3"), table, cls="container-fluid")

def realtor_commissions(request: Request):
    user = request.scope.get('user')
    if not user:
        return RedirectResponse(url="/login")
    content = realtor_commissions_content(user.id)
    # Flash toast
    flash = request.session.pop('flash', None) if hasattr(request, 'session') else None
    if flash and isinstance(flash, dict):
        content = Div(content, Script(f"showToast({(flash.get('message') or '')!r}, {(flash.get('level') or 'info')!r})"))
    if request.headers.get("HX-Request"):
        return content
    return Layout(content, user_role="Realtor")

from backend.src.api.wallets import ensure_wallets_schema, create_withdraw_request, get_withdraw_requests_by_realtor

def realtor_withdraw_content(user_id: int):
    bal = get_wallet_balance(user_id)
    requests = get_withdraw_requests_by_realtor(user_id)
    def row_to_tr(idx, r):
        return Tr(
            Td(str(idx+1)),
            Td(f"₦{float(r['amount']):,.2f}"),
            Td(r['method'] or ''),
            Td(r['status'].title()),
            Td(r['created_at'] or ''),
        )
    return Div(
        H1("Withdraw Funds", cls="mb-3"),
        Div(
            Card(title="Wallet Balance", content=f"₦{bal:,.2f}", card_cls="card mb-4"),
            cls=""
        ),
        Div(
            H4("Request Withdrawal", cls="mb-2"),
            Form(
                Div(Label("Amount", cls="form-label"), Input(type="number", name="amount", step="0.01", min="0", required=True, cls="form-control"), cls="mb-3"),
                Div(Label("Method", cls="form-label"), Input(type="text", name="method", placeholder="e.g. bank_transfer", cls="form-control"), cls="mb-3"),
                Div(Label("Account Details", cls="form-label"), Textarea(name="account", rows="2", placeholder="Bank name / Account name / Account number", cls="form-control"), cls="mb-3"),
                Div(Label("Notes (optional)", cls="form-label"), Textarea(name="notes", rows="2", cls="form-control"), cls="mb-3"),
                Button("Submit Request", type="submit", cls="btn btn-primary"),
                hx_post="/realtor/withdraw",
                hx_target="#main-content"
            ),
            cls="card p-3 mb-4"
        ),
        Div(
            H4("Withdrawal Requests", cls="mb-2"),
            Table(
                Thead(Tr(Th("S/N"), Th("Amount"), Th("Method"), Th("Status"), Th("Requested"))),
                Tbody(*(row_to_tr(i, r) for i, r in enumerate(requests)) if requests else Tr(Td("No requests", colspan="5", cls="text-center text-muted py-4"))),
                cls="table table-striped table-hover"
            ),
            cls="card p-3"
        ),
        cls="container-fluid"
    )

async def realtor_withdraw(request: Request):
    user = request.scope.get('user')
    if not user:
        return RedirectResponse(url="/login")
    if request.method == "GET":
        content = realtor_withdraw_content(user.id)
        # Flash toast
        flash = request.session.pop('flash', None) if hasattr(request, 'session') else None
        if flash and isinstance(flash, dict):
            content = Div(content, Script(f"showToast({(flash.get('message') or '')!r}, {(flash.get('level') or 'info')!r})"))
        return content if request.headers.get("HX-Request") else Layout(content, user_role="Realtor")
    # POST
    form = await request.form()
    try:
        amount = float(form.get('amount') or 0)
        method = form.get('method')
        account = form.get('account')
        notes = form.get('notes')
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        ensure_wallets_schema()
        create_withdraw_request(user.id, amount, method, account, notes)
        if hasattr(request, 'session'):
            request.session['flash'] = {'message': 'Withdrawal request submitted', 'level': 'success'}
    except Exception as e:
        if hasattr(request, 'session'):
            request.session['flash'] = {'message': f'Failed to submit request: {e}', 'level': 'danger'}
    return Response(headers={'HX-Redirect': '/realtor/withdraw'})

async def realtor_sales(request: Request):
    """Handle all sales-related routes"""
    return await realtor_sales_route_handler(request)
    