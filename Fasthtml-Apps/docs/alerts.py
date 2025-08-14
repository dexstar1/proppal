from fasthtml.common import *

def Alerts():
    return Div(
        H2("Alerts", cls="fw-bold text-uppercase"),
        Div(
            P("This is a primary alert—check it out!", cls="alert alert-primary"),
            P("This is a secondary alert—check it out!", cls="alert alert-secondary"),
            P("This is a success alert—check it out!", cls="alert alert-success"),
            P("This is a danger alert—check it out!", cls="alert alert-danger"),
            P("This is a warning alert—check it out!", cls="alert alert-warning"),
            P("This is an info alert—check it out!", cls="alert alert-info"),
            P("This is a light alert—check it out!", cls="alert alert-light"),
            P("This is a dark alert—check it out!", cls="alert alert-dark"),
            cls="px-md-10 py-10"
        )
    )