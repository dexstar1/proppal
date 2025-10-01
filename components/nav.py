from fasthtml.common import *

def Navbar(user_role: str = "Client"):
    """A navigation bar with toggles for desktop/mobile sidebars, a search form, and user action icons."""
    badge_id = "notifications-badge-admin" if user_role == "Admin" else ("notifications-badge-realtor" if user_role == "Realtor" else "notifications-badge")
    return Nav(
        Div(
            # Mobile sidebar toggle
            Button(
                I(cls="fe fe-menu"),
                cls="btn btn-ghost d-lg-none",
                type="button",
                data_bs_toggle="offcanvas",
                data_bs_target="#sidebar"
            ),
            # Desktop sidebar toggle
            Button(
                I(cls="fe fe-menu"),
                cls="btn btn-ghost d-none d-lg-block text-left",
                type="button",
                id="desktop-sidebar-toggle"
            ),
            Form(
                Div(
                    Input(
                        cls="form-control form-control-underline form-control-sm border-dark",
                        type="search",
                        placeholder="Search properties"
                    ),
                    Div(
                        Button(
                            I(cls="fe fe-search"),
                            cls="btn btn-underline btn-sm border-dark",
                            type="button"
                        ),
                        cls="input-group-append"
                    ),
                    cls="input-group"
                ),
                cls="navbar-form w-100 mx-3",
                style="max-width: 550px;"
            ),
        Ul(
                Li(
                    A(
                    Span(
                        I(cls="fe fe-bell"),
                        "0",
                        id=badge_id,
                        cls='badge bg-white ms-2',
                        hx_get='/notifications/unread-count',
                        hx_trigger='load',
                        hx_target=f"#{badge_id}",
                        hx_swap='outerHTML'
                    ),
                    cls="nav-link",
                    hx_get="/notifications",
                    hx_target="#main-content"
                    ),
                    cls="nav-item me-3 d-flex align-items-center"
                ),
                Li(
                    (A(
                        Img(src="/assets/img/properties/placeholder.png", cls="rounded-circle", style="width:32px;height:32px;object-fit:cover;", id="nav-profile-avatar", hx_get="/realtor/profile/avatar", hx_trigger="load", hx_swap="outerHTML"),
                        cls="nav-link p-0 d-flex align-items-center"
                    ) if user_role == "Realtor" else A(
                        I(cls="fe fe-user"),
                        cls="nav-link",
                        href="#"
                    )),
                    cls="nav-item"
                ),
                cls="navbar-nav flex-row align-items-center"
            ),
            cls="container-fluid"
        ),
        cls="navbar navbar-expand navbar-light pt-0 pt-lg-6"
    )