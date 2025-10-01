from fasthtml.common import *
from components.layout import Layout
from components.card import Card
from starlette.requests import Request
from starlette.responses import RedirectResponse
from backend.src.api.admin_sales import (
    get_all_sales, get_sale_by_id,
    approve_sale_and_create_payout, reject_sale,
    get_payouts, mark_payout_paid,
    ensure_admin_sales_schema,
    get_pending_sales_count, get_pending_payouts_count
)
import math

DEFAULT_COMMISSION_RATE = 0.10  # 10%


def _require_admin(request: Request):
    user = request.scope.get('user')
    if not user:
        return None, RedirectResponse(url="/login")
    # Optional: enforce role if available in user
    # if getattr(user, 'role', None) != 'admin':
    #     return None, Div("Unauthorized", cls="alert alert-danger")
    return user, None


# Sales listing and details
async def admin_sales_list(request: Request):
    user, redirect = _require_admin(request)
    if redirect: return redirect
    ensure_admin_sales_schema()
    rows = get_all_sales()

    # Pagination
    per_page = 10
    try:
        page = int(request.query_params.get('page', '1'))
    except Exception:
        page = 1
    total = len(rows)
    total_pages = max(1, math.ceil(total / per_page))
    page = max(1, min(page, total_pages))
    start = (page - 1) * per_page
    page_rows = rows[start:start+per_page]

    # Flash messages via session (preferred)
    toast_script = None
    flash = request.session.pop('flash', None) if hasattr(request, 'session') else None
    if flash and isinstance(flash, dict):
        msg = flash.get('message') or ''
        level = flash.get('level') or 'info'
        toast_script = Script(f"showToast({msg!r}, {level!r})")
    else:
        # Backward compat: fallback to query param
        toast = request.query_params.get('toast')
        if toast == 'approved':
            toast_script = Script("showToast('Sale approved and payout created', 'success')")
        elif toast == 'rejected':
            toast_script = Script("showToast('Sale rejected', 'success')")
        elif toast == 'error':
            toast_script = Script("showToast('Operation failed', 'danger')")

    # Badge class mapping for statuses
    def badge_cls(status: str) -> str:
        status = (status or '').lower()
        if status in ('approved', 'paid', 'success'):
            return 'badge bg-success'
        if status in ('pending', 'in_progress', 'processing'):
            return 'badge bg-warning'
        if status in ('rejected', 'failed', 'cancelled', 'error'):
            return 'badge bg-danger'
        return 'badge bg-secondary'

    def action_dropdown(s):
        items = []
        items.append(Li(A('View', hx_get=f"/admin/sales/{s['id']}", hx_target="#main-content", cls='dropdown-item')))
        if s['status'] == 'pending':
            items.append(Li(A('Approve', hx_post=f"/admin/sales/{s['id']}/approve", hx_target="#main-content", cls='dropdown-item')))
            items.append(Li(A('Reject', hx_post=f"/admin/sales/{s['id']}/reject", hx_target="#main-content", hx_confirm='Reject this sale?', cls='dropdown-item')))
        return Div(
            Button(cls='btn btn-sm btn-outline-secondary dropdown-toggle', data_bs_toggle='dropdown'),
            Ul(*items, cls='dropdown-menu'),
            cls='dropdown'
        )

    def row_to_tr(idx, s):
        return Tr(
            Td(str(start + idx + 1)),
            Td(s["property_name"] or f"Property {s['property_id']}") ,
            Td(f"{s['client_first_name']} {s['client_last_name']}") ,
            Td(f"₦{float(s['amount']):,.2f}"),
            Td(Span(s['status'].title(), cls=badge_cls(s['status']))),
            Td(s['created_at'] or ''),
            Td(action_dropdown(s)),
        )

    # Pagination controls
    def pagination_controls():
        if total_pages <= 1:
            return Fragment()
        nav_items = []
        prev_disabled = ' disabled' if page <= 1 else ''
        next_disabled = ' disabled' if page >= total_pages else ''
        nav_items.append(Li(A('Previous', hx_get=f"/admin/sales?page={page-1}", hx_target='#main-content', cls=f'page-link{prev_disabled}'), cls='page-item'))
        nav_items.append(Li(Span(f"Page {page} of {total_pages}", cls='page-link disabled'), cls='page-item'))
        nav_items.append(Li(A('Next', hx_get=f"/admin/sales?page={page+1}", hx_target='#main-content', cls=f'page-link{next_disabled}'), cls='page-item'))
        return Nav(Ul(*nav_items, cls='pagination'))

    content = Div(
        H1("Sales Approvals"),
        Div(
            Card(title="Total Sales", content=str(len(rows)), card_cls="card mb-4 h-100"),
            Card(title="Pending", content=str(len([r for r in rows if r['status']=='pending'])), card_cls="card mb-4 h-100"),
            Card(title="Approved", content=str(len([r for r in rows if r['status']=='approved'])), card_cls="card mb-4 h-100"),
            cls="row"
        ),
        Div(
            Div(
                Table(
                    Thead(Tr(Th("S/N"), Th("Property"), Th("Client"), Th("Amount"), Th("Status"), Th("Date"), Th("Action"))),
                    Tbody(*(row_to_tr(i, s) for i, s in enumerate(page_rows)) if page_rows else Tr(Td("No sales found", colspan="7", cls="text-center text-muted py-4"))),
                    cls="table table-striped table-hover"
                ),
                cls="table-responsive"
            ),
            pagination_controls(),
            cls="card"
        ),
        (toast_script if toast_script else Fragment()),
        cls="container-fluid"
    )
    return content if request.headers.get("HX-Request") else Layout(content, user_role="Admin")


