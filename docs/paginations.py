from fasthtml.common import *

def Paginations():
    return Section(
        H3("Pagination"),
        P(
            "Indicates a series of related content exists across multiple pages. ",
            Br(),
            A("Bootstrap documentation", 
              href="http://getbootstrap.com/docs/5.1/components/pagination/", 
              target="_blank"),
            cls="text-gray-500"
        ),
        Div(
            Div(
                # Large Pagination
                Ul(
                    Li(
                        A(
                            I(cls="fa fa-caret-left"),
                            cls="page-link page-link-arrow",
                            href="#"
                        ),
                        cls="page-item"
                    ),
                    Li(A("1", href="#", cls="page-link"), cls="page-item active"),
                    Li(A("2", href="#", cls="page-link"), cls="page-item"),
                    Li(A("3", href="#", cls="page-link"), cls="page-item"),
                    Li(A("4", href="#", cls="page-link"), cls="page-item"),
                    Li(A("5", href="#", cls="page-link"), cls="page-item"),
                    Li(A("6", href="#", cls="page-link"), cls="page-item"),
                    Li(
                        A(
                            I(cls="fa fa-caret-right"),
                            cls="page-link page-link-arrow",
                            href="#"
                        ),
                        cls="page-item"
                    ),
                    cls="pagination pagination-lg mb-5"
                ),
                
                # Default Pagination
                Ul(
                    Li(
                        A(
                            I(cls="fa fa-caret-left"),
                            cls="page-link page-link-arrow",
                            href="#"
                        ),
                        cls="page-item"
                    ),
                    Li(A("1", href="#", cls="page-link"), cls="page-item active"),
                    Li(A("2", href="#", cls="page-link"), cls="page-item"),
                    Li(A("3", href="#", cls="page-link"), cls="page-item"),
                    Li(A("4", href="#", cls="page-link"), cls="page-item"),
                    Li(A("5", href="#", cls="page-link"), cls="page-item"),
                    Li(A("6", href="#", cls="page-link"), cls="page-item"),
                    Li(
                        A(
                            I(cls="fa fa-caret-right"),
                            cls="page-link page-link-arrow",
                            href="#"
                        ),
                        cls="page-item"
                    ),
                    cls="pagination mb-5"
                ),
                
                # Small Pagination 
                Ul(
                    Li(
                        A(
                            I(cls="fa fa-caret-left"),
                            cls="page-link page-link-arrow",
                            href="#"
                        ),
                        cls="page-item"
                    ),
                    Li(A("1", href="#", cls="page-link"), cls="page-item active"),
                    Li(A("2", href="#", cls="page-link"), cls="page-item"),
                    Li(A("3", href="#", cls="page-link"), cls="page-item"),
                    Li(A("4", href="#", cls="page-link"), cls="page-item"),
                    Li(A("5", href="#", cls="page-link"), cls="page-item"),
                    Li(A("6", href="#", cls="page-link"), cls="page-item"),
                    Li(
                        A(
                            I(cls="fa fa-caret-right"),
                            cls="page-link page-link-arrow",
                            href="#"
                        ),
                        cls="page-item"
                    ),
                    cls="pagination pagination-sm"
                ),
                cls="card-body border"
            ),
            Div(
                Code(
                    '<ul class="pagination pagination-lg">\n  <li class="page-item">\n    <a class="page-link page-link-arrow" href="#">\n      <i class="fa fa-caret-left"></i>\n    </a>\n  </li>\n  <li class="page-item active">\n    <a class="page-link" href="#">...</a>\n  </li>\n  <li class="page-item">\n    <a class="page-link page-link-arrow" href="#">\n      <i class="fa fa-caret-right"></i>\n    </a>\n  </li>\n</ul>',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        cls="px-md-10 py-10"
    )