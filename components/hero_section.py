from fasthtml.common import *

def hero_section():
    return Section(
            Div(
                Div(
                    Div(
                            H1("Better Things In a Better Way", cls="display-4 mb-10"),
                            A("Shop Now", cls="link-underline text-reset mx-4 my-4"),
                            cls="col-12 col-md-7 col-lg-5 text-center text-white"
                    ),
                    cls="row justify-content-center align-items-center min-vh-100 pt-15 pb-12"
                ),
                cls="container d-flex flex-column",
            ),
            cls="mt-n12",
            style="text-align: center; padding: 20px; background-image: url('/assets/images/cover.jpg'); background-size:cover; background-repeat:no-repeat;height: 100vh; width: 100vw; display:flex;flex-direction:column;justify-content:center;align-items:center;"
        )
