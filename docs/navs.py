from fasthtml.common import *

def Navs():
    return Section(
        H3("Navs"),
        P(
            A("Bootstrap documentation", href="http://getbootstrap.com/docs/5.1/components/navs/", target="_blank"),
            cls="text-gray-500"
        ),
        Div(
            Div(
                Ul(
                    Li(A("Active", href="#!", cls="nav-link active"), cls="nav-item"),
                    Li(A("Link", href="#!", cls="nav-link"), cls="nav-item"),
                    Li(A("Link", href="#!", cls="nav-link"), cls="nav-item"),
                    Li(A("Disabled", href="#!", cls="nav-link disabled"), cls="nav-item"),
                    cls="nav"
                ),
                cls="card-body border"
            ),
            Div(
                Code(
                    '<ul class="nav">\n  <li class="nav-item">\n    <a class="nav-link active" href="#!">Active</a>\n  </li>\n  ...\n</ul>',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        Hr(cls="my-7"),
        H5("Unstyled"),
        P(
            "Removes the bottom underline of the ",
            Code(".active"),
            " link.",
            cls="text-gray-500"
        ),
        Div(
            Div(
                Ul(
                    Li(A("Active", href="#!", cls="nav-link active"), cls="nav-item"),
                    Li(A("Link", href="#!", cls="nav-link"), cls="nav-item"),
                    Li(A("Link", href="#!", cls="nav-link"), cls="nav-item"),
                    Li(A("Disabled", href="#!", cls="nav-link disabled"), cls="nav-item"),
                    cls="nav nav-unstyled"
                ),
                cls="card-body border"
            ),
            Div(
                Code(
                    '<ul class="nav nav-unstyled">\n  <li class="nav-item">\n    <a class="nav-link active" href="#!">Active</a>\n  </li>\n  ...\n</ul>',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        Hr(cls="my-7"),
        H5("Vertical"),
        P(
            "Positions the links vertically.",
            cls="text-gray-500"
        ),
        Div(
            Div(
                Ul(
                    Li(A("Active", href="#!", cls="nav-link active"), cls="nav-item"),
                    Li(A("Link", href="#!", cls="nav-link"), cls="nav-item"),
                    Li(A("Link", href="#!", cls="nav-link"), cls="nav-item"),
                    Li(A("Disabled", href="#!", cls="nav-link disabled"), cls="nav-item"),
                    cls="nav nav-vertical"
                ),
                cls="card-body border"
            ),
            Div(
                Code(
                    '<ul class="nav nav-vertical">\n  <li class="nav-item">\n    <a class="nav-link active" href="#!">Active</a>\n  </li>\n  ...\n</ul>',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        Hr(cls="my-7"),
        H5("Divider"),
        P(
            "Adds a divider between nav items.",
            cls="text-gray-500"
        ),
        Div(
            Div(
                Ul(
                    Li(A("Active", href="#!", cls="nav-link active"), cls="nav-item"),
                    Li(A("Link", href="#!", cls="nav-link"), cls="nav-item"),
                    Li(A("Link", href="#!", cls="nav-link"), cls="nav-item"),
                    Li(A("Disabled", href="#!", cls="nav-link disabled"), cls="nav-item"),
                    cls="nav nav-unstyled nav-divided"
                ),
                cls="card-body border"
            ),
            Div(
                Code(
                    '<ul class="nav nav-unstyled nav-divided">\n  <li class="nav-item">\n    <a class="nav-link active" href="#!">Active</a>\n  </li>\n  ...\n</ul>',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        Hr(cls="my-7"),
        H5("Tabs"),
        P(
            "Removes the horizontal padding of the first and last link and changes the underline styles. Works with ",
            Code(".nav-link"),
            " items as direct children of ",
            Code(".nav"),
            ".",
            cls="text-gray-500"
        ),
        Div(
            Div(
                Nav(
                    A("Active", href="#!", cls="nav-link active"),
                    A("Link", href="#!", cls="nav-link"),
                    A("Link", href="#!", cls="nav-link"),
                    A("Disabled", href="#!", cls="nav-link disabled"),
                    cls="nav nav-tabs"
                ),
                cls="card-body border"
            ),
            Div(
                Code(
                    '<nav class="nav nav-tabs">\n  <a class="nav-link active" href="#!">Active</a>\n  ...\n</nav>',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        Hr(cls="my-7"),
        H5("Overflow"),
        P(
            "Creates a horizontally scrollable variation of the nav component. Items do not get stacked if they don't fit the viewport. Instead, they stay on the same line and become scrollable in the x axes.",
            cls="text-gray-500"
        ),
        Div(
            Div(
                Nav(
                    A("Active", href="#!", cls="nav-link active"),
                    A("Link", href="#!", cls="nav-link"),
                    A("Link", href="#!", cls="nav-link"),
                    A("Disabled", href="#!", cls="nav-link disabled"),
                    cls="nav nav-overflow"
                ),
                cls="card-body border"
            ),
            Div(
                Code(
                    '<nav class="nav nav-overflow">\n  <a class="nav-link active" href="#!">Active</a>\n  ...\n</nav>',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        cls="px-md-10 py-10"
    )