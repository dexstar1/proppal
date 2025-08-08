from fasthtml.common import *

def Modals():
    return Section(
        H3("Modals"),
        P(
            "Use Bootstrap’s JavaScript modal plugin to add dialogs to your site for lightboxes, user notifications, or completely custom content. ",
            Br(),
            A("Bootstrap documentation", href="http://getbootstrap.com/docs/5.1/components/modal/", target="_blank"),
            cls="text-gray-500"
        ),
        Div(
            Div(
                Button(
                    "Launch demo modal",
                    cls="btn btn-primary",
                    data_bs_toggle="modal",
                    data_bs_target="#modalProduct"
                ),
                cls="card-body border"
            ),
            cls="card"
        ),
        cls="px-md-10 py-10"
    )