async def admin_sale_detail(request: Request):
    user, redirect = _require_admin(request)
    if redirect: return redirect
    sale_id = int(request.path_params.get('sale_id'))
    s = get_sale_by_id(sale_id)
    if not s:
        content = Div("Sale not found", cls="alert alert-danger")
        return content if request.headers.get("HX-Request") else Layout(content, user_role="Admin")

    content = Div(
        Button("← Back", cls="btn btn-outline-secondary mb-4", hx_get="/admin/sales", hx_target="#main-content"),
        H2(f"Sale #{s['id']} - {s['client_first_name']} {s['client_last_name']}"),
        Div(
            Div(
                H5("Property"),
                P(f"{s['property_name'] or s['property_id']}")
            , cls="col-md-4"),
            Div(
                H5("Realtor"),
                P(s['realtor_email'] or s['realtor_id'])
            , cls="col-md-4"),
            Div(
                H5("Amount"),
                P(f"₦{float(s['amount']):,.2f}")
            , cls="col-md-4"),
            cls="row"
        ),
        Div(
            H5("Status"),
            P(Span(s['status'].title(), cls=f"badge bg-{'success' if s['status']=='approved' else 'warning' if s['status']=='pending' else 'danger'}")),
            cls="mb-3"
        ),
        Div(
            # Approval form with adjustable commission rate
            (Form(
                Div(
                    Label("Commission Rate (%)", cls="form-label me-2"),
                    Input(type="number", name="commission_rate", value=str(int(DEFAULT_COMMISSION_RATE*100)), step="0.01", min="0", max="100", cls="form-control", style="max-width: 160px; display: inline-block;"),
                    Button("Approve", type="submit", cls="btn btn-success ms-3"),
                    cls="d-flex align-items-center"
                ),
                hx_post=f"/admin/sales/{s['id']}/approve", hx_target="#main-content"
            ) if s['status']=='pending' else Fragment()),
            # Reject form with reason
            (Form(
                Div(
Input(type="text", name="reject_reason", placeholder="Reason (required)", required=True, cls="form-control", style="max-width: 280px; display: inline-block;"),
                    Button("Reject", type="submit", cls="btn btn-danger ms-3"),
                    cls="d-flex align-items-center ms-3"
                ),
                hx_post=f"/admin/sales/{s['id']}/reject", hx_target="#main-content"
            ) if s['status']=='pending' else Fragment()),
            cls="mb-4 d-flex align-items-center"
        ),
        cls="container-fluid"
    )
    return content if request.headers.get("HX-Request") else Layout(content, user_role="Admin")


