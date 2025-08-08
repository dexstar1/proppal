from fasthtml.common import *

def Alerts():
    return Section(
            H3("Alerts"),
            P(
                "Provide contextual feedback messages for typical user actions with the handful of available and flexible alert messages. ",
                Br(),
                A("Bootstrap documentation", href="http://getbootstrap.com/docs/5.1/components/alerts/", target="_blank"),
                cls="text-gray-500"
            ),
            Div(
                Div(
                    # Primary
                    Div("A simple primary alert—check it out!", cls="alert alert-primary", role="alert"),
                    # Secondary
                    Div("A simple secondary alert—check it out!", cls="alert alert-secondary", role="alert"),
                    # Success
                    Div(
                        H6("Well done!", cls="alert-heading"),
                        P("Aww yeah, you successfully read this important alert message. This example text is going to run a bit longer so that you can see how spacing within an alert works with this kind of content."),
                        Hr(),
                        P("Whenever you need to, be sure to use margin utilities to keep things nice and tidy.", cls="mb-0"),
                        cls="alert alert-success", role="alert"
                    ),
                    # Danger
                    Div(
                        Strong("Danger Will Robinson!"), " This is a dismissable alert!",
                        Button(
                            Span("×", aria_hidden="true"),
                            type="button", cls="btn-close", data_dismiss="alert", aria_label="Close"
                        ),
                        cls="alert alert-danger alert-dismissible fade show", role="alert"
                    ),
                    # Warning
                    Div(
                        Strong("Holy guacamole!"), " Notice how the text/UI have high contrast?",
                        Button(
                            Span("×", aria_hidden="true"),
                            type="button", cls="btn-close", data_dismiss="alert", aria_label="Close"
                        ),
                        cls="alert alert-warning alert-dismissible fade show", role="alert"
                    ),
                    # Info
                    Div("A simple info alert—check it out!", cls="alert alert-info", role="alert"),
                    # Light
                    Div("A simple light alert—check it out!", cls="alert alert-light", role="alert"),
                    # Dark
                    Div("A simple dark alert—check it out!", cls="alert alert-dark", role="alert"),
                    cls="card-body border"
                ),
                cls="card"
            ),
            cls="px-md-10 py-10"
        )