from fasthtml.common import *

def admin_button():
    return Div(
        Button("Admin",
                hx_get=f"/add-product",
                hx_swap="innerHTML",
                hx_target="#theBody",
               cls="btn btn-primary btn-lg")
    )

def docs_button():
    return Div(
        Button("Docs",
                hx_get=f"/docs",
                hx_swap="innerHTML",
                hx_target="#theBody",
               cls="btn btn-primary btn-lg")
    )


def view_site_button():
    return Div(
        Button("Back",
                hx_get=f"/",
                hx_swap="outerHTML",
                hx_target="#theBody",
               cls="btn btn-outline-primary btn-underline mb-1")
    )
