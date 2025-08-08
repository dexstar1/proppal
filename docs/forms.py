from fasthtml.common import *

def Forms():
    return Section(
        H3("Form"),
        P(
            "Shopper supports all of Bootstrap's default form styling in addition to a handful of new input types and features. ",
            Br(),
            A("Bootstrap documentation", href="https://getbootstrap.com/docs/5.1/forms/overview/", target="_blank"),
            cls="text-gray-500"
        ),
        Div(
            Div(
                Form(
                    Div(
                        Label("Email address", cls="form-label", for_="exampleInputEmail1"),
                        Input(type="email", cls="form-control", id="exampleInputEmail1", placeholder="Enter email"),
                        cls="form-group"
                    ),
                    Div(
                        Label("Password", cls="form-label", for_="exampleInputPassword1"),
                        Input(type="password", cls="form-control", id="exampleInputPassword1", placeholder="Password"),
                        cls="form-group"
                    ),
                    Button("Submit", type="submit", cls="btn btn-primary")
                ),
                cls="card-body border"
            ),
            cls="card"
        ),
        Hr(cls="my-7"),
        H5("Input group"),
        P(
            "Easily extend form controls by adding text, buttons, or button groups on either side of textual inputs, custom selects, and custom file inputs.",
            cls="text-gray-500"
        ),
        Div(
            Div(
                Div(
                    Div(
                        Span("@", cls="input-group-text", id="basic-addon1"),
                        cls="input-group-prepend"
                    ),
                    Input(type="text", cls="form-control", placeholder="Username", aria_label="Username", aria_describedby="basic-addon1"),
                    cls="input-group mb-3"
                ),
                Div(
                    Input(type="text", cls="form-control", placeholder="Recipient's username", aria_label="Recipient's username", aria_describedby="basic-addon2"),
                    Div(
                        Span("@example.com", cls="input-group-text", id="basic-addon2"),
                        cls="input-group-append"
                    ),
                    cls="input-group"
                ),
                cls="card-body border"
            ),
            cls="card"
        ),
        Hr(cls="my-7"),
        H5("Sizing"),
        P(
            "Set heights using classes like .form-control-lg and .form-control-sm.",
            cls="text-gray-500"
        ),
        Div(
            Div(
                Div(
                    Input(type="text", cls="form-control form-control-lg", placeholder=".form-control-lg"),
                    cls="form-group"
                ),
                Div(
                    Input(type="text", cls="form-control", placeholder=".form-control"),
                    cls="form-group"
                ),
                Div(
                    Input(type="text", cls="form-control form-control-sm", placeholder=".form-control-sm"),
                    cls="form-group"
                ),
                Div(
                    Input(type="text", cls="form-control form-control-xs", placeholder=".form-control-xs"),
                    cls="form-group"
                ),
                Div(
                    Input(type="text", cls="form-control form-control-xxs", placeholder=".form-control-xxs"),
                    cls="form-group"
                ),
                cls="card-body border"
            ),
            Div(
                Code(
                    '<div class="form-group">\n  <input type="text" class="form-control form-control-lg" placeholder=".form-control-lg">\n</div>\n...',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        Hr(cls="my-7"),
        H5("Underline"),
        P(
            "Removes top, right, and left borders of a ",
            Code(".form-control"),
            ".",
            cls="text-gray-500"
        ),
        Div(
            Div(
                Div(
                    Input(type="text", cls="form-control form-control-underline", placeholder=".form-control-underline"),
                    cls="form-group"
                ),
                cls="card-body border"
            ),
            Div(
                Code(
                    '<div class="form-group">\n  <input type="text" class="form-control form-control-underline" placeholder=".form-control-underline">\n</div>',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        Hr(cls="my-7"),
        H5("Input group merge"),
        P(
            "A slightly modified version of the default input groups that always keeps icons as a part of the form control.",
            cls="text-gray-500"
        ),
        Div(
            Div(
                Div(
                    Input(cls="form-control", type="search", placeholder="Search"),
                    Div(
                        Button(
                            I(cls="fe fe-search"),
                            type="submit",
                            cls="btn btn-outline-border"
                        ),
                        cls="input-group-append"
                    ),
                    cls="input-group input-group-merge"
                ),
                cls="card-body border"
            ),
            Div(
                Code(
                    '<div class="input-group input-group-merge">\n  <input class="form-control" type="search" placeholder="Search">\n  <div class="input-group-append">\n    <button class="btn btn-outline-border" type="submit">\n      <i class="fe fe-search"></i>\n    </button>\n  </div>\n</div>',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        Hr(cls="my-7"),
        H5("Form select"),
        P(
            "Customize the native ",
            Code("<select>"),
            "s with custom CSS that changes the element’s initial appearance.",
            cls="text-gray-500"
        ),
        Div(
            Div(
                Select(
                    Option("Open this select menu", selected=True),
                    Option("One", value="1"),
                    Option("Two", value="2"),
                    Option("Three", value="3"),
                    cls="form-select",
                    aria_label="Default select example"
                ),
                cls="card-body border"
            ),
            Div(
                Code(
                    '<select class="form-select">\n  <option selected="">Open this select menu</option>\n  <option value="1">One</option>\n  <option value="2">Two</option>\n  <option value="3">Three</option>\n</select>',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        Hr(cls="my-7"),
        H5("Form check"),
        P(
            "For even more customization and cross browser consistency, use our completely custom form elements to replace the browser defaults. They’re built on top of semantic and accessible markup, so they’re solid replacements for any default form control.",
            cls="text-gray-500"
        ),
        Div(
            Div(
                Div(
                    Input(cls="form-check-input", type="checkbox", id="inlineCheckbox1", value="option1"),
                    Label("Check this custom checkbox", cls="form-check-label", for_="inlineCheckbox1"),
                    cls="form-check form-check-inline"
                ),
                cls="card-body border"
            ),
            Div(
                Code(
                    '<div class="form-check form-check-inline">\n  <input class="form-check-input" type="checkbox" id="inlineCheckbox1" value="option1">\n  <label class="form-check-label" for="inlineCheckbox1">Check this custom checkbox</label>\n</div>',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        Hr(),
        Div(
            Div(
                Div(
                    Input(cls="form-check-input", type="radio", name="inlineRadioOptions", id="inlineRadio1", value="option1"),
                    Label("Toggle this custom radio", cls="form-check-label", for_="inlineRadio1"),
                    cls="form-check"
                ),
                Div(
                    Input(cls="form-check-input", type="radio", name="inlineRadioOptions", id="inlineRadio2", value="option2"),
                    Label("Or toggle this other custom radio", cls="form-check-label", for_="inlineRadio2"),
                    cls="form-check"
                ),
                cls="card-body border"
            ),
            Div(
                Code(
                    '<div class="form-check">\n  <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio1" value="option1">\n  <label class="form-check-label" for="inlineRadio1">Toggle this custom radio</label>\n</div>\n...',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        Hr(),
        Div(
            Div(
                Div(
                    Input(cls="form-check-input", type="checkbox", id="customColor1", style="background-color: red"),
                    Label("Custom color checkbox / radio", cls="form-check-label", for_="customColor1"),
                    cls="form-check form-check-inline form-check-color"
                ),
                cls="card-body border"
            ),
            Div(
                Code(
                    '<div class="form-check form-check-inline form-check-color">\n  <input class="form-check-input" type="checkbox" id="customColor1" style="background-color: red">\n  <label class="form-check-label" for="customColor1">Custom color checkbox / radio</label>\n</div>',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        Hr(),
        Div(
            Div(
                Div(
                    Input(cls="form-check-input", type="checkbox", id="customText1"),
                    Label("Custom text checkbox / radio", cls="form-check-label", for_="customText1"),
                    cls="form-check form-check-inline form-check-text"
                ),
                cls="card-body border"
            ),
            Div(
                Code(
                    '<div class="form-check form-check-inline form-check-text">\n  <input class="form-check-input" type="checkbox" id="customText1">\n  <label class="form-check-label" for="customText1">Custom text checkbox / radio</label>\n</div>',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        Hr(),
        Div(
            Div(
                Div(
                    Input(cls="form-check-input", type="checkbox", id="customImage1", style="background-image: url(../assets/img/products/product-7.jpg);"),
                    Label("", cls="form-check-label", for_="customImage1"),
                    cls="form-check form-check-img"
                ),
                cls="card-body border"
            ),
            Div(
                Code(
                    '<div class="form-check form-check-img">\n  <input class="form-check-input" type="checkbox" id="customImage1" style="background-image: url(../assets/img/products/product-7.jpg);">\n  <label class="form-check-label" for="customImage1"></label>\n</div>',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        Hr(),
        Div(
            Div(
                Div(
                    Input(cls="form-check-input", type="checkbox", id="customSize1"),
                    Label("XXS", cls="form-check-label", for_="customSize1"),
                    cls="form-check form-check-size"
                ),
                cls="card-body border"
            ),
            Div(
                Code(
                    '<div class="form-check form-check-size">\n  <input class="form-check-input" type="checkbox" id="customSize1">\n  <label class="form-check-label" for="customSize1">XXS</label>\n</div>',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        Hr(),
        Div(
            Div(
                Div(
                    Input(cls="form-check-input", type="checkbox", role="switch", id="flexSwitchCheckDefault"),
                    Label("Default switch checkbox input", cls="form-check-label", for_="flexSwitchCheckDefault"),
                    cls="form-check form-switch"
                ),
                cls="card-body border"
            ),
            Div(
                Code(
                    '<div class="form-check form-switch">\n  <input class="form-check-input" type="checkbox" role="switch" id="flexSwitchCheckDefault">\n  <label class="form-check-label" for="flexSwitchCheckDefault">Default switch checkbox input</label>\n</div>',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        cls="px-md-10 py-10"
    )