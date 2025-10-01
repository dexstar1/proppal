from fasthtml.common import *
from components.card import Card
from components.layout import Layout
from starlette.requests import Request
from routes.realtor_sales import realtor_sales_route_handler
from backend.src.models.property import Property
from typing import List, Optional, Any
from routes.admin import execute_db, _parse_property_from_row
from backend.src.api.admin_sales import get_all_sales
from backend.src.api.wallets import get_withdraw_requests_by_realtor

from backend.src.api.wallets import get_wallet_balance

from backend.src.api.admin_sales import get_commissions_by_realtor, get_all_sales
from backend.src.api.wallets import get_withdraw_requests_by_realtor
import math

def realtor_dashboard_content(user_role: str = "Realtor", wallet_balance: float = 0.0, commissions: list = None, stats: dict | None = None, withdraws: list | None = None, display_name: str | None = None, referral_code: str | None = None):
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
        H1(f"{user_role} - {display_name}") if display_name else H1(user_role),
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
                        Card(
                        title="My Referral Code",
                        content=Div(
                            Div(Strong(referral_code or '—', id='my-ref-code-dashboard'), cls='me-3 d-inline'),
                            A('Copy Code', cls='badge badge-secondary me-2', onclick="navigator.clipboard.writeText(document.getElementById('my-ref-code-dashboard').innerText).then(()=>{this.innerText='Copied'; setTimeout(()=>this.innerText='Copy Code',1200)})"),
                            A('Copy Link', cls='badge badge-primary', onclick="(()=>{const c=document.getElementById('my-ref-code-dashboard').innerText||'';const link=`${location.origin}/register?ref=${c}`;navigator.clipboard.writeText(link).then(()=>{this.innerText='Link Copied'; setTimeout(()=>this.innerText='Copy Link',1200)})})()"),
                            cls='d-flex align-items-center'
                        ),
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

    # Ensure referral stats
    try:
        from backend.src.api.referrals import get_or_create_referral_code, get_downlines, ensure_referrals_schema
        ensure_referrals_schema()
        ref_code = get_or_create_referral_code(int(user.id)) if user else None
        downs = get_downlines(int(user.id)) if user else []
        referrals_count = len(downs or [])
    except Exception:
        ref_code = None
        referrals_count = 0

    stats = {
        'referrals_count': referrals_count,
        'transactions_count': total_sales,
        'total_sales': total_sales,
        'pending_sales': pending_sales,
        'approved_sales': approved_sales,
        'total_withdrawn': total_withdrawn,
        'total_commission_amount': total_commission_amount,
    }

    # Prefer first + last name captured during account verification; fallback to email-derived name
    if user:
        first = getattr(user, 'first_name', None) or getattr(user, 'firstname', None)
        last = getattr(user, 'last_name', None) or getattr(user, 'lastname', None)
        name = f"{(first or '').strip()} {(last or '').strip()}".strip()
        disp = name or _display_name_from_email(getattr(user, 'email', ''))
    else:
        disp = None
    if request.headers.get("HX-Request"):
        return realtor_dashboard_content(wallet_balance=bal, commissions=comms, stats=stats, withdraws=my_withdraws, display_name=disp, referral_code=ref_code)
    return Layout(realtor_dashboard_content(wallet_balance=bal, commissions=comms, stats=stats, withdraws=my_withdraws, display_name=disp, referral_code=ref_code), user_role="Realtor", user_display=disp)

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
            Thead(Tr(Th("S/N"), Th("Image"), Th("Title"), Th("Location"), Th("Price"), Th("Action"))),
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

def _display_name_from_email(email: str) -> str:
    try:
        local = (email or '').split('@', 1)[0]
        first = re.split(r'[._-]+', local)[0]
        return first.capitalize() if first else email
    except Exception:
        return email


def realtor_properties(request: Request):
    if request.headers.get("HX-Request"):
        return realtor_properties_content(request)
    user = request.scope.get('user')
    disp = _display_name_from_email(getattr(user, 'email', '')) if user else None
    return Layout(realtor_properties_content(request), user_role="Realtor", user_display=disp)

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
    from backend.src.api.referrals import get_downlines, referrals_histogram_by_month, ensure_referrals_schema, get_or_create_referral_code
    def histo_bar(label: str, val: int, maxv: int):
        width = 0 if maxv <= 0 else int((val / maxv) * 100)
        return Tr(Td(label), Td(val), Td(Div(style=f"height:10px;background:#0d6efd;width:{width}%;")))
    # We will fetch in the route where user exists; here just structure
    return Div(
        H1("My Referrals"),
        Div(id='referrals-summary'),
        Div(id='referrals-histogram'),
        cls="container-fluid"
    )

def realtor_referrals(request: Request):
    user = request.scope.get('user')
    if not user:
        return RedirectResponse(url="/login")
    try:
        from backend.src.api.referrals import get_downlines, referrals_histogram_by_month, ensure_referrals_schema, get_or_create_referral_code
        ensure_referrals_schema()
        code = get_or_create_referral_code(int(user.id))
        downs = get_downlines(int(user.id)) or []
        hist = referrals_histogram_by_month(int(user.id)) or []
    except Exception:
        code = None; downs = []; hist = []

    maxc = max((c for _, c in hist), default=0)
    def bar_row(label: str, val: int):
        width = 0 if maxc <= 0 else int((val / maxc) * 100)
        return Tr(Td(label), Td(str(val)), Td(Div(style=f"height:10px;background:#0d6efd;width:{width}%;")))

    table = Div(
        H4("Referral Signups by Month"),
        Table(
            Thead(Tr(Th("Month"), Th("Signups"), Th(""))),
            Tbody(*(bar_row(m, c) for m, c in hist) if hist else Tr(Td("No referrals yet", colspan="3", cls="text-center text-muted py-4"))),
            cls="table table-sm"
        )
    )
    summary = Div(
        Div(
            Strong("Your Referral Code: "),
            Span(code or '—', id='my-ref-code'),
            Button('Copy Code', cls='badge badge-secondary ms-2', onclick="navigator.clipboard.writeText(document.getElementById('my-ref-code').innerText).then(()=>{this.innerText='Copied'; setTimeout(()=>this.innerText='Copy Code',1200)})"),
            Button('Copy Link', cls='badge badge-primary ms-2', onclick="(()=>{const c=document.getElementById('my-ref-code').innerText||'';const link=`${location.origin}/register?ref=${c}`;navigator.clipboard.writeText(link).then(()=>{this.innerText='Link Copied'; setTimeout(()=>this.innerText='Copy Link',1200)})})()")
        ),
        P(f"Total downlines: {len(downs)}"),
        cls='mb-3'
    )
    # Downlines table
    def down_row(r):
        em = r['email'] if isinstance(r, dict) else r['email']
        created = (r.get('created_at') if isinstance(r, dict) else r['created_at']) or ''
        referred = (r.get('referred_at') if isinstance(r, dict) else r['referred_at']) or ''
        return Tr(Td(em), Td(created), Td(referred))
    downlines_table = Div(
        H4("Downlines"),
        Table(
            Thead(Tr(Th('Email'), Th('Joined'), Th('Referred At'))),
            Tbody(*(down_row(dict(d) if not isinstance(d, dict) else d) for d in downs) if downs else Tr(Td('No downlines yet', colspan='3', cls='text-center text-muted py-4'))),
            cls='table table-sm'
        )
    )
    content = Div(H1("My Referrals"), summary, table, downlines_table, cls="container-fluid")
    if request.headers.get("HX-Request"):
        return content
    return Layout(content, user_role="Realtor")


def realtor_transactions_content(user_id: int, type_filter: str = 'all', status_filter: str = 'all'):
    # Gather sales and withdrawal transactions for this realtor
    try:
        sales_rows = get_all_sales() or []
        my_sales = [dict(r) if not isinstance(r, dict) else r for r in sales_rows if (r.get('realtor_id') if isinstance(r, dict) else r['realtor_id']) == user_id]
    except Exception:
        my_sales = []
    try:
        withdraws = get_withdraw_requests_by_realtor(user_id) or []
        my_withdraws = [dict(w) if not isinstance(w, dict) else w for w in withdraws]
    except Exception:
        my_withdraws = []

    # Normalize into a unified list for display
    events = []
    for s in my_sales:
        events.append({
            'type': 'Sale',
            'ref': f"Sale #{s.get('id')}",
            'amount': float(s.get('amount') or 0),
            'status': (s.get('status') or '').title(),
            'date': s.get('created_at') or '',
            'link': f"/realtor/sales/{s.get('id')}"
        })
    for w in my_withdraws:
        events.append({
            'type': 'Withdrawal',
            'ref': f"WR#{w.get('id')}",
            'amount': float(w.get('amount') or 0),
            'status': (w.get('status') or '').title(),
            'date': w.get('created_at') or '',
            'link': '/realtor/withdraw'
        })

    # Apply filters
    tf = (type_filter or 'all').lower()
    sf = (status_filter or 'all').lower()
    if tf in ('sale', 'sales', 'withdrawal', 'withdrawals'):
        want = 'Sale' if tf.startswith('sale') else 'Withdrawal'
        events = [e for e in events if e['type'] == want]
    if sf in ('pending', 'approved', 'rejected', 'paid', 'success', 'failed', 'cancelled', 'in_progress', 'processing'):
        events = [e for e in events if e['status'].lower() == sf]

    # Sort by date desc (ISO strings sort correctly)
    events.sort(key=lambda e: e.get('date') or '', reverse=True)

    def row(e):
        return Tr(
            Td(e['type']),
            Td(e['ref']),
            Td(f"₦{e['amount']:,.2f}"),
            Td(Span(e['status'], cls=f"badge bg-{'success' if e['status'].lower() in ('approved','paid','success') else 'warning' if e['status'].lower() in ('pending','in_progress','processing') else 'danger'}")),
            Td(e['date']),
            Td(A('Open', hx_get=e['link'], hx_target='#main-content', cls='btn btn-sm btn-outline-primary'))
        )

    # Filter controls
    def filter_badge(label, tval, sval, active):
        return A(
            label,
            hx_get=f"/realtor/transactions?type={tval}&status={sval}",
            hx_target="#main-content",
            cls=f"badge me-2 {'badge-dark' if active else 'badge-secondary'}"
        )

    type_all = filter_badge('All', 'all', sf, tf == 'all')
    type_sales = filter_badge('Sales', 'sales', sf, tf.startswith('sale'))
    type_withdrawals = filter_badge('Withdrawals', 'withdrawals', sf, tf.startswith('withdraw'))

    status_all = filter_badge('All Status', tf, 'all', sf == 'all')
    status_pending = filter_badge('Pending', tf, 'pending', sf == 'pending')
    status_approved = filter_badge('Approved', tf, 'approved', sf == 'approved')
    status_rejected = filter_badge('Rejected', tf, 'rejected', sf == 'rejected')

    controls = Div(
        Div(type_all, type_sales, type_withdrawals, cls='mb-2'),
        Div(status_all, status_pending, status_approved, status_rejected, cls='mb-3'),
        cls='d-flex flex-column'
    )

    table = Div(
        Table(
            Thead(Tr(Th('Type'), Th('Reference'), Th('Amount'), Th('Status'), Th('Date'), Th(''))),
            Tbody(*(row(e) for e in events) if events else Tr(Td('No transactions', colspan='6', cls='text-center text-muted py-4'))),
            cls='table table-striped table-hover'
        ),
        cls='table-responsive'
    )
    return Div(H1('My Transactions', cls='mb-3'), controls, table, cls='container-fluid')


def realtor_transactions(request: Request):
    user = request.scope.get('user')
    if not user:
        return RedirectResponse(url="/login")
    tfilter = request.query_params.get('type', 'all')
    sfilter = request.query_params.get('status', 'all')
    content = realtor_transactions_content(user.id, tfilter, sfilter)
    # Flash toast
    flash = request.session.pop('flash', None) if hasattr(request, 'session') else None
    if flash and isinstance(flash, dict):
        content = Div(content, Script(f"showToast({(flash.get('message') or '')!r}, {(flash.get('level') or 'info')!r})"))
    if request.headers.get("HX-Request"):
        return content
    # Keep the display name logic consistent with dashboard
    first = getattr(user, 'first_name', None) or getattr(user, 'firstname', None)
    last = getattr(user, 'last_name', None) or getattr(user, 'lastname', None)
    name = f"{(first or '').strip()} {(last or '').strip()}".strip()
    disp = name or _display_name_from_email(getattr(user, 'email', ''))
    return Layout(content, user_role='Realtor', user_display=disp)

def realtor_commissions_content(user_id: int):
    rows = get_commissions_by_realtor(user_id)

    # Pagination
    per_page = 10
    page = 1
    total = len(rows)
    total_pages = max(1, math.ceil(total / per_page))
    start = 0
    page_rows = rows[start:start+per_page]

    def badge_cls(status: str) -> str:
        status = (status or '').lower()
        if status in ('approved', 'paid', 'success'):
            return 'badge bg-success'
        if status in ('pending', 'in_progress', 'processing'):
            return 'badge bg-warning'
        if status in ('rejected', 'failed', 'cancelled', 'error'):
            return 'badge bg-danger'
        return 'badge bg-secondary'

    def row_to_tr(c):
        return Tr(
            Td(f"Sale #{c['sale_id']}"),
            Td(f"₦{float(c['amount']):,.2f}"),
            Td(Span(c['status'].title(), cls=badge_cls(c['status']))),
            Td(c['created_at'] or ''),
        )
    table = Div(
        Table(
            Thead(Tr(Th("Sale"), Th("Amount"), Th("Status"), Th("Created"))),
            Tbody(*(row_to_tr(c) for c in page_rows) if page_rows else Tr(Td("No commissions", colspan="4", cls="text-center text-muted py-4"))),
            cls="table table-striped table-hover"
        ),
        cls="table-responsive"
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
    user = request.scope.get('user')
    disp = _display_name_from_email(getattr(user, 'email', '')) if user else None
    return Layout(content, user_role="Realtor", user_display=disp)

from backend.src.api.wallets import ensure_wallets_schema, create_withdraw_request, get_withdraw_requests_by_realtor

def realtor_withdraw_content(user_id: int):
    bal = get_wallet_balance(user_id)
    requests = get_withdraw_requests_by_realtor(user_id)

    # Pagination
    per_page = 10
    page = 1
    total = len(requests)
    total_pages = max(1, math.ceil(total / per_page))
    start = 0
    page_rows = requests[start:start+per_page]

    def badge_cls(status: str) -> str:
        status = (status or '').lower()
        if status in ('approved', 'paid', 'success'):
            return 'badge bg-success'
        if status in ('pending', 'in_progress', 'processing'):
            return 'badge bg-warning'
        if status in ('rejected', 'failed', 'cancelled', 'error'):
            return 'badge bg-danger'
        return 'badge bg-secondary'

    def row_to_tr(idx, r):
        return Tr(
            Td(str(start + idx + 1)),
            Td(f"₦{float(r['amount']):,.2f}"),
            Td(Span((r['status'] or '').title(), cls=badge_cls(r['status']))),
            Td(r['created_at'] or ''),
        )
    return Div(
            H1("Withdraw Funds", cls="mb-3"),
            Div(
                Div(
                Card(title="Wallet Balance", content=f"₦{bal:,.2f}", card_cls="card mb-4"),
                cls="col-12 col-md-6 col-xl-6"
                ),
                Div(
                    H6("Request Withdrawal", cls="mb-2"),
                    Form(
                        Div(Label("Amount", cls="form-label"), Input(type="number", name="amount", step="0.01", min="0", required=True, cls="form-control"), cls="mb-3"),
                        Button("Submit Request", type="submit", cls="btn btn-primary"),
                        hx_post="/realtor/withdraw",
                        hx_target="#main-content"
                    ),
                    cls="card p-3 mb-4 col-12 col-md-6 col-xl-6"
                ), 
                cls="row"
            ),
        Div(
            H4("Withdrawal Requests", cls="mb-2"),
            Div(
                Table(
                    Thead(Tr(Th("S/N"), Th("Amount"), Th("Status"), Th("Requested"))),
                    Tbody(*(row_to_tr(i, r) for i, r in enumerate(page_rows)) if page_rows else Tr(Td("No requests", colspan="5", cls="text-center text-muted py-4"))),
                    cls="table table-striped table-hover"
                ),
                cls="table-responsive"
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
        user = request.scope.get('user')
        disp = _display_name_from_email(getattr(user, 'email', '')) if user else None
        return content if request.headers.get("HX-Request") else Layout(content, user_role="Realtor", user_display=disp)
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
    