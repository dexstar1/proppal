from fasthtml.common import *

def Popovers():
    return Section(
        H3("Popovers"),
        P(
            A("Bootstrap documentation", 
              href="http://getbootstrap.com/docs/5.1/components/popovers/", 
              target="_blank"),
            cls="text-gray-500"
        ),
        Div(
            Div(
                Button(
                    "Popover on top",
                    type="button",
                    cls="btn btn-primary mb-1",
                    data_bs_container="body",
                    data_bs_toggle="popover",
                    data_bs_placement="top",
                    data_bs_content="Vivamus sagittis lacus vel augue laoreet rutrum faucibus.",
                    data_bs_original_title="",
                    title=""
                ),
                Button(
                    "Popover on right",
                    type="button", 
                    cls="btn btn-secondary mb-1",
                    data_bs_container="body",
                    data_bs_toggle="popover",
                    data_bs_placement="right",
                    data_bs_content="Vivamus sagittis lacus vel augue laoreet rutrum faucibus.",
                    data_bs_original_title="",
                    title=""
                ),
                Button(
                    "Popover on bottom",
                    type="button",
                    cls="btn btn-success mb-1",
                    data_bs_container="body", 
                    data_bs_toggle="popover",
                    data_bs_placement="bottom",
                    data_bs_content="Vivamus sagittis lacus vel augue laoreet rutrum faucibus.",
                    data_bs_original_title="",
                    title=""
                ),
                Button(
                    "Popover on left",
                    type="button",
                    cls="btn btn-info mb-1",
                    data_bs_container="body",
                    data_bs_toggle="popover", 
                    data_bs_placement="left",
                    data_bs_content="Vivamus sagittis lacus vel augue laoreet rutrum faucibus.",
                    data_bs_original_title="",
                    title=""
                ),
                cls="card-body border"
            ),
            cls="card"
        ),
        cls="px-md-10 py-10"
    )