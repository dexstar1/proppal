from fasthtml.common import *
from components.card import Card
from components.layout import Layout
from starlette.requests import Request
from backend.src.models.property import Property
from typing import List, Optional, Union
from starlette.datastructures import UploadFile
import sqlite3
import os
import uuid

# --- Constants ---
FEATURES_LIST = [
    "Accessible Road", "Approved Government Excision", "Buy and build land", "Contract of Sales",
    "Deed of Assignment", "Dry Land", "Good title", "Instant Allocation", "Perimeter Fencing",
    "Survey", "24 Hour Water Supply", "24 Hours Security", "24/7 uninterrupted power supply",
    "Approved Gazette", "Balcony", "Basketball Court", "Beautiful Landscapes", "Building approval",
    "Central Business District", "Golf Course", "Good drainage system", "Government Allocation",
    "Governor's Consent", "Interlocked Road", "Interlocked Streets", "Tennis Court(s)", "Water treatment plant"
]
PROPERTY_TYPES = ["land", "house", "apartment"]
PROPERTY_STATUSES = ["for sale", "for rent", "invest", "lease", "sold"]
PROPERTY_LABELS = ["buy and build", "off-plan", "open house", "ready to move in", "sold out"]

# --- Page Content Components (Fully Implemented) ---

def admin_dashboard_content():
    # Compute real stats for admin overview
    # Properties count
    try:
        row = execute_db("SELECT COUNT(*) AS c FROM properties", fetchone=True)
        properties_count = int(row["c"]) if row else 0
    except Exception:
        properties_count = 0
    # Users subset for dashboard table
    latest_users = get_all_users_admin(limit=5)

    # Users count (all users)
    try:
        row_u = execute_db("SELECT COUNT(*) AS c FROM users", fetchone=True)
        users_count = int(row_u["c"]) if row_u else 0
    except Exception:
        users_count = 0

    # Sales stats and revenue
    try:
        from backend.src.api.admin_sales import get_all_sales, get_pending_sales_count, get_pending_payouts_count
        sales_rows = get_all_sales() or []
        total_sales = len(sales_rows)
        pending_sales = sum(1 for r in sales_rows if (r.get('status') if isinstance(r, dict) else r['status']) == 'pending')
        approved_sales = sum(1 for r in sales_rows if (r.get('status') if isinstance(r, dict) else r['status']) == 'approved')
        # total revenue from approved sales (amount column)
        total_revenue = sum(float((r.get('amount') if isinstance(r, dict) else r['amount']) or 0) for r in sales_rows if (r.get('status') if isinstance(r, dict) else r['status']) == 'approved')
        # Pending payouts (commissions) quick count (use API for schema safety)
        pending_payouts = int(get_pending_payouts_count())
    except Exception:
        total_sales = 0
        pending_sales = 0
        approved_sales = 0
        total_revenue = 0.0
        pending_payouts = 0

    # Pending withdrawal requests (site-wide)
    try:
        from backend.src.api.wallets import get_withdraw_requests
        wr = get_withdraw_requests() or []
        pending_withdraws = sum(1 for r in wr if (r.get('status') if isinstance(r, dict) else r['status']) == 'pending')
    except Exception:
        pending_withdraws = 0

    # Cards layout similar to realtor's dashboard (real data)
    users_table = Div(
        H4("Recent Users", cls="mt-4"),
        Table(
            Thead(Tr(Th("ID"), Th("First Name"), Th("Last Name"), Th("Email"), Th("Role"), Th("Verified"), Th("Status"))),
            Tbody(*(Tr(
                Td(str(u['id'])),
                Td((u['first_name'] or '') if 'first_name' in u.keys() else ''),
                Td((u['last_name'] or '') if 'last_name' in u.keys() else ''),
                Td(u['email'] or ''),
                Td(u['role'] or ''),
                Td('Yes' if u['is_verified'] else 'No'),
                Td((u['status'] or 'active').title())
            ) for u in latest_users) if latest_users else Tr(Td('No users', colspan='7', cls='text-center text-muted py-4'))),
            cls="table table-responsive table-sm table-hover"
        ),
        cls='table-responsive'
    )
    return Div(
        H6('Welcome, '),
        H1("Admin"),
        Div(
            Card(title="Total Properties", content=f"{properties_count}", card_cls="card mb-4 col-12 col-md-6 col-xl-3 shadow mx-2"),
            Card(title="Total Users", content=str(users_count), card_cls="card mb-4 col-12 col-md-6 col-xl-3 shadow mx-2"),
            Card(title="Total Sales", content=str(total_sales), card_cls="card mb-4 col-12 col-md-6 col-xl-3 shadow mx-2"),
            Card(title="Pending Sales", content=str(pending_sales), card_cls="card mb-4 col-12 col-md-6 col-xl-3 shadow mx-2"),
            Card(title="Approved Sales", content=str(approved_sales), card_cls="card mb-4 col-12 col-md-6 col-xl-3 shadow mx-2"),
            Card(title="Total Revenue", content=f"₦{total_revenue:,.2f}", card_cls="card mb-4 col-12 col-md-6 col-xl-3 shadow mx-2"),
            Card(title="Pending Payouts", content=str(pending_payouts), card_cls="card mb-4 col-12 col-md-6 col-xl-3 shadow mx-2"),
            Card(title="Pending Withdrawals", content=str(pending_withdraws), card_cls="card mb-4 col-12 col-md-6 col-xl-3 shadow mx-2"),
            cls="dashboard-content row"
        ),
        users_table,
        cls="container-fluid"
    )


