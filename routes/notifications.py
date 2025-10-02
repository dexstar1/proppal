from fasthtml.common import *
from components.layout import Layout
from starlette.requests import Request
from starlette.responses import RedirectResponse
from backend.src.api.notifications import get_notifications_for_user, mark_notification_read, get_unread_count_for_user, mark_all_notifications_read
import math


def _require_user(request: Request):
    user = request.scope.get('user')
    if not user:
        return None, RedirectResponse(url="/login")
    return user, None


async def notifications_list(request: Request):
    user, redirect = _require_user(request)
    if redirect: return redirect
    filter_val = request.query_params.get('filter', 'all')
    unread_only = (filter_val == 'unread')
    rows = get_notifications_for_user(user.id, unread_only=unread_only)
    unread_count = get_unread_count_for_user(user.id)

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

    def action_dropdown(n):
        d = n if isinstance(n, dict) else dict(n)
        items = []
        link = d.get('link')
        if link:
            items.append(Li(A('Open', hx_get=link, hx_target='#main-content', cls='dropdown-item')))
        is_read = int(d.get('is_read', 0) or 0)
        if is_read == 0:
            items.append(Li(A('Mark Read', hx_post=f"/notifications/{d['id']}/read", hx_target='#main-content', cls='dropdown-item')))
        else:
            items.append(Li(Span('Read', cls='dropdown-item text-muted')))
        return Div(
            Button(cls='btn btn-sm btn-outline-secondary dropdown-toggle', data_bs_toggle='dropdown'),
            Ul(*items, cls='dropdown-menu'),
            cls='dropdown'
        )

    def row_to_tr(n):
        return Tr(
            Td(n['title']),
            Td(n['message']),
            Td(n['created_at']),
            Td(action_dropdown(n))
        )

    def pagination_controls():
        if total_pages <= 1:
            return Fragment()
        nav_items = []
        prev_disabled = ' disabled' if page <= 1 else ''
        next_disabled = ' disabled' if page >= total_pages else ''
        base = f"/notifications?filter={filter_val}"
        nav_items.append(Li(A('Previous', hx_get=f"{base}&page={page-1}", hx_target='#main-content', cls=f'page-link{prev_disabled}'), cls='page-item'))
        nav_items.append(Li(Span(f"Page {page} of {total_pages}", cls='page-link disabled'), cls='page-item'))
        nav_items.append(Li(A('Next', hx_get=f"{base}&page={page+1}", hx_target='#main-content', cls=f'page-link{next_disabled}'), cls='page-item'))
        return Nav(Ul(*nav_items, cls='pagination'))

    content = Div(
        Div(
            H1("Notifications", cls="me-auto"),
            Div(
                A("All", hx_get="/notifications?filter=all", hx_target="#main-content", cls=f"badge me-2 {'badge-white' if filter_val=='all' else 'badge-secondary'}"),
                A("Unread", hx_get="/notifications?filter=unread", hx_target="#main-content", cls=f"badge me-3 {'badge-dark' if filter_val=='unread' else 'badge-secondary'}"),
                A("Read All", cls="badge badge-dark", disabled=(unread_count==0), hx_post="/notifications/mark-all-read", hx_target="#main-content"),
                cls="d-flex align-items-center"
            ),
            cls="mb-4"
        ),
        Div(
            Table(
                Thead(Tr(Th("Title"), Th("Message"), Th("Date"), Th("Action"))),
                Tbody(*(row_to_tr(n) for n in page_rows) if page_rows else Tr(Td("No notifications", colspan="5", cls="text-center text-muted py-4"))),
                cls="table table-responsive table-striped table-hover"
            ),
            cls="card my-4"
        ),
        pagination_controls(),
        cls="container-fluid"
    )
    # Flash toast on page render
    flash = request.session.pop('flash', None) if hasattr(request, 'session') else None
    if flash and isinstance(flash, dict):
        content = Div(content, Script(f"showToast({(flash.get('message') or '')!r}, {(flash.get('level') or 'info')!r})"))
    return content if request.headers.get("HX-Request") else Layout(content, user_role=getattr(user, 'role', 'Client'))


async def notifications_mark_read(request: Request):
    user, redirect = _require_user(request)
    if redirect: return redirect
    nid = int(request.path_params.get('notification_id'))
    mark_notification_read(nid, user.id)
    if hasattr(request, 'session'):
        request.session['flash'] = {'message': 'Notification marked as read', 'level': 'success'}
    return RedirectResponse(url="/notifications")


async def notifications_mark_all_read(request: Request):
    user, redirect = _require_user(request)
    if redirect: return redirect
    mark_all_notifications_read(user.id)
    if hasattr(request, 'session'):
        request.session['flash'] = {'message': 'All notifications marked as read', 'level': 'success'}
    return RedirectResponse(url="/notifications")


async def notifications_unread_count_fragment(request: Request):
    user, redirect = _require_user(request)
    if redirect: return redirect
    count = get_unread_count_for_user(user.id)
    badge_cls = "badge bg-danger ms-2" if count > 0 else "badge bg-secondary ms-2"
    # Return a span that can replace the existing badge via HTMX
    return Span(str(count), id="notifications-badge", cls=badge_cls)


async def notifications_dropdown_menu(request: Request):
    """Return recent notifications as dropdown <li> items for the navbar menu."""
    user, redirect = _require_user(request)
    if redirect: return redirect

    rows = get_notifications_for_user(user.id, unread_only=False) or []
    items = []

    # Header
    items.append(Li(Span("Notifications", cls="dropdown-header")))

    # Up to 5 recent
    for r in rows[:5]:
        n = dict(r) if not isinstance(r, dict) else r
        text = (n.get('title') or n.get('message') or 'Notification')
        is_unread = (n.get('is_read') == 0)
        label = Span(text, cls=("fw-bold" if is_unread else ""))
        if n.get('link'):
            items.append(
                Li(
                    A(
                        label,
                        hx_get=n['link'],
                        hx_target="#main-content",
                        cls="dropdown-item"
                    )
                )
            )
        else:
            items.append(Li(Span(text, cls="dropdown-item text-muted")))

    if not rows:
        items.append(Li(Span("No notifications", cls="dropdown-item text-muted")))

    # Footer
    items.append(Li(Hr(cls="dropdown-divider")))
    items.append(Li(A("View all notifications", hx_get="/notifications", hx_target="#main-content", cls="dropdown-item")))

    # Return only the li nodes to be swapped into the <ul> via hx-swap="innerHTML"
    return Fragment(*items)
