from fasthtml.common import *

def Badges():
    return Div(
        H2("Badges", cls="fw-bold text-uppercase"),
        P("Badges are used to highlight new or unread items. They can be used in various contexts to convey information."),
        Div(
            Span("New", cls="badge bg-primary"),
            Span("Updated", cls="badge bg-secondary"),
            Span("Sale", cls="badge bg-danger"),
            cls="mb-3"
        ),
        H3("Examples", cls="mt-4"),
        Div(
            Div("Example 1", cls="badge bg-success"),
            Div("Example 2", cls="badge bg-warning"),
            cls="d-flex flex-column gap-2"
        ),
        cls="px-md-10 py-10"
    )