def _safe_get(obj, *keys):
    """Return attribute or mapping value from obj for the first matching key name.
    Supports Pydantic models, sqlite3.Row, dicts.
    """
    for k in keys:
        try:
            if hasattr(obj, k):
                return getattr(obj, k)
        except Exception:
            pass
        try:
            return obj[k]  # type: ignore[index]
        except Exception:
            pass
    return None


def action_dropdown(prop):
    pid = _safe_get(prop, 'id')
    items = [
        Li(A('View', hx_get=f"/admin/properties/{pid}", hx_target="#main-content", cls='dropdown-item')),
        Li(A('Edit', hx_get=f"/admin/properties/{pid}/edit", hx_target="#main-content", cls='dropdown-item')),
        Li(A('Delete', hx_delete=f"/admin/properties/{pid}", hx_confirm="Are you sure?", hx_target="#main-content", cls='dropdown-item text-danger')),
    ]
    return Div(
        Button(cls='btn btn-sm btn-outline-secondary dropdown-toggle', data_bs_toggle='dropdown'),
        Ul(*items, cls='dropdown-menu'),
        cls='dropdown'
    )


def admin_properties_content():
    properties = get_all_properties()
    return Div(
        H1("Property Management"),
        Button("Add New Property", cls="btn btn-primary mb-4", hx_get="/admin/properties/new", hx_target="#main-content"),
        Table(
            Thead(Tr(Th("S/N"), Th("Image"), Th("Title"), Th("Location"), Th("Price"), Th("Action"))),
            Tbody(*[Tr(
                Td(f"{i + 1}"),
                Td(Img(src=(prop.images[0] if _safe_get(prop, 'images') else None), cls="img-thumbnail", style="max-width: 70px;") if _safe_get(prop, 'images') else "No Image"),
                Td(_safe_get(prop, 'name') or ''),
                Td(f"{_safe_get(prop, 'city') or ''}, {_safe_get(prop, 'state') or ''}"),
                Td(f"${float(_safe_get(prop, 'price') or 0):,.2f}"),
                Td(action_dropdown(prop))
            ) for i, prop in enumerate(properties)]),
            cls="table table-responsive table-striped"
        ),
        cls="container-fluid"
    )

def admin_property_detail_content(property_id: int):
    prop = get_property_by_id(property_id)
    if not prop:
        return Div(H1("Property Not Found"), cls="alert alert-danger")
    location_parts = [prop.address, prop.city, prop.state, prop.country, prop.zip_code]
    full_location = ", ".join(filter(None, location_parts))
    return Div(
        H1(prop.name),
        Div(
            Div(
                H4("Status & Labels"),
                P(f"Status: {prop.property_status or 'N/A'}"),
                P(f"Type: {prop.property_type or 'N/A'}"),
                P(f"Label: {prop.labels or 'N/A'}"),
                cls="mb-4"
            ),
            Div(
                H4("Details"),
                P(prop.description),
                P(f"Location: {full_location}"),
                P(f"Price: ${prop.price:,.2f}"),
                cls="mb-4"
            ),
            Div(
                H4("Room & Size Details"),
                P(f"Bedrooms: {prop.bedrooms or 'N/A'}"),
                P(f"Bathrooms: {prop.bathrooms or 'N/A'}"),
                P(f"Total Rooms: {prop.rooms or 'N/A'}"),
                P(f"Property Area: {prop.property_area_size or 'N/A'} sq. units"),
                P(f"Land Size: {prop.property_land_size or 'N/A'} sq. units"),
                P(f"Garages: {prop.garages or 'N/A'}"),
                P(f"Year Built: {prop.year_built or 'N/A'}"),
                cls="mb-4"
            ),
            Div(
                H4("Features"),
                P(", ".join(prop.features)) if prop.features else P("None"),
                cls="mb-4"
            ),
            Div(
                H4("Media"),
                A("View Virtual Tour", href=prop.virtual_tour_url, target="_blank") if prop.virtual_tour_url else P("No tour"),
                A("View Video", href=prop.video_url, target="_blank") if prop.video_url else P("No video"),
                cls="mb-4"
            ),
            Div(
                H4("Images"),
                *[Img(src=img, cls="img-thumbnail me-2 mb-2", style="max-width: 200px") for img in prop.images],
                cls="mb-4"
            ),
            Button("Back", cls="btn btn-secondary", hx_get="/admin/properties", hx_target="#main-content"),
        ),
        cls="container-fluid"
    )

