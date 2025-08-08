from fasthtml.common import *

def Badges():
    return Section(
        H3("Badges"),
        P(
            "A small count and labeling component. ",
            Br(),
            A("Bootstrap documentation", href="https://getbootstrap.com/docs/5.1/components/badge/", target="_blank"),
            cls="text-gray-500"
        ),
        Div(
            Div(
                Span("Primary", cls="badge bg-primary"),
                Span("Secondary", cls="badge bg-secondary"),
                Span("Success", cls="badge bg-success"),
                Span("Danger", cls="badge bg-danger"),
                Span("Warning", cls="badge bg-warning"),
                Span("Info", cls="badge bg-info"),
                Span("Light", cls="badge bg-light text-body"),
                Span("Dark", cls="badge bg-dark"),
                Span("White", cls="badge bg-white text-body"),
                cls="card-body border"
            ),
            cls="card"
        ),
        Hr(cls="my-7"),
        H5("Links"),
        P(
            "Using the contextual ",
            Code(".badge-*"),
            " classes on an ",
            Code("<a>"),
            " element quickly provide actionable badges with hover and focus states.",
            cls="text-gray-500"
        ),
        Div(
            Div(
                A("Primary", href="#!", cls="badge bg-primary"),
                A("Secondary", href="#!", cls="badge bg-secondary"),
                A("Success", href="#!", cls="badge bg-success"),
                A("Danger", href="#!", cls="badge bg-danger"),
                A("Warning", href="#!", cls="badge bg-warning"),
                A("Info", href="#!", cls="badge bg-info"),
                A("Light", href="#!", cls="badge bg-light text-body"),
                A("Dark", href="#!", cls="badge bg-dark"),
                A("White", href="#!", cls="badge bg-white text-body")      
                ),
        cls="card"
    ),
    cls="px-md-10 py-10"
)