from fasthtml.common import *
from components.layout import Layout
from starlette.requests import Request
from starlette.responses import RedirectResponse
from backend.src.api.notifications import get_notifications_for_user, mark_notification_read, get_unread_count_for_user, mark_all_notifications_read


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

    def row_to_tr(n):
        return Tr(
            Td(Span("•", cls="text-danger") if n['is_read'] == 0 else Td()),
            Td(n['title']),
            Td(n['message']),
            Td(n['created_at']),
            Td(
                (Button("Open", cls="btn btn-sm btn-primary me-2", hx_get=n['link'], hx_target="#main-content") if n['link'] else Fragment()),
                (Button("Mark Read", cls="btn btn-sm btn-outline-secondary", hx_post=f"/notifications/{n['id']}/read", hx_target="#main-content") if n['is_read'] == 0 else Span("Read", cls="text-muted"))
            )
        )

    content = Div(
        Div(
            H1("Notifications", cls="me-auto"),
            Div(
                A("All", hx_get="/notifications?filter=all", hx_target="#main-content", cls=f"btn btn-sm me-2 {'btn-primary' if filter_val=='all' else 'btn-outline-primary'}"),
                A("Unread", hx_get="/notifications?filter=unread", hx_target="#main-content", cls=f"btn btn-sm me-3 {'btn-primary' if filter_val=='unread' else 'btn-outline-primary'}"),
                Button("Mark All Read", cls="btn btn-sm btn-outline-secondary", disabled=(unread_count==0), hx_post="/notifications/mark-all-read", hx_target="#main-content"),
                cls="d-flex align-items-center"
            ),
            cls="d-flex align-items-center justify-content-between mb-3"
        ),
        Table(
            Thead(Tr(Th(""), Th("Title"), Th("Message"), Th("Date"), Th("Actions"))),
            Tbody(*(row_to_tr(n) for n in rows) if rows else Tr(Td("No notifications", colspan="5", cls="text-center text-muted py-4"))),
            cls="table table-striped table-hover"
        ),
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