# Action
async def admin_sale_approve(request: Request):
    user, redirect = _require_admin(request)
    if redirect: return redirect
    sale_id = int(request.path_params.get('sale_id'))
    # Prefer commission rate from form (percentage), fallback to query or default
    commission_rate = DEFAULT_COMMISSION_RATE
    try:
        form = await request.form()
        if form and form.get('commission_rate') is not None:
            commission_rate = float(form.get('commission_rate')) / 100.0
        else:
            commission_rate = float(request.query_params.get('commission_rate', DEFAULT_COMMISSION_RATE))
    except Exception:
        commission_rate = DEFAULT_COMMISSION_RATE

    res = approve_sale_and_create_payout(sale_id, user.id, commission_rate)
    if not res.get('updated'):
        content = Div(
            Div(f"Approval failed: {res.get('error', 'unknown error')}", cls="alert alert-danger"),
            Script("showToast('Approval failed', 'danger')")
        )
        return content if request.headers.get("HX-Request") else Layout(content, user_role="Admin")
    else:
        # Set flash message and redirect
        if hasattr(request, 'session'):
            request.session['flash'] = {'message': 'Sale approved and payout created', 'level': 'success'}
        return Response(headers={'HX-Redirect': '/admin/sales'})


async def admin_sale_reject(request: Request):
    user, redirect = _require_admin(request)
    if redirect: return redirect
    sale_id = int(request.path_params.get('sale_id'))
    reason = None
    try:
        form = await request.form()
        reason = form.get('reject_reason')
    except Exception:
        reason = None
    ok = reject_sale(sale_id, user.id, reason)
    if ok:
        # Set flash message and redirect
        if hasattr(request, 'session'):
            request.session['flash'] = {'message': 'Sale rejected', 'level': 'success'}
        return Response(headers={'HX-Redirect': '/admin/sales'})
    else:
        content = Div(
            Div("Reject failed.", cls="alert alert-danger"),
            Button("Back to Sales", cls="btn btn-secondary", hx_get="/admin/sales", hx_target="#main-content"),
            Script("showToast('Reject failed', 'danger')")
        )
        return content if request.headers.get("HX-Request") else Layout(content, user_role="Admin")


# Payouts and Withdraw Requests
async def admin_payouts_list(request: Request):
    user, redirect = _require_admin(request)
    if redirect: return redirect
    # Show approved withdrawal requests as historical payouts
    from backend.src.api.wallets import get_withdraw_requests
    rows = [r for r in get_withdraw_requests() if r['status'] == 'approved']

    # Flash (session-based)
    toast_script = None
    flash = request.session.pop('flash', None) if hasattr(request, 'session') else None
    if flash and isinstance(flash, dict):
        msg = flash.get('message') or ''
        level = flash.get('level') or 'info'
        toast_script = Script(f"showToast({msg!r}, {level!r})")

    def row_to_tr(idx, r):
        return Tr(
            Td(str(idx+1)),
            Td(r['realtor_email'] or r['realtor_id']),
            Td(f"₦{float(r['amount']):,.2f}"),
            Td(Span(p['status'].title(), cls=badge_cls(p['status']))),
            Td(r['decided_at'] or ''),
        )
    # Pagination
    per_page = 10
    try:
        page = int(request.query_params.get('page', '1'))
    except Exception:
        page = 1
    total = len(rows)
    total_pages = max(1, math.ceil(total / per_page))
    page = max(1, min(page, total_pages))
    start = (page - 1) * per_page
    page_rows = rows[start:start+per_page]

    def pagination_controls():
        if total_pages <= 1:
            return Fragment()
        nav_items = []
        prev_disabled = ' disabled' if page <= 1 else ''
        next_disabled = ' disabled' if page >= total_pages else ''
        nav_items.append(Li(A('Previous', hx_get=f"/admin/payouts?page={page-1}", hx_target='#main-content', cls=f'page-link{prev_disabled}'), cls='page-item'))
        nav_items.append(Li(Span(f"Page {page} of {total_pages}", cls='page-link disabled'), cls='page-item'))
        nav_items.append(Li(A('Next', hx_get=f"/admin/payouts?page={page+1}", hx_target='#main-content', cls=f'page-link{next_disabled}'), cls='page-item'))
        return Nav(Ul(*nav_items, cls='pagination'))

    content = Div(
        H1("Payouts (Approved Withdrawals)"),
        Div(
            Div(
                Table(
                    Thead(Tr(Th("S/N"), Th("Realtor"), Th("Amount"), Th("Status"), Th("Approved On"))),
                    Tbody(*(row_to_tr(i, r) for i, r in enumerate(page_rows)) if page_rows else Tr(Td("No approved withdrawals", colspan="5", cls="text-center text-muted py-4"))),
                    cls="table table-striped table-hover"
                ),
                cls="table-responsive"
            ),
            pagination_controls(),
            cls="card"
        ),
        (toast_script if toast_script else Fragment()),
        cls="container-fluid"
    )
    return content if request.headers.get("HX-Request") else Layout(content, user_role="Admin")


