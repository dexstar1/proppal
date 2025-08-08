from fasthtml.common import *

def Breadcrumb():
    return Section(
                H3("Breadcrumb"),
                P(
                    "Indicate the current page’s location within a navigational hierarchy that automatically adds separators via CSS. ",
                    Br(),
                    A("Bootstrap documentation", href="https://getbootstrap.com/docs/5.1/components/breadcrumb/", target="_blank"),
                    cls="text-gray-500"
                ),
                Div(
                    Div(
                        Ol(
                            Li(A("Home", href="index.html"), cls="breadcrumb-item"),
                            Li(A("Shop", href="shop.html"), cls="breadcrumb-item"),
                            Li("Product", cls="breadcrumb-item active"),
                            cls="breadcrumb mb-3"
                        ),
                        Ol(
                            Li(A("Home", href="index.html"), cls="breadcrumb-item"),
                            Li(A("Shop", href="shop.html"), cls="breadcrumb-item"),
                            Li("Product", cls="breadcrumb-item active"),
                            cls="breadcrumb mb-3 fs-xs"
                        ),
                        Ol(
                            Li(A("Home", href="index.html", cls="text-gray-400"), cls="breadcrumb-item"),
                            Li(A("Shop", href="shop.html", cls="text-gray-400"), cls="breadcrumb-item"),
                            Li("Product", cls="breadcrumb-item active"),
                            cls="breadcrumb mb-3 fs-xs text-gray-400"
                        ),
                        cls="card-body border"
                    ),
                    Div(
                        Code(
                            '<ol class="breadcrumb mb-3">\n'
                            '  <li class="breadcrumb-item">\n'
                            '    <a href="index.html">Home</a>\n'
                            '  </li>\n'
                            '  <li class="breadcrumb-item">\n'
                            '    <a href="shop.html">Shop</a>\n'
                            '  </li>\n'
                            '  <li class="breadcrumb-item active">\n'
                            '    Product\n'
                            '  </li>\n'
                            '</ol>\n\n'
                            '<ol class="breadcrumb mb-3 fs-xs">\n'
                            '  <li class="breadcrumb-item">\n'
                            '    <a href="index.html">Home</a>\n'
                            '  </li>\n'
                            '  <li class="breadcrumb-item">\n'
                            '    <a href="shop.html">Shop</a>\n'
                            '  </li>\n'
                            '  <li class="breadcrumb-item active">\n'
                            '    Product\n'
                            '  </li>\n'
                            '</ol>\n\n'
                            '<ol class="breadcrumb mb-3 fs-xs text-gray-400">\n'
                            '  <li class="breadcrumb-item">\n'
                            '    <a class="text-gray-400" href="index.html">Home</a>\n'
                            '  </li>\n'
                            '  <li class="breadcrumb-item">\n'
                            '    <a class="text-gray-400" href="shop.html">Shop</a>\n'
                            '  </li>\n'
                            '  <li class="breadcrumb-item active">\n'
                            '    Product\n'
                            '  </li>\n'
                            '</ol>',
                            cls="highlight html hljs xml"
                        ),
                        cls="card-footer fs-sm bg-dark"
                    ),
                    cls="card"
                ),
                cls="px-md-10 py"
            )