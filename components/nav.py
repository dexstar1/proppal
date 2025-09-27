from fasthtml.common import *

def Navbar():
    """A navigation bar with toggles for desktop/mobile sidebars, a search form, and user action icons."""
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
                cls="btn btn-ghost d-none d-lg-block",
                type="button",
                id="desktop-sidebar-toggle"
            ),
            Form(
                Div(
                    Input(
                        cls="form-control form-control-underline form-control-sm border-dark",
                        type="search",
                        placeholder="Search for items and brands"
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
                        I(cls="fe fe-user"),
                        cls="nav-link",
                        href="./account-orders.html"
                    ),
                    cls="nav-item"
                ),
                Li(
                    A(
                        I(cls="fe fe-heart"),
                        cls="nav-link",
                        href="./account-wishlist.html"
                    ),
                    cls="nav-item ms-lg-n4"
                ),
                Li(
                    A(
                        Span(
                            I(cls="fe fe-shopping-cart"),
                            data_cart_items="2"
                        ),
                        cls="nav-link",
                        data_bs_toggle="offcanvas",
                        href="#modalShoppingCart"
                    ),
                    cls="nav-item ms-lg-n4"
                ),
                cls="navbar-nav flex-row"
            ),
            cls="container-fluid"
        ),
        cls="navbar navbar-expand navbar-light pt-0 pt-lg-6"
    )