# Commissions admin
from backend.src.api.admin_sales import approve_commission, reject_commission, get_payouts

async def admin_commissions_list(request: Request):
    user, redirect = _require_admin(request)
    if redirect: return redirect
    rows = get_payouts()

    # Pagination
    per_page = 10
    try:
        page = int(request.query_params.get('page', '1'))
    except Exception:
        page = 1
    total = len(rows)
    total_pages = max(1, math.ceil(total / per_page))
    page = max(1, min(page, total_pages))
    start = (page - 1) * per_page
    page_rows = rows[start:start+per_page]

    # Flash toast
    toast_script = None
    flash = request.session.pop('flash', None) if hasattr(request, 'session') else None
    if flash and isinstance(flash, dict):
        msg = flash.get('message') or ''
        level = flash.get('level') or 'info'
        toast_script = Script(f"showToast({msg!r}, {level!r})")

    def badge_cls(status: str) -> str:
        status = (status or '').lower()
        if status in ('approved', 'paid', 'success'):
            return 'badge bg-success'
        if status in ('pending', 'in_progress', 'processing'):
            return 'badge bg-warning'
        if status in ('rejected', 'failed', 'cancelled', 'error'):
            return 'badge bg-danger'
        return 'badge bg-secondary'

    def action_dropdown(p):
        items = []
        if p['status'] == 'pending':
            items.append(Li(A('Approve', hx_post=f"/admin/commissions/{p['id']}/approve", hx_target="#main-content", cls='dropdown-item')))
            items.append(Li(A('Reject', hx_post=f"/admin/commissions/{p['id']}/reject", hx_target="#main-content", hx_confirm='Reject this commission?', cls='dropdown-item')))
        return Div(
            Button(cls='btn btn-sm btn-outline-secondary dropdown-toggle', data_bs_toggle='dropdown'),
            Ul(*items, cls='dropdown-menu'),
            cls='dropdown'
        )

    def row_to_tr(idx, p):
        commission = float(p['amount']) if p['amount'] is not None else 0.0
        sale_amount = float(p['sale_amount']) if p['sale_amount'] is not None else 0.0
        rate = float(p['commission_rate']) if p['commission_rate'] is not None else 0.0
        rate_pct = f"{rate*100:.2f}%"
        return Tr(
            Td(str(start + idx + 1)),
            Td(p['realtor_email'] or p['realtor_id']),
            Td(f"₦{sale_amount:,.2f}"),
            Td(f"₦{commission:,.2f}"),
            Td(Span(p['status'].title(), cls=badge_cls(p['status']))),
            Td(p['created_at'] or ''),
            Td(action_dropdown(p))
        )

    def pagination_controls():
        if total_pages <= 1:
            return Fragment()
        nav_items = []
        prev_disabled = ' disabled' if page <= 1 else ''
        next_disabled = ' disabled' if page >= total_pages else ''
        nav_items.append(Li(A('Previous', hx_get=f"/admin/commissions?page={page-1}", hx_target='#main-content', cls=f'page-link{prev_disabled}'), cls='page-item'))
        nav_items.append(Li(Span(f"Page {page} of {total_pages}", cls='page-link disabled'), cls='page-item'))
        nav_items.append(Li(A('Next', hx_get=f"/admin/commissions?page={page+1}", hx_target='#main-content', cls=f'page-link{next_disabled}'), cls='page-item'))
        return Nav(Ul(*nav_items, cls='pagination'))

    content = Div(
        H1("Commissions Management"),
        Div(
            Div(
                Table(
                    Thead(Tr(Th("S/N"), Th("Realtor"), Th("Sale Amount"), Th("Commission"), Th("Status"), Th("Created"), Th("Action"))),
                    Tbody(*(row_to_tr(i, p) for i, p in enumerate(page_rows)) if page_rows else Tr(Td("No commissions", colspan="9", cls="text-center text-muted py-4"))),
                    cls="table table-striped table-hover"
                ),
                cls="table-responsive"
            ),
            pagination_controls(),
            cls="card"
        ),
        (toast_script if toast_script else Fragment()),
        cls="container-fluid"
    )
    return content if request.headers.get("HX-Request") else Layout(content, user_role="Admin")


