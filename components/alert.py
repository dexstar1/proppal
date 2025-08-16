from fasthtml.common import *

def primary_alert():
    return Div("A simple primary alert—check it out!", cls="alert alert-primary", role="alert"),

def secondary_alert():
    return Div("A simple secondary alert—check it out!", cls="alert alert-secondary", role="alert"),

def success_alert():
    return Div(
                H6("Well done!", cls="alert-heading"),
                P("Aww yeah, you successfully read this important alert message. This example text is going to run a bit longer so that you can see how spacing within an alert works with this kind of content."),
                Hr(),
                P("Whenever you need to, be sure to use margin utilities to keep things nice and tidy.", cls="mb-0"),
                cls="alert alert-success", role="alert"
            ),     

def danger_alert():
    return Div(
                Strong("Danger Will Robinson!"), " This is a dismissable alert!",
                Button(
                    Span("×", aria_hidden="true"),
                    type="button", cls="btn-close", data_dismiss="alert", aria_label="Close"
                ),
                cls="alert alert-danger alert-dismissible fade show", role="alert"
            ),              

def warning_alert():
    return Div(
                Strong("Holy guacamole!"), " Notice how the text/UI have high contrast?",
                Button(
                    Span("×", aria_hidden="true"),
                    type="button", cls="btn-close", data_dismiss="alert", aria_label="Close"
                ),
                cls="alert alert-warning alert-dismissible fade show", role="alert"
            ),

def info_alert():
    return Div("A simple info alert—check it out!", cls="alert alert-info", role="alert"),

def light_alert():
    return Div("A simple light alert—check it out!", cls="alert alert-light", role="alert"),

def dark_alert():
    return Div("A simple dark alert—check it out!", cls="alert alert-dark", role="alert"),