def ensure_users_admin_schema():
    try:
        rows = execute_db("PRAGMA table_info(users)", fetchall=True)
        cols = {r[1] for r in rows} if rows else set()
        if 'status' not in cols:
            execute_db("ALTER TABLE users ADD COLUMN status TEXT", commit=True)
        if 'created_at' not in cols:
            execute_db("ALTER TABLE users ADD COLUMN created_at TEXT", commit=True)
        if 'first_name' not in cols:
            try: execute_db("ALTER TABLE users ADD COLUMN first_name TEXT", commit=True)
            except Exception: pass
        if 'last_name' not in cols:
            try: execute_db("ALTER TABLE users ADD COLUMN last_name TEXT", commit=True)
            except Exception: pass
    except Exception:
        pass


def get_all_users_admin(limit: int | None = None, offset: int | None = None, search: str | None = None, role: str | None = None, status: str | None = None, verified: str | None = None):
    ensure_users_admin_schema()
    where = []
    params = []
    if search and search.strip():
        where.append("(LOWER(email) LIKE ? OR LOWER(first_name) LIKE ? OR LOWER(last_name) LIKE ?)")
        sv = f"%{search.lower()}%"; params += [sv, sv, sv]
    if role in ('admin','realtor'):
        where.append("role = ?"); params.append(role)
    if status in ('active','suspended'):
        where.append("COALESCE(status,'active') = ?"); params.append(status)
    if verified in ('yes','no'):
        where.append("is_verified = ?"); params.append(1 if verified=='yes' else 0)
    where_sql = (" WHERE " + " AND ".join(where)) if where else ""
    q = "SELECT id, first_name, last_name, email, role, is_verified, COALESCE(status,'active') AS status, created_at FROM users" + where_sql + " ORDER BY id DESC"
    if limit is not None:
        q += " LIMIT ?"; params.append(int(limit))
    if offset is not None:
        q += " OFFSET ?"; params.append(int(offset))
    rows = execute_db(q, tuple(params), fetchall=True)
    return rows or []


def get_user_admin(user_id: int):
    ensure_users_admin_schema()
    row = execute_db("SELECT id, email, role, is_verified, COALESCE(status,'active') AS status, created_at FROM users WHERE id = ?", (user_id,), fetchone=True)
    return row


def admin_user_detail_content(user_id: int):
    u = get_user_admin(user_id)
    if not u:
        return Div(H1("User Not Found"), cls="alert alert-danger")
    return Div(
        H1(f"User #{u['id']}"),
        P(Strong("Email: "), Span(u['email'] or '')),
        P(Strong("Role: "), Span(u['role'] or '')),
        P(Strong("Verified: "), Span('Yes' if u['is_verified'] else 'No')),
        P(Strong("Status: "), Span((u['status'] or 'active').title(), cls=f"badge bg-{'success' if (u['status'] or 'active')=='active' else 'warning'}")),
        Button("Back", cls="btn btn-secondary", hx_get="/admin/users", hx_target="#main-content"),
        cls="container-fluid"
    )


def admin_user_edit_form(user_id: int):
    u = get_user_admin(user_id)
    if not u:
        return Div(H1("User Not Found"), cls="alert alert-danger")
    return Div(
        H1(f"Edit User #{u['id']}"),
        Form(
            Div(Label("Email", cls="form-label"), Input(name="email", value=u['email'] or '', readonly=True, cls="form-control"), cls="mb-3"),
            Div(Label("First Name", cls="form-label"), Input(name="first_name", value=(u['first_name'] or '') if 'first_name' in u.keys() else '', cls="form-control"), cls="mb-3"),
            Div(Label("Last Name", cls="form-label"), Input(name="last_name", value=(u['last_name'] or '') if 'last_name' in u.keys() else '', cls="form-control"), cls="mb-3"),
            Div(Label("Role", cls="form-label"), Select(
                Option("admin", value="admin", selected=(u['role']=='admin')),
                Option("realtor", value="realtor", selected=(u['role']=='realtor')),
                name="role", cls="form-select form-control"), cls="mb-3"),
            Div(Label("Verified", cls="form-label me-2"), Input(type="checkbox", name="is_verified", checked=bool(u['is_verified'])), cls="form-check form-switch mb-3"),
            Div(Label("Status", cls="form-label"), Select(
                Option("active", value="active", selected=((u['status'] or 'active')=='active')),
                Option("suspended", value="suspended", selected=((u['status'] or '')=='suspended')),
                name="status", cls="form-select form-control"), cls="mb-3"),
            Button("Save", type="submit", cls="btn btn-primary"),
            hx_put=f"/admin/users/{u['id']}", hx_target="#main-content"
        ),
        cls="container-fluid"
    )