async def admin_commission_approve(request: Request):
    user, redirect = _require_admin(request)
    if redirect: return redirect
    cid = int(request.path_params.get('commission_id'))
    ok = approve_commission(cid, user.id)
    if hasattr(request, 'session'):
        request.session['flash'] = {'message': 'Commission approved' if ok else 'Approval failed', 'level': 'success' if ok else 'danger'}
    return Response(headers={'HX-Redirect': '/admin/commissions'})


async def admin_commission_reject(request: Request):
    user, redirect = _require_admin(request)
    if redirect: return redirect
    cid = int(request.path_params.get('commission_id'))
    ok = reject_commission(cid, user.id)
    if hasattr(request, 'session'):
        request.session['flash'] = {'message': 'Commission rejected' if ok else 'Rejection failed', 'level': 'success' if ok else 'danger'}
    return Response(headers={'HX-Redirect': '/admin/commissions'})


# Withdraw requests admin
from backend.src.api.wallets import get_withdraw_requests, approve_withdraw_request, reject_withdraw_request

async def admin_withdraw_requests_list(request: Request):
    user, redirect = _require_admin(request)
    if redirect: return redirect
    rows = get_withdraw_requests()

    # Pagination
    per_page = 10
    try:
        page = int(request.query_params.get('page', '1'))
    except Exception:
        page = 1
    total = len(rows)
    total_pages = max(1, math.ceil(total / per_page))
    page = max(1, min(page, total_pages))
    start = (page - 1) * per_page
    page_rows = rows[start:start+per_page]

    # Flash toast
    toast_script = None
    flash = request.session.pop('flash', None) if hasattr(request, 'session') else None
    if flash and isinstance(flash, dict):
        msg = flash.get('message') or ''
        level = flash.get('level') or 'info'
        toast_script = Script(f"showToast({msg!r}, {level!r})")

    def badge_cls(status: str) -> str:
        status = (status or '').lower()
        if status in ('approved', 'paid', 'success'):
            return 'badge bg-success'
        if status in ('pending', 'in_progress', 'processing'):
            return 'badge bg-warning'
        if status in ('rejected', 'failed', 'cancelled', 'error'):
            return 'badge bg-danger'
        return 'badge bg-secondary'

    def action_dropdown(r):
        items = []
        if r['status'] == 'pending':
            items.append(Li(A('Approve', hx_post=f"/admin/withdraw-requests/{r['id']}/approve", hx_target="#main-content", hx_confirm='Approve this withdrawal request?', cls='dropdown-item')))
            items.append(Li(A('Reject', hx_post=f"/admin/withdraw-requests/{r['id']}/reject", hx_target="#main-content", hx_confirm='Reject this withdrawal request?', cls='dropdown-item')))
        return Div(
            Button(cls='btn btn-sm btn-outline-secondary dropdown-toggle', data_bs_toggle='dropdown'),
            Ul(*items, cls='dropdown-menu'),
            cls='dropdown'
        )

    def row_to_tr(idx, r):
        return Tr(
            Td(str(start + idx + 1)),
            Td(r['realtor_email'] or r['realtor_id']),
            Td(f"₦{float(r['amount']):,.2f}"),
            Td(Span((r['status'] or '').title(), cls=badge_cls(r['status']))),
            Td(r['created_at'] or ''),
            Td(action_dropdown(r))
        )

    def pagination_controls():
        if total_pages <= 1:
            return Fragment()
        nav_items = []
        prev_disabled = ' disabled' if page <= 1 else ''
        next_disabled = ' disabled' if page >= total_pages else ''
        nav_items.append(Li(A('Previous', hx_get=f"/admin/withdraw-requests?page={page-1}", hx_target='#main-content', cls=f'page-link{prev_disabled}'), cls='page-item'))
        nav_items.append(Li(Span(f"Page {page} of {total_pages}", cls='page-link disabled'), cls='page-item'))
        nav_items.append(Li(A('Next', hx_get=f"/admin/withdraw-requests?page={page+1}", hx_target='#main-content', cls=f'page-link{next_disabled}'), cls='page-item'))
        return Nav(Ul(*nav_items, cls='pagination'))

    content = Div(
        H1("Withdraw Requests"),
        Div(
            Div(
                Table(
                    Thead(Tr(Th("S/N"), Th("Realtor"), Th("Amount"), Th("Status"), Th("Requested"), Th("Action"))),
                    Tbody(*(row_to_tr(i, r) for i, r in enumerate(page_rows)) if page_rows else Tr(Td("No requests", colspan="7", cls="text-center text-muted py-4"))),
                    cls="table table-striped table-hover"
                ),
                cls="table-responsive"
            ),
            pagination_controls(),
            cls="card"
        ),
        (toast_script if toast_script else Fragment()),
        cls="container-fluid"
    )
    return content if request.headers.get("HX-Request") else Layout(content, user_role="Admin")


