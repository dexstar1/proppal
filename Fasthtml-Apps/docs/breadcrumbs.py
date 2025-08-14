from fasthtml.common import *

def Breadcrumbs():
    return Div(
        Div(
            H2("Breadcrumbs", cls="fs-4 fw-bold"),
            P("Breadcrumbs are a navigation aid that helps users understand their current location within a website or application. They provide a way to navigate back to previous sections easily."),
            Div(
                P("Example:"),
                Ol(
                    Li(A("Home", href="#")),
                    Li(A("Library", href="#")),
                    Li(A("Data", href="#")),
                    cls="breadcrumb"
                ),
                cls="px-md-10 py-10"
            ),
            cls="px-md-10 py-10"
        ),
        cls="px-md-10 py-10"
    )