def admin_users_content(search_q: str = '', role_f: str = 'all', status_f: str = 'all', verified_f: str = 'all', page: int = 1, per_page: int = 10):
    # Pagination & filters
    page = max(1, int(page or 1))
    per_page = max(1, int(per_page or 10))
    off = (page - 1) * per_page
    role = role_f if role_f in ('admin','realtor') else None
    status = status_f if status_f in ('active','suspended') else None
    verified = verified_f if verified_f in ('yes','no') else None
    rows = get_all_users_admin(limit=per_page, offset=off, search=(search_q or None), role=role, status=status, verified=verified)
    # total count for pagination
    ensure_users_admin_schema()
    where = []
    params = []
    if search_q and search_q.strip():
        where.append("(LOWER(email) LIKE ? OR LOWER(first_name) LIKE ? OR LOWER(last_name) LIKE ?)")
        sv = f"%{search_q.lower()}%"; params += [sv, sv, sv]
    if role:
        where.append("role = ?"); params.append(role)
    if status:
        where.append("COALESCE(status,'active') = ?"); params.append(status)
    if verified:
        where.append("is_verified = ?"); params.append(1 if verified=='yes' else 0)
    where_sql = (" WHERE " + " AND ".join(where)) if where else ""
    cnt_row = execute_db("SELECT COUNT(*) AS c FROM users" + where_sql, tuple(params), fetchone=True)
    total = int(cnt_row['c']) if cnt_row else 0
    total_pages = max(1, (total + per_page - 1) // per_page)

    def actions_cell(u):
        uid = u['id']
        suspended = (str(u['status'] or '').lower() == 'suspended')
        items = [
            Li(A('View', hx_get=f"/admin/users/{uid}", hx_target="#main-content", cls='dropdown-item')),
            Li(A('Edit', hx_get=f"/admin/users/{uid}/edit", hx_target="#main-content", cls='dropdown-item')),
            Li(A('Activate' if suspended else 'Suspend', hx_post=f"/admin/users/{uid}/suspend", hx_target="#main-content", cls='dropdown-item text-danger')),
        ]
        return Div(
            Button(cls='btn btn-sm btn-outline-secondary dropdown-toggle', data_bs_toggle='dropdown'),
            Ul(*items, cls='dropdown-menu'),
            cls='dropdown'
        )
    # Filters UI
    filters = Form(
        Div(
            Div(Label("Search", cls='form-label'), Input(type='search', name='q', value=search_q or '', cls='form-control'), cls='col-md-4'),
            Div(Label("Role", cls='form-label'), Select(
                Option('All', value='all', selected=(role_f=='all')),
                Option('Admin', value='admin', selected=(role_f=='admin')),
                Option('Realtor', value='realtor', selected=(role_f=='realtor')),
                name='role', cls='form-select form-control'), cls='col-md-2'),
            Div(Label("Status", cls='form-label'), Select(
                Option('All', value='all', selected=(status_f=='all')),
                Option('Active', value='active', selected=(status_f=='active')),
                Option('Suspended', value='suspended', selected=(status_f=='suspended')),
                name='status', cls='form-select form-control'), cls='col-md-2'),
            Div(Label("Verified", cls='form-label'), Select(
                Option('All', value='all', selected=(verified_f=='all')),
                Option('Yes', value='yes', selected=(verified_f=='yes')),
                Option('No', value='no', selected=(verified_f=='no')),
                name='verified', cls='form-select form-control'), cls='col-md-2'),
            Div(Label("Per Page", cls='form-label'), Select(
                Option('10', value='10', selected=(per_page==10)),
                Option('25', value='25', selected=(per_page==25)),
                Option('50', value='50', selected=(per_page==50)),
                name='per_page', cls='form-select form-control'), cls='col-md-2'),
            Div(Label(""), Button('Apply', cls='btn btn-primary w-100'), cls='col-md-3 my-3'),
            cls='row g-2'
        ),
        hx_get='/admin/users', hx_target='#main-content', cls='card p-4 mb-4'
    )

    table = Div(
        Table(
            Thead(Tr(Th("ID"), Th("First Name"), Th("Last Name"), Th("Email"), Th("Role"), Th("Verified"), Th("Status"), Th("Action"))),
            Tbody(*(Tr(
                Td(str(u['id'])),
                Td((u['first_name'] or '') if 'first_name' in u.keys() else ''),
                Td((u['last_name'] or '') if 'last_name' in u.keys() else ''),
                Td(u['email'] or ''),
                Td(u['role'] or ''),
                Td('Yes' if u['is_verified'] else 'No'),
                Td(Span((u['status'] or 'active').title(), cls=f"badge bg-{'success' if (u['status'] or 'active')=='active' else 'warning'}")),
                Td(actions_cell(u))
            ) for u in rows) if rows else Tr(Td('No users', colspan='8', cls='text-center text-muted py-4'))),
            cls="table table-responsive table-striped table-hover"
        ),
        cls='table-responsive my-4'
    )

    # Pagination controls
    def page_link(p):
        return A(str(p), hx_get=f"/admin/users?q={search_q}&role={role_f}&status={status_f}&verified={verified_f}&page={p}&per_page={per_page}", hx_target="#main-content", cls=f"page-link {'active' if p==page else ''}")
    nav = Nav(Ul(
        Li(A('Prev', hx_get=f"/admin/users?q={search_q}&role={role_f}&status={status_f}&verified={verified_f}&page={max(1,page-1)}&per_page={per_page}", hx_target="#main-content", cls=f"page-link {'disabled' if page<=1 else ''}"), cls='page-item'),
        *[Li(page_link(p), cls='page-item') for p in range(1, total_pages+1)],
        Li(A('Next', hx_get=f"/admin/users?q={search_q}&role={role_f}&status={status_f}&verified={verified_f}&page={min(total_pages,page+1)}&per_page={per_page}", hx_target="#main-content", cls=f"page-link {'disabled' if page>=total_pages else ''}"), cls='page-item'),
        cls='pagination'
    )) if total_pages>1 else Fragment()

    return Div(H1("User Management"), filters, table, nav, cls="container-fluid")

def admin_analytics_content():
    return Div(H1("Analytics Dashboard"), Div(Card(title="Monthly Revenue", content="Chart placeholder"), Card(title="User Growth", content="Chart placeholder")), cls="container-fluid")

def admin_payouts_content():
    return Div(H1("Payout Management"), Table(Thead(Tr(Th("ID"), Th("User"), Th("Amount"), Th("Status"), Th("Action"))), Tbody(Tr(Td("#P001"), Td("Jane Smith"), Td("$1,200"), Td("Pending"), Td(Button("Approve", cls="btn btn-sm btn-success")))), cls="table table-responsive table-striped"), cls="container-fluid")

# --- Page Route Functions ---

async def admin_dashboard(request: Request):
    content = admin_dashboard_content()
    return content if request.headers.get("HX-Request") else Layout(content, user_role="Admin")

async def admin_properties_route(request: Request):
    try:
        property_id = request.path_params.get('property_id')
        if request.method == "POST": return await handle_new_property(request)
        if request.method == "PUT" and property_id: return await handle_update_property(request, int(property_id))
        if request.method == "DELETE" and property_id: return await handle_delete_property(request, int(property_id))
        path = request.url.path
        if path.endswith("/new"): content = new_property_form()
        elif path.endswith("/edit") and property_id: content = edit_property_form(int(property_id))
        elif property_id: content = admin_property_detail_content(int(property_id))
        else: content = admin_properties_content()
        # Flash toast
        flash = request.session.pop('flash', None) if hasattr(request, 'session') else None
        if flash and isinstance(flash, dict):
            content = Div(content, Script(f"showToast({(flash.get('message') or '')!r}, {(flash.get('level') or 'info')!r})"))
        return content if request.headers.get("HX-Request") else Layout(content, user_role="Admin")
    except Exception as e:
        return Div(f"An error occurred: {e}", cls="alert alert-danger")

async def admin_users(request: Request):
    q = request.query_params.get('q', '')
    role = request.query_params.get('role', 'all')
    status = request.query_params.get('status', 'all')
    verified = request.query_params.get('verified', 'all')
    try: page = int(request.query_params.get('page', '1'))
    except: page = 1
    try: per_page = int(request.query_params.get('per_page', '10'))
    except: per_page = 10
    content = admin_users_content(q, role, status, verified, page, per_page)
    return content if request.headers.get("HX-Request") else Layout(content, user_role="Admin")

async def admin_analytics(request: Request):
    content = admin_analytics_content()
    return content if request.headers.get("HX-Request") else Layout(content, user_role="Admin")

async def admin_payouts(request: Request):
    content = admin_payouts_content()
    return content if request.headers.get("HX-Request") else Layout(content, user_role="Admin")

# --- User Handlers ---

async def admin_user_view(request: Request):
    uid = int(request.path_params.get('user_id'))
    content = admin_user_detail_content(uid)
    return content if request.headers.get("HX-Request") else Layout(content, user_role="Admin")

async def admin_user_edit(request: Request):
    uid = int(request.path_params.get('user_id'))
    content = admin_user_edit_form(uid)
    return content if request.headers.get("HX-Request") else Layout(content, user_role="Admin")

async def admin_user_update(request: Request):
    uid = int(request.path_params.get('user_id'))
    form = await request.form()
    first_name = (form.get('first_name') or '').strip()
    last_name = (form.get('last_name') or '').strip()
    role = form.get('role')
    is_verified = 1 if form.get('is_verified') in ['on','true','1'] else 0
    status = form.get('status')
    ensure_users_admin_schema()
    try:
        execute_db(
            "UPDATE users SET first_name = COALESCE(NULLIF(?, ''), first_name), last_name = COALESCE(NULLIF(?, ''), last_name), role = COALESCE(?, role), is_verified = COALESCE(?, is_verified), status = COALESCE(?, status) WHERE id = ?",
            (first_name, last_name, role, is_verified, status, uid), commit=True
        )
        if hasattr(request, 'session'):
            request.session['flash'] = {'message': 'User updated', 'level': 'success'}
    except Exception as e:
        if hasattr(request, 'session'):
            request.session['flash'] = {'message': f'Failed to update user: {e}', 'level': 'danger'}
    return Response(headers={'HX-Redirect': f'/admin/users/{uid}'})

async def admin_user_suspend(request: Request):
    uid = int(request.path_params.get('user_id'))
    ensure_users_admin_schema()
    u = get_user_admin(uid)
    new_status = 'active' if u and (u['status'] or 'active') == 'suspended' else 'suspended'
    try:
        execute_db("UPDATE users SET status = ? WHERE id = ?", (new_status, uid), commit=True)
        if hasattr(request, 'session'):
            request.session['flash'] = {'message': f'User status set to {new_status}', 'level': 'success'}
    except Exception as e:
        if hasattr(request, 'session'):
            request.session['flash'] = {'message': f'Failed to update status: {e}', 'level': 'danger'}
    return Response(headers={'HX-Redirect': '/admin/users'})

# --- Form Handlers (FIXED & EXPLICIT) ---

async def handle_new_property(request: Request):
    form = await request.form()
    try:
        images_str = await _save_uploaded_images(form)
        features_str = ",".join(form.getlist("features"))
        
        # Explicitly get, clean, and type-cast all values
        conn = sqlite3.connect('proppal.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO properties (name, description, price, images, realtor_id, features, address, country, state, city, area, zip_code, latitude, longitude, virtual_tour_url, property_type, property_status, labels, video_url, bedrooms, bathrooms, rooms, property_area_size, property_land_size, garages, year_built)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            form.get('name'), form.get('description'),
            float(form.get('price')) if form.get('price') else None,
            images_str, 1, features_str,
            form.get('address'), form.get('country'), form.get('state'), form.get('city'), form.get('area'), form.get('zip_code'),
            float(form.get('latitude')) if form.get('latitude') else None,
            float(form.get('longitude')) if form.get('longitude') else None,
            form.get('virtual_tour_url'), form.get('property_type'), form.get('property_status'), form.get('labels'), form.get('video_url'),
            int(form.get('bedrooms')) if form.get('bedrooms') else None,
            int(form.get('bathrooms')) if form.get('bathrooms') else None,
            int(form.get('rooms')) if form.get('rooms') else None,
            float(form.get('property_area_size')) if form.get('property_area_size') else None,
            float(form.get('property_land_size')) if form.get('property_land_size') else None,
            int(form.get('garages')) if form.get('garages') else None,
            int(form.get('year_built')) if form.get('year_built') else None
        ))
        conn.commit()
        conn.close()
        if hasattr(request, 'session'):
            request.session['flash'] = {'message': 'Property created successfully', 'level': 'success'}
        return Response(headers={'HX-Redirect': '/admin/properties'})
    except Exception as e:
        if hasattr(request, 'session'):
            request.session['flash'] = {'message': f'Error creating property: {e}', 'level': 'danger'}
        return Response(headers={'HX-Redirect': '/admin/properties'})

