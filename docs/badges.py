from fasthtml.common import *
from components.badge import badge_span, badge_link

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
                badge_span(text="Primary", type="primary"),
                badge_span(text="Secondary", type="secondary"),
                badge_span(text="Success", type="success"),
                badge_span(text="Danger", type="danger"),
                badge_span(text="Warning", type="warning"),
                badge_span(text="Info", type="info"),
                badge_span(text="Light", type="light"),
                badge_span(text="Dark", type="dark"),
                badge_span(text="White", type="white"),
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
                badge_link(text="Primary", type="primary", href="!"),
                badge_link(text="Secondary", type="secondary", href="!"),
                badge_link(text="Success", type="success", href="!"),
                badge_link(text="Danger", type="danger", href="!"),
                badge_link(text="Warning", type="warning", href="!"),
                badge_link(text="Info", type="info", href="!"),
                badge_link(text="Light", type="light", href="!"),
                badge_link(text="Dark", type="dark", href="!"),
                badge_link(text="White", type="white", href="!")
                ),
        cls="card"
    ),
    cls="px-md-10 py-10"
)