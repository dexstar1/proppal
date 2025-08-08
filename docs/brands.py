from fasthtml.common import *

def Brands():
    return Section(
    H3("Brands"),
    P(
        "A simple brand component to easily add brand images of the same size. You can extend it with the ",
        Code(".lift"),
        " utility to add hover effects.",
        cls="text-gray-500"
    ),
    Div(
        Div(
            Div(
                Div(
                    A(
                        Img(cls="brand-img", src="../assets/img/brands/gray-350/mango.svg", alt="..."),
                        href="#!",
                        cls="brand lift mb-7 text-center"
                    ),
                    cls="col-6 col-sm-4 col-md-3 col-lg-2"
                ),
                Div(
                    A(
                        Img(cls="brand-img", src="../assets/img/brands/gray-350/zara.svg", alt="..."),
                        href="#!",
                        cls="brand lift mb-7 text-center"
                    ),
                    cls="col-6 col-sm-4 col-md-3 col-lg-2"
                ),
                Div(
                    A(
                        Img(cls="brand-img", src="../assets/img/brands/gray-350/reebok.svg", alt="..."),
                        href="#!",
                        cls="brand lift mb-7 text-center"
                    ),
                    cls="col-6 col-sm-4 col-md-3 col-lg-2"
                ),
                Div(
                    A(
                        Img(cls="brand-img", src="../assets/img/brands/gray-350/asos.svg", alt="..."),
                        href="#!",
                        cls="brand lift mb-7 text-center"
                    ),
                    cls="col-6 col-sm-4 col-md-3 col-lg-2"
                ),
                Div(
                    A(
                        Img(cls="brand-img", src="../assets/img/brands/gray-350/stradivarius.svg", alt="..."),
                        href="#!",
                        cls="brand lift mb-7 text-center"
                    ),
                    cls="col-6 col-sm-4 col-md-3 col-lg-2"
                ),
                cls="row"
            ),
            cls="card-body pb-0 bg-light"
        ),
        Div(
            Code(
                '<a class="brand lift text-center" href="#!"><img class="brand-img" src="../assets/img/brands/gray-350/mango.svg" alt="..."></a>',
                cls="highlight html hljs xml"
            ),
            cls="card-footer fs-sm bg-dark"
        ),
        cls="card"
    ),
    cls="px-md-10 py-10"
)