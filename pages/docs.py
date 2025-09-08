from fasthtml.common import *
from components.nav import nav
# from docs.alerts import Alerts
# from docs.avatars import Avatars
from docs.badges import Badges
# from docs.brands import Brands
# from docs.breadcrumbs import Breadcrumbs
# from docs.buttons import Buttons
from docs.cards import Cards
# from docs.dropdowns import Dropdowns
# from docs.forms import Forms
# from docs.icons import Icons 
# from docs.lists import Lists
# from docs.modals import Modals
# from docs.navbars import Navbars
# from docs.navs import Navs
# from docs.paginations import Paginations
# from docs.popovers import Popovers 
# from docs.progress import Progress 
# from docs.rates import Rates
# from docs.typography import Typography
from components.button import view_site_button

def design_system():
    return Div(
                view_site_button(),
                Div(
                    Div(
                        nav(), cls="col-12 col-md-4 col-lg-3 col-xl-2"
                    ),
                    # Div(Alerts(), cls="col-12 col-md-8 col-lg-9 col-xl-10"),
                    # Div(Avatars(), cls="col-12 col-md-8 col-lg-9 col-xl-10"), 
                    # Div(Badges(), cls="col-12 col-md-8 col-lg-9 col-xl-10"), 
                    # Div(Brands(), cls="col-12 col-md-8 col-lg-9 col-xl-10"),
                    # Div(Breadcrumbs(), cls="col-12 col-md-8 col-lg-9 col-xl-10"),
                    # Div(Buttons(), cls="col-12 col-md-8 col-lg-9 col-xl-10"),
                    Div(Cards(), cls="col-12 col-md-8 col-lg-9 col-xl-10"),
                    # Div(Dropdowns(), cls="col-12 col-md-8 col-lg-9 col-xl-10"),
                    # Div(Forms(), cls="col-12 col-md-8 col-lg-9 col-xl-10"),
                    # Div(Icons(), cls="col-12 col-md-8 col-lg-9 col-xl-10"),
                    # Div(Lists(), cls="col-12 col-md-8 col-lg-9 col-xl-10"),
                    # Div(Modals(), cls="col-12 col-md-8 col-lg-9 col-xl-10"),
                    # Div(Navbars(), cls="col-12 col-md-8 col-lg-9 col-xl-10"),
                    # Div(Navs(), cls="col-12 col-md-8 col-lg-9 col-xl-10"),
                    # Div(Paginations(), cls="col-12 col-md-8 col-lg-9 col-xl-10"),
                    # Div(Popovers(), cls="col-12 col-md-8 col-lg-9 col-xl-10"),
                    # Div(Progress(), cls="col-12 col-md-8 col-lg-9 col-xl-10"),
                    # Div(Rates(), cls="col-12 col-md-8 col-lg-9 col-xl-10"),
                    # Div(Typography(), cls="col-12 col-md-8 col-lg-9 col-xl-10"),
                    cls="row" ), cls="container-fluid", id="theBody"
    ) 