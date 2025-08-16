from fasthtml.common import *
from components.alert import primary_alert
from components.alert import secondary_alert
from components.alert import success_alert
from components.alert import danger_alert
from components.alert import warning_alert
from components.alert import info_alert
from components.alert import light_alert
from components.alert import dark_alert


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
                    primary_alert(), 
                    secondary_alert(),
                    success_alert(),
                    danger_alert(),
                    warning_alert(),
                    info_alert(),
                    light_alert(),
                    dark_alert(),
                    cls="card-body border"
                ),
                cls="card"
            ),
            cls="px-md-10 py-10"
        )