async def admin_withdraw_request_approve(request: Request):
    user, redirect = _require_admin(request)
    if redirect: return redirect
    req_id = int(request.path_params.get('request_id'))
    ok = approve_withdraw_request(req_id, user.id)
    if hasattr(request, 'session'):
        request.session['flash'] = {'message': 'Withdrawal approved' if ok else 'Approval failed', 'level': 'success' if ok else 'danger'}
    return Response(headers={'HX-Redirect': '/admin/withdraw-requests'})


async def admin_withdraw_request_reject(request: Request):
    user, redirect = _require_admin(request)
    if redirect: return redirect
    req_id = int(request.path_params.get('request_id'))
    ok = reject_withdraw_request(req_id, user.id)
    if hasattr(request, 'session'):
        request.session['flash'] = {'message': 'Withdrawal rejected' if ok else 'Rejection failed', 'level': 'success' if ok else 'danger'}
    return Response(headers={'HX-Redirect': '/admin/withdraw-requests'})


async def admin_sales_pending_count_fragment(request: Request):
    # No auth gate for fragment; rely on visibility from sidebar role
    count = get_pending_sales_count()
    badge_cls = "badge bg-danger ms-2" if count > 0 else "badge bg-secondary ms-2"
    return Span(str(count), id="admin-sales-pending-badge", cls=badge_cls)


async def admin_payouts_pending_count_fragment(request: Request):
    count = get_pending_payouts_count()
    badge_cls = "badge bg-danger ms-2" if count > 0 else "badge bg-secondary ms-2"
    return Span(str(count), id="admin-payouts-pending-badge", cls=badge_cls)


# Withdraw requests count fragment (pending)
from backend.src.api.wallets import get_withdraw_requests as _get_all_withdraws

async def admin_withdraw_pending_count_fragment(request: Request):
    try:
        rows = _get_all_withdraws()
        count = len([r for r in rows if (r.get('status') or '') == 'pending'])
    except Exception:
        count = 0
    badge_cls = "badge bg-danger ms-2" if count > 0 else "badge bg-secondary ms-2"
    return Span(str(count), id="admin-withdraw-pending-badge", cls=badge_cls)


async def admin_payout_pay(request: Request):
    user, redirect = _require_admin(request)
    if redirect: return redirect
    payout_id = int(request.path_params.get('payout_id'))
    method = reference = notes = metadata = None
    try:
        form = await request.form()
        method = form.get('method')
        reference = form.get('reference')
        notes = form.get('notes')
        # If you later post JSON metadata, you can parse and pass it here
    except Exception:
        pass
    ok = mark_payout_paid(payout_id, user.id, method=method, reference=reference, notes=notes, metadata=metadata)
    if hasattr(request, 'session'):
        request.session['flash'] = {'message': 'Payout marked as paid' if ok else 'Update failed', 'level': 'success' if ok else 'danger'}
    return Response(headers={'HX-Redirect': '/admin/payouts'})