async def handle_update_property(request: Request, property_id: int):
    form = await request.form()
    try:
        new_images_str = await _save_uploaded_images(form)
        images_str = new_images_str if new_images_str else form.get("existing_images", "")
        features_str = ",".join(form.getlist("features"))

        conn = sqlite3.connect('proppal.db')
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE properties SET 
            name=?, description=?, price=?, images=?, features=?, address=?, country=?, state=?, city=?, area=?, zip_code=?, 
            latitude=?, longitude=?, virtual_tour_url=?, property_type=?, property_status=?, labels=?, video_url=?, 
            bedrooms=?, bathrooms=?, rooms=?, property_area_size=?, property_land_size=?, garages=?, year_built=?
            WHERE id=?
        """, (
            form.get('name'), form.get('description'),
            float(form.get('price')) if form.get('price') else None,
            images_str, features_str,
            form.get('address'), form.get('country'), form.get('state'), form.get('city'), form.get('area'), form.get('zip_code'),
            float(form.get('latitude')) if form.get('latitude') else None,
            float(form.get('longitude')) if form.get('longitude') else None,
            form.get('virtual_tour_url'), form.get('property_type'), form.get('property_status'), form.get('labels'), form.get('video_url'),
            int(form.get('bedrooms')) if form.get('bedrooms') else None,
            int(form.get('bathrooms')) if form.get('bathrooms') else None,
            int(form.get('rooms')) if form.get('rooms') else None,
            float(form.get('property_area_size')) if form.get('property_area_size') else None,
            float(form.get('property_land_size')) if form.get('property_land_size') else None,
            int(form.get('garages')) if form.get('garages') else None,
            int(form.get('year_built')) if form.get('year_built') else None,
            property_id
        ))
        conn.commit()
        conn.close()
        if hasattr(request, 'session'):
            request.session['flash'] = {'message': 'Property updated successfully', 'level': 'success'}
        return Response(headers={'HX-Redirect': '/admin/properties'})
    except Exception as e:
        if hasattr(request, 'session'):
            request.session['flash'] = {'message': f'Error updating property: {e}', 'level': 'danger'}
        return Response(headers={'HX-Redirect': '/admin/properties'})

async def handle_delete_property(request: Request, property_id: int):
    delete_property(property_id)
    if hasattr(request, 'session'):
        request.session['flash'] = {'message': 'Property deleted', 'level': 'success'}
    return Response(headers={'HX-Redirect': '/admin/properties'})

# --- DB & Helpers (Complete) ---

async def _save_uploaded_images(form) -> str:
    image_files = form.getlist("images")
    saved_image_paths = []
    if image_files and isinstance(image_files[0], UploadFile) and image_files[0].filename:
        UPLOAD_DIR = "public/assets/img/properties"
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        for image_file in image_files:
            if isinstance(image_file, UploadFile) and image_file.filename:
                ext = os.path.splitext(image_file.filename)[1]
                unique_filename = f"{uuid.uuid4()}{ext}"
                save_path = os.path.join(UPLOAD_DIR, unique_filename)
                with open(save_path, "wb") as buffer:
                    buffer.write(await image_file.read())
                saved_image_paths.append(f"/assets/img/properties/{unique_filename}")
    return ",".join(saved_image_paths)

def execute_db(query, params=(), fetchone=False, fetchall=False, commit=False):
    conn = sqlite3.connect('proppal.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = None
    if fetchone: result = cursor.fetchone()
    if fetchall: result = cursor.fetchall()
    if commit: conn.commit()
    conn.close()
    return result

def delete_property(property_id: int):
    execute_db("DELETE FROM properties WHERE id = ?", (property_id,), commit=True)

def get_all_properties() -> List[Property]:
    rows = execute_db("SELECT * FROM properties ORDER BY id DESC", fetchall=True)
    return [_parse_property_from_row(row) for row in rows if row]

def get_property_by_id(property_id: int) -> Optional[Property]:
    row = execute_db("SELECT * FROM properties WHERE id = ?", (property_id,), fetchone=True)
    return _parse_property_from_row(row) if row else None

def _parse_property_from_row(row) -> Property:
    prop_dict = dict(row)
    for key in ['images', 'features']:
        val = prop_dict.get(key)
        prop_dict[key] = val.split(',') if val and val.strip() else []
    if prop_dict.get('realtor_id') is None: prop_dict['realtor_id'] = 1

    numeric_fields = [
        'latitude', 'longitude', 'price', 'property_area_size', 'property_land_size',
        'bedrooms', 'bathrooms', 'rooms', 'garages', 'year_built'
    ]
    for field in numeric_fields:
        if prop_dict.get(field) == '' or prop_dict.get(field) is None:
            prop_dict[field] = None

    return Property(**prop_dict)

# --- Form Components (Complete) ---

def _build_select(name, options, selected, required=False):
    return Div(Label(name.replace('_', ' ').title(), cls="form-label"), Select(Option(value="", children="-- Select --"), *[Option(o, value=o, selected=(o == selected)) for o in options], name=name, cls="form-select form-control", required=required), cls="mb-3")

def _build_feature_checkboxes(selected_features):
    return [Div(Input(type="checkbox", name="features", value=feature, id=f"feature_{feature.replace(' ', '_')}", cls="form-check-input", checked=feature in selected_features), Label(feature, for_=f"feature_{feature.replace(' ', '_')}", cls="form-check-label"), cls="form-check form-check-inline") for feature in FEATURES_LIST]

def new_property_form():
    return Div(H2("Add New Property"), Form(_property_form_fields(), hx_post="/admin/properties", hx_target="#main-content", enctype="multipart/form-data", cls="mt-4"))

def edit_property_form(property_id: int):
    prop = get_property_by_id(property_id)
    if not prop: return Div("Property not found")
    return Div(H2("Edit Property"), Form(_property_form_fields(prop), hx_put=f"/admin/properties/{property_id}", hx_target="#main-content", enctype="multipart/form-data", cls="mt-4"))

def _property_form_fields(prop: Optional[Property] = None):
    return Fragment(
        Div(Label("Name", cls="form-label"), Input(name="name", value=prop.name if prop else "", cls="form-control", required=True), cls="mb-3"),
        Div(Label("Description", cls="form-label"), Textarea(prop.description if prop else "", name="description", cls="form-control"), cls="mb-3"),
        Div(Label("Price", cls="form-label"), Input(type="number", name="price", value=prop.price if prop else "", cls="form-control", required=True, step="any"), cls="mb-3"),
        H4("Classification", cls="mt-4"),
        Div(
            Div(_build_select("property_type", PROPERTY_TYPES, prop.property_type if prop else None, required=True), cls="col-md-4"),
            Div(_build_select("property_status", PROPERTY_STATUSES, prop.property_status if prop else None, required=True), cls="col-md-4"),
            Div(_build_select("labels", PROPERTY_LABELS, prop.labels if prop else None, required=True), cls="col-md-4"),
            cls="row mb-3"
        ),
        H4("Features", cls="mt-4"),
        Div(*_build_feature_checkboxes(prop.features if prop else []), cls="d-flex flex-wrap mb-3 border rounded p-2"),
        H4("Location", cls="mt-4"),
        Div(Label("Address", cls="form-label"), Input(name="address", value=prop.address if prop else "", cls="form-control"), cls="mb-3"),
        Div(
            Div(Label("Country", cls="form-label"), Input(name="country", value=prop.country if prop else "", cls="form-control"), cls="col-md-6"),
            Div(Label("State", cls="form-label"), Input(name="state", value=prop.state if prop else "", cls="form-control"), cls="col-md-6"),
            cls="row mb-3"
        ),
        Div(
            Div(Label("City", cls="form-label"), Input(name="city", value=prop.city if prop else "", cls="form-control"), cls="col-md-4"),
            Div(Label("Area", cls="form-label"), Input(name="area", value=prop.area if prop else "", cls="form-control"), cls="col-md-4"),
            Div(Label("Zip Code", cls="form-label"), Input(name="zip_code", value=prop.zip_code if prop else "", cls="form-control"), cls="col-md-4"),
            cls="row mb-3"
        ),
        H4("Map", cls="mt-4"),
        Div(
            Div(Label("Latitude", cls="form-label"), Input(type="number", name="latitude", step="any", value=prop.latitude if prop else "", cls="form-control"), cls="col-md-6"),
            Div(Label("Longitude", cls="form-label"), Input(type="number", name="longitude", step="any", value=prop.longitude if prop else "", cls="form-control"), cls="col-md-6"),
            cls="row mb-3"
        ),
        H4("Details", cls="mt-4"),
        Div(
            Div(Label("Bedrooms", cls="form-label"), Input(type="number", name="bedrooms", value=prop.bedrooms if prop else "", cls="form-control"), cls="col-md-3"),
            Div(Label("Bathrooms", cls="form-label"), Input(type="number", name="bathrooms", value=prop.bathrooms if prop else "", cls="form-control"), cls="col-md-3"),
            Div(Label("Rooms", cls="form-label"), Input(type="number", name="rooms", value=prop.rooms if prop else "", cls="form-control"), cls="col-md-3"),
            Div(Label("Garages", cls="form-label"), Input(type="number", name="garages", value=prop.garages if prop else "", cls="form-control"), cls="col-md-3"),
            cls="row mb-3"
        ),
        Div(
            Div(Label("Property Area Size", cls="form-label"), Input(type="number", name="property_area_size", step="any", value=prop.property_area_size if prop else "", cls="form-control"), cls="col-md-4"),
            Div(Label("Land Size", cls="form-label"), Input(type="number", name="property_land_size", step="any", value=prop.property_land_size if prop else "", cls="form-control"), cls="col-md-4"),
            Div(Label("Year Built", cls="form-label"), Input(type="number", name="year_built", value=prop.year_built if prop else "", cls="form-control"), cls="col-md-4"),
            cls="row mb-3"
        ),
        H4("Media", cls="mt-4"),
        Div(Label("Video URL", cls="form-label"), Input(type="text", name="video_url", value=prop.video_url if prop else "", cls="form-control"), cls="mb-3"),
        Div(Label("360 Virtual Tour URL", cls="form-label"), Input(type="text", name="virtual_tour_url", value=prop.virtual_tour_url if prop else "", cls="form-control"), cls="mb-3"),
        (Div(H4("Current Images"), *[Img(src=img, cls="img-thumbnail me-2 mb-2", style="max-width: 100px") for img in prop.images], cls="mb-3") if prop and prop.images else Div()),
        Div(Label("Upload Images", cls="form-label"), Input(type="file", name="images", multiple=True, cls="form-control"), cls="mb-3"),
        (Input(type="hidden", name="existing_images", value=",".join(prop.images)) if prop else Div()),
        Button("Save Property" if not prop else "Update Property", type="submit", cls="btn btn-primary mt-4")
    )