from fasthtml.common import *
from components.avatar import avatar

def Sidebar(user_role: str = "Client"):
    """Renders a responsive sidebar, fixed on desktop and off-canvas on mobile."""
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
            'Leads': '/admin/leads',
            'Enquiries': '/admin/enquiries',
            'Users': '/admin/users',
            'Analytics': '/admin/analytics',
            'Payouts': '/admin/payouts',
        }
    elif user_role == "Realtor":
        sidebar_links = {
            'Dashboard': '/realtor/dashboard',
            'Properties': '/realtor/properties',
            'Property Sales': '/realtor/property-sales',
            'Properties': '/realtor/properties',
            'Referrals': '/realtor/referrals',
            'Commissions': '/realtor/commissions',
            'Withdraw Funds': '/realtor/withdraw-funds',
            'Transactions': '/realtor/transactions',
        }

    sidebar_items = [
        Li(
            A(text, href=link, hx_get=link, hx_target="#main-content", hx_push_url="true", cls="nav-link text-light"),
            cls="nav-item"
        ) for text, link in sidebar_links.items()
    ]

    profile_items = [
        Li(A("My Account", href="#", cls="nav-link text-light"), cls="nav-item"),
        Li(A("Notifications", href="#", cls="nav-link text-light"), cls="nav-item"),
        Li(A("Sign out", href="/logout", cls="nav-link text-light"), cls="nav-item"),
    ]

    # Shared content for both sidebars
    sidebar_content = (
        Div(
            avatar(avatar_size="xxl", shape="circle", src="../assets/images/avatars/avatar-1.jpg", alt="..."),
            Div(
                Span("Welcome Back,", cls="mb-0"),
                Span(user_role, cls="fw-bold mb-0"),
                cls="ms-2 mt-2"
            ), cls="d-flex flex-column text-center align-items-center p-3 mb-3 text-light"
        ),
        Ul(*sidebar_items, cls="nav nav-pills flex-column"),
        Ul(*profile_items, cls="nav nav-pills flex-column"),
    )

    # Desktop sidebar (fixed and togglable)
    desktop_sidebar = Nav(
        *sidebar_content,
        id="desktop-sidebar",
        cls="d-none d-lg-flex flex-column flex-shrink-0 p-3 bg-dark vh-100",
        style="position: fixed; top: 0; left: 0; width: 240px; z-index: 1020;"
    )

    # Mobile sidebar (off-canvas)
    mobile_sidebar = Div(
        Div(H5("Menu", cls="offcanvas-title"), Button(cls="btn-close", data_bs_dismiss="offcanvas"), cls="offcanvas-header"),
        Div(
            Nav(*sidebar_content, cls="d-flex flex-column flex-shrink-0 p-3 bg-dark h-100"),
            cls="offcanvas-body p-0"
        ),
        id="sidebar",
        cls="offcanvas offcanvas-start d-lg-none",
        tabindex="-1"
    )

    return Fragment(desktop_sidebar, mobile_sidebar)