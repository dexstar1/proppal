from fasthtml.common import *
from components.avatar import avatar

def Sidebar(user_role: str = "Client", user_display: str | None = None):
    """Renders a responsive sidebar, fixed on desktop and off-canvas on mobile.
    If user_display is provided, it is used in the welcome header instead of the role.
    """
    sidebar_links = {}
    if user_role == "Client":
        sidebar_links = {
            'Dashboard': '/client/dashboard',
            'Browse Properties': '/client/properties',
            'My Enquiries': '/client/enquiries',
        }
    elif user_role == "Admin":
        sidebar_links = {
            'Dashboard': '/admin/dashboard',
            'Properties': '/admin/properties',
            'Sales': '/admin/sales',
            'Commissions': '/admin/commissions',
            'Payouts': '/admin/payouts',
            'Withdrawals': '/admin/withdraw-requests',
            'Users': '/admin/users',
            # 'Leads': '/admin/leads',
            # 'Enquiries': '/admin/enquiries',
            # 'Analytics': '/admin/analytics',
            'Notifications': '/notifications',
        }
    elif user_role == "Realtor":
        sidebar_links = {
            'Dashboard': '/realtor/dashboard',
            'Properties': '/realtor/properties',
            'Sales': '/realtor/sales',
            'Referrals': '/realtor/referrals',
            'Commissions': '/realtor/commissions',
            'Transactions': '/realtor/transactions',
            'Withdraw Funds': '/realtor/withdraw',
            'Notifications': '/notifications',
            'My Account': '/realtor/account',
        }

    # 🔹 Icon mapping
    icons = {
        'Dashboard': "fa-solid fa-gauge",
        'Browse Properties': "fa-solid fa-magnifying-glass",
        'My Enquiries': "fa-solid fa-envelope-open-text",
        'Properties': "fa-solid fa-building",
        'Sales': "fa-solid fa-chart-line",
        'Referrals': "fa-solid fa-user-group",
        'Commissions': "fa-solid fa-hand-holding-dollar",
        'Payouts': "fa-solid fa-sack-dollar",
        'Withdrawals': "fa-solid fa-wallet",
        'Users': "fa-solid fa-users",
        # 'Withdraw Funds': "fa-solid fa-wallet",
        # 'Leads': "fa-solid fa-user-plus",
        # 'Enquiries': "fa-solid fa-inbox",
        # 'Analytics': "fa-solid fa-chart-pie",
        'Notifications': "fa-solid fa-bell",
        'My Account': "fa-solid fa-user",
        'Transactions': "fa-solid fa-receipt",
        'Sign out': "fa-solid fa-right-from-bracket",
    }

    sidebar_items = []
    for text, link in sidebar_links.items():
        icon = icons.get(text, "fa-solid fa-circle")  # fallback icon

        if link == '/admin/sales':
            sidebar_items.append(
                Li(
                    Div(
                        A(I(cls=icon), " " + text,
                          href=link, hx_get=link, hx_target="#main-content", hx_push_url="true",
                          cls="nav-link text-light d-inline-flex align-items-center"),
                        Span("0", id="admin-sales-pending-badge",
                             cls="badge bg-secondary ms-2",
                             hx_get="/admin/sales/pending-count",
                             hx_trigger="revealed, every 20s", hx_swap="outerHTML"),
                        cls="d-flex align-items-center"
                    ),
                    cls="nav-item"
                )
            )
        elif link == '/admin/commissions':
            sidebar_items.append(
                Li(
                    Div(
                        A(I(cls=icon), " " + text,
                          href=link, hx_get=link, hx_target="#main-content", hx_push_url="true",
                          cls="nav-link text-light d-inline-flex align-items-center"),
                        Span("0", id="admin-payouts-pending-badge",
                             cls="badge bg-secondary ms-2",
                             hx_get="/admin/payouts/pending-count",
                             hx_trigger="revealed, every 20s", hx_swap="outerHTML"),
                        cls="d-flex align-items-center"
                    ),
                    cls="nav-item"
                )
            )
        elif link == '/admin/withdraw-requests':
            sidebar_items.append(
                Li(
                    Div(
                        A(I(cls=icon), " " + text,
                          href=link, hx_get=link, hx_target="#main-content", hx_push_url="true",
                          cls="nav-link text-light d-inline-flex align-items-center"),
                        Span("0", id="admin-withdraw-pending-badge",
                             cls="badge bg-secondary ms-2",
                             hx_get="/admin/withdraws/pending-count",
                             hx_trigger="revealed, every 20s", hx_swap="outerHTML"),
                        cls="d-flex align-items-center"
                    ),
                    cls="nav-item"
                )
            )
        elif link == '/notifications':
            sidebar_items.append(
                Li(
                    Div(
                        A(I(cls=icon), " " + text,
                          href=link, hx_get=link, hx_target='#main-content', hx_push_url='true',
                          cls='nav-link text-light d-inline-flex align-items-center'),
                        Span('0', id='notifications-badge',
                             cls='badge bg-secondary ms-2',
                             hx_get='/notifications/unread-count',
                             hx_trigger='revealed, every 20s, notification-update from:body',
                             hx_swap='outerHTML'),
                        cls='d-flex align-items-center'
                    ),
                    cls='nav-item'
                )
            )
        else:
            sidebar_items.append(
                Li(
                    A(I(cls=icon), " " + text,
                      href=link, hx_get=link, hx_target="#main-content", hx_push_url="true",
                      cls="nav-link text-light d-inline-flex align-items-center"),
                    cls="nav-item"
                )
            )

    profile_items = [
        Li(A(I(cls=icons['Sign out']), " Sign out",
             href="/logout", cls="nav-link text-light d-inline-flex align-items-center"),
           cls="nav-item"),
    ]

    # Shared content for both sidebars
    sidebar_content = (
        Div(
            avatar(avatar_size="xl",
                   src="/assets/images/cozyhavens_logo.png", alt="..."),
            cls="d-flex flex-column text-center align-items-center p-3 mb-3 border-bottom-logo"
        ),
        Ul(*sidebar_items, cls="nav nav-pills flex-column"),
        Ul(*profile_items, cls="nav nav-pills flex-column"),
    )

    # Desktop sidebar (fixed and togglable)
    desktop_sidebar = Nav(
        *sidebar_content,
        id="desktop-sidebar",
        cls="d-none d-lg-flex flex-column flex-shrink-0 p-4 bg-dark vh-100",
        style="position: fixed; top: 0; left: 0; width: 240px; z-index: 1020;overflow-y:scroll;"
    )

    # Mobile sidebar (off-canvas)
    mobile_sidebar = Div(
        Div(H5("Menu", cls="offcanvas-title"),
            Button(cls="btn-close", data_bs_dismiss="offcanvas"),
            cls="offcanvas-header"),
        Div(
            Nav(*sidebar_content, cls="d-flex flex-column flex-shrink-0 p-3 bg-dark h-100"),
            cls="offcanvas-body p-0"
        ),
        id="sidebar",
        cls="offcanvas offcanvas-start d-lg-none",
        tabindex="-1"
    )

    return Fragment(desktop_sidebar, mobile_sidebar)
