from fasthtml.common import *

def Lists():
    return Section(
        H3("Lists"),
        P(
            "List groups are a flexible and powerful component for displaying a series of content. Modify and extend them to support just about any content within. ",
            Br(),
            A("Bootstrap documentation", href="http://getbootstrap.com/docs/5.1/components/list-group/", target="_blank"),
            cls="text-gray-500"
        ),
        Div(
            Div(
                Ul(
                    Li("Cras justo odio", cls="list-group-item active"),
                    Li("Dapibus ac facilisis in", cls="list-group-item"),
                    Li("Morbi leo risus", cls="list-group-item"),
                    Li("Porta ac consectetur ac", cls="list-group-item"),
                    cls="list-group"
                ),
                cls="card-body border"
            ),
            cls="card"
        ),
        Hr(cls="my-7"),
        H5("Sizing"),
        P(
            "Change ",
            Code(".list-group-item"),
            " padding with three sizing options.",
            cls="text-gray-500"
        ),
        Div(
            Div(
                Ul(
                    Li("Cras justo odio", cls="list-group-item active"),
                    Li("Dapibus ac facilisis in", cls="list-group-item"),
                    Li("Morbi leo risus", cls="list-group-item"),
                    cls="list-group list-group-lg mb-5"
                ),
                Ul(
                    Li("Cras justo odio", cls="list-group-item active"),
                    Li("Dapibus ac facilisis in", cls="list-group-item"),
                    Li("Morbi leo risus", cls="list-group-item"),
                    cls="list-group mb-5"
                ),
                Ul(
                    Li("Cras justo odio", cls="list-group-item active"),
                    Li("Dapibus ac facilisis in", cls="list-group-item"),
                    Li("Morbi leo risus", cls="list-group-item"),
                    cls="list-group list-group-sm"
                ),
                cls="card-body border"
            ),
            Div(
                Code(
                    '<ul class="list-group list-group-lg mb-5">\n    <li class="list-group-item active">Cras justo odio</li>\n    <li class="list-group-item">Dapibus ac facilisis in</li>\n    <li class="list-group-item">Morbi leo risus</li>\n</ul>\n...',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        Hr(cls="my-7"),
        H5("Flush"),
        P(
            "Add ",
            Code(".list-group-flush"),
            " to remove some borders and rounded corners to render list group items edge-to-edge in a parent container (e.g., cards).",
            cls="text-gray-500"
        ),
        Div(
            Div(
                Ul(
                    Li("Cras justo odio", cls="list-group-item active"),
                    Li("Dapibus ac facilisis in", cls="list-group-item"),
                    Li("Morbi leo risus", cls="list-group-item"),
                    cls="list-group list-group-flush"
                ),
                cls="card-body border"
            ),
            Div(
                Code(
                    '<ul class="list-group list-group-flush">\n    <li class="list-group-item active">Cras justo odio</li>\n    <li class="list-group-item">Dapibus ac facilisis in</li>\n    <li class="list-group-item">Morbi leo risus</li>\n</ul>',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card mb-6"
        ),
        P(
            "Additionally use ",
            Code(".list-group-flush-x"),
            " or ",
            Code(".list-group-flush-y"),
            " to remove only vertical or horizontal borders and paddings of a ",
            Code(".list-group"),
            ".",
            cls="text-gray-500"
        ),
        cls="px-md-10 py-10"
    )