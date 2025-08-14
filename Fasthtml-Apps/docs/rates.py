from fasthtml.common import *

def Rates():
    return Div(
        H2("Rates", cls="mb-4"),
        P("Here you can find the various rates applicable to our services.", cls="lead"),
        H3("Standard Rates", cls="mt-4"),
        P("Our standard rates are as follows:", cls="mb-2"),
        Ul(
            Li("Service A: $100"),
            Li("Service B: $150"),
            Li("Service C: $200"),
            cls="list-unstyled"
        ),
        H3("Discounted Rates", cls="mt-4"),
        P("We offer discounted rates for bulk purchases:", cls="mb-2"),
        Ul(
            Li("Service A: $90 (for 10 or more)"),
            Li("Service B: $135 (for 10 or more)"),
            Li("Service C: $180 (for 10 or more)"),
            cls="list-unstyled"
        ),
        cls="px-md-10 py-10"
    )