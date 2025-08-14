from fasthtml.common import *
from components.nav import nav
from docs.alerts import Alerts
from docs.avatars import Avatars
from docs.badges import Badges
from docs.brands import Brands
from docs.breadcrumbs import Breadcrumbs
from docs.rates import Rates

def design_system():
    return Div(
                Div(
                    Div(
                        nav(), cls="col-12 col-md-4 col-lg-3 col-xl-2"
                    ),
                    Div(Alerts(), cls="col-12 col-md-8 col-lg-9 col-xl-10 px-md-10 py-10"),
                    Div(Avatars(), cls="col-12 col-md-8 col-lg-9 col-xl-10 px-md-10 py-10"),
                    Div(Badges(), cls="col-12 col-md-8 col-lg-9 col-xl-10 px-md-10 py-10"),
                    Div(Brands(), cls="col-12 col-md-8 col-lg-9 col-xl-10 px-md-10 py-10"),
                    Div(Breadcrumbs(), cls="col-12 col-md-8 col-lg-9 col-xl-10 px-md-10 py-10"),
                    Div(Rates(), cls="col-12 col-md-8 col-lg-9 col-xl-10 px-md-10 py-10"),
                    cls="row" ), cls="container-fluid"
    )