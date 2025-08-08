from fasthtml.common import *

def Dropdowns():
    return Section(
        H3("Dropdowns"),
        P(
            "Toggle contextual overlays for displaying lists of links and more with the Bootstrap dropdown plugin. Dropdown menus are toggled on hover in navigation panels.",
            Br(),
            A("Bootstrap documentation", href="https://getbootstrap.com/docs/5.1/components/dropdowns/", target="_blank"),
            cls="text-gray-500"
        ),
        Div(
            Div(
                Div(
                    # Dropdown
                    Div(
                        Button(
                            "Dropdown menu",
                            cls="btn btn-primary dropdown-toggle",
                            type="button",
                            id="dropdownMenuButton",
                            data_bs_toggle="dropdown",
                            aria_haspopup="true",
                            aria_expanded="false",
                            data_display="static"
                        ),
                        Div(
                            A("Action", href="#!", cls="dropdown-item"),
                            A("Another action", href="#!", cls="dropdown-item"),
                            A("Something else here", href="#!", cls="dropdown-item"),
                            cls="dropdown-menu",
                            aria_labelledby="dropdownMenuButton"
                        ),
                        cls="dropdown"
                    ),
                    cls="card-body border"
                ),
                cls="card"
            ),
        ),
        Hr(cls="my-7"),
        H5("Cards"),
        P(
            "You can use the ",
            Code(".card"),
            " and ",
            Code(".list-styled"),
            " components inside dropdowns to achieve a different look of your dropdown menus.",
            cls="text-gray-500"
        ),
        Div(
            Div(
                Div(
                    # Dropdown with card menu
                    Div(
                        Button(
                            "Dropdown card",
                            cls="btn btn-secondary dropdown-toggle",
                            type="button",
                            id="dropdownMenuButtonTwo",
                            data_bs_toggle="dropdown",
                            aria_haspopup="true",
                            aria_expanded="false"
                        ),
                        Div(
                            Div(
                                Div(
                                    Ul(
                                        Li(A("Action", href="#!", cls="list-styled-link"), cls="list-styled-item"),
                                        Li(A("Another action", href="#!", cls="list-styled-link"), cls="list-styled-item"),
                                        Li(A("Something else here", href="#!", cls="list-styled-link"), cls="list-styled-item"),
                                        cls="list-styled mb-0"
                                    ),
                                    cls="card-body"
                                ),
                                cls="card"
                            ),
                            cls="dropdown-menu",
                            aria_labelledby="dropdownMenuButtonTwo"
                        ),
                        cls="dropdown"
                    ),
                    cls="card-body border"
                ),
                Div(
                    Code(
                        '<div class="dropdown">\n  <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButtonTwo" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Dropdown card</button>\n  <div class="dropdown-menu" aria-labelledby="dropdownMenuButtonTwo">\n    <div class="card">\n      <div class="card-body">\n        <ul class="list-styled mb-0">\n          <li class="list-styled-item"><a class="list-styled-link" href="#!">Action</a></li>\n          <li class="list-styled-item"><a class="list-styled-link" href="#!">Another action</a></li>\n          <li class="list-styled-item"><a class="list-styled-link" href="#!">Something else here</a></li>\n        </ul>\n      </div>\n    </div>\n  </div>\n</div>',
                        cls="highlight html hljs xml"
                    ),
                    cls="card-footer fs-sm bg-dark"
                ),
                cls="card"
            ),
        ),
        cls="px-md-10 py-10"
    )