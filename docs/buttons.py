from fasthtml.common import *

def Buttons():
    return Section(
        H3("Buttons"),
        P(
            "Use Bootstrap’s custom button styles for actions in forms, dialogs, and more with support for multiple sizes, states, and more. ",
            Br(),
            A("Bootstrap documentation", href="https://getbootstrap.com/docs/5.1/components/buttons/", target="_blank"),
            cls="text-gray-500"
        ),
        Div(
            Div(
                Button("Primary", type="button", cls="btn btn-primary"),
                Button("Secondary", type="button", cls="btn btn-secondary"),
                Button("Success", type="button", cls="btn btn-success"),
                Button("Danger", type="button", cls="btn btn-danger"),
                Button("Warning", type="button", cls="btn btn-warning"),
                Button("Info", type="button", cls="btn btn-info"),
                Button("Light", type="button", cls="btn btn-light"),
                Button("Dark", type="button", cls="btn btn-dark"),
                Button("Link", type="button", cls="btn btn-link"),
                cls="card-body border"
            ),
            cls="card mb-8"
        ),
        Hr(cls="my-7"),
        H5("Outline"),
        P(
            "In need of a button, but not the hefty background colors they bring? Replace the default modifier classes with the ",
            Code(".btn-outline-*"),
            " ones to remove all background images and colors on any button. Additionally we've added the ",
            Code(".btn-outline-border"),
            " modifier.",
            cls="text-gray-500"
        ),
        Div(
            Div(
                Button("Primary", type="button", cls="btn btn-outline-primary"),
                Button("Secondary", type="button", cls="btn btn-outline-secondary"),
                Button("Success", type="button", cls="btn btn-outline-success"),
                Button("Danger", type="button", cls="btn btn-outline-danger"),
                Button("Warning", type="button", cls="btn btn-outline-warning"),
                Button("Info", type="button", cls="btn btn-outline-info"),
                Button("Border", type="button", cls="btn btn-outline-border"),
                cls="card-body border"
            ),
            Div(
                Code(
                    '<button type="button" class="btn btn-outline-primary">Primary</button>\n...',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        Hr(cls="my-7"),
        H5("Sizes"),
        P(
            "Besides ",
            Code(".btn-lg"),
            " and ",
            Code(".btn-sm"),
            ", we've added ",
            Code(".btn-xs"),
            " and ",
            Code(".btn-xxs"),
            " for even smaller buttons.",
            cls="text-gray-500"
        ),
        Div(
            Div(
                Button("Large button", type="button", cls="btn btn-primary btn-lg"),
                Button("Basic button", type="button", cls="btn btn-secondary"),
                Button("Small button", type="button", cls="btn btn-success btn-sm"),
                Button("Extra small button", type="button", cls="btn btn-danger btn-xs"),
                Button("XXS button", type="button", cls="btn btn-warning btn-xxs"),
                cls="card-body border"
            ),
            Div(
                Code(
                    '<button type="button" class="btn btn-primary btn-lg">Large button</button>\n...',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        Hr(cls="my-7"),
        H5("Circle"),
        P(
            "Turn any button into a circle with a ",
            Code(".btn-rounded-cirle"),
            " modifier.",
            cls="text-gray-500"
        ),
        Div(
            Div(
                Button(I(cls="fe fe-check"), cls="btn btn-primary btn-circle btn-lg mb-1"),
                Button(I(cls="fe fe-check"), cls="btn btn-secondary btn-circle mb-1"),
                Button(I(cls="fe fe-check"), cls="btn btn-success btn-circle btn-sm mb-1"),
                Button(I(cls="fe fe-check"), cls="btn btn-danger btn-circle btn-xs mb-1"),
                Button(I(cls="fe fe-check"), cls="btn btn-warning btn-circle btn-xxs mb-1"),
                cls="card-body border"
            ),
            Div(
                Code(
                    '<button class="btn btn-primary btn-circle btn-lg mb-1"><i class="fe fe-check"></i></button>\n...',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        Hr(cls="my-7"),
        H5("Underline"),
        P(
            "Remove top, right, and left borders with a ",
            Code(".btn-underline"),
            " modifier.",
            cls="text-gray-500"
        ),
        Div(
            Div(
                Button("Primary", cls="btn btn-outline-primary btn-underline mb-1"),
                Button("Secodary", cls="btn btn-outline-secondary btn-underline mb-1"),
                Button("Success", cls="btn btn-outline-success btn-underline mb-1"),
                Button("Danger", cls="btn btn-outline-danger btn-underline mb-1"),
                Button("Warning", cls="btn btn-outline-warning btn-underline mb-1"),
                Button("Dark", cls="btn btn-outline-dark btn-underline mb-1"),
                Button("Border", cls="btn btn-outline-border btn-underline mb-1"),
                cls="card-body border"
            ),
            Div(
                Code(
                    '<button class="btn btn-outline-primary btn-underline mb-1">Primary</button>\n...',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        Hr(cls="my-7"),
        H5("Arrows"),
        P(
            "Simply add the Feather Icons left or right arrow icons to animate them on hover.",
            cls="text-gray-500"
        ),
        Div(
            Div(
                Button(
                    "Next Step ",
                    I(cls="fe fe-arrow-right ms-2"),
                    cls="btn btn-dark mb-1"
                ),
                Button(
                    I(cls="fe fe-arrow-left me-2"),
                    " Previous Step",
                    cls="btn btn-outline-border mb-1"
                ),
                cls="card-body border"
            ),
            Div(
                Code(
                    '<button class="btn btn-dark mb-1">Next Step <i class="fe fe-arrow-right ms-2"></i></button>\n...',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        Hr(cls="my-7"),
        H5("Brands"),
        P(
            "Popular brand colored buttons. Easily add more by extending the ",
            Code("$brand-colors"),
            " SCSS map in ",
            Code("variables.scss"),
            ".",
            cls="text-gray-500"
        ),
        Div(
            Div(
                Button("Facebook", cls="btn btn-facebook mb-1"),
                Button("Twitter", cls="btn btn-twitter mb-1"),
                Button("Pinterest", cls="btn btn-pinterest mb-1"),
                Button("LinkedIn", cls="btn btn-linkedin mb-1"),
                cls="card-body border"
            ),
            Div(
                Code(
                    '<button class="btn btn-facebook mb-1">Facebook</button>\n...',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        Hr(cls="my-7"),
        H5("Hover"),
        P(
            "Creates a pulse effect on hover. Works perfectly with circle buttons.",
            cls="text-gray-500"
        ),
        Div(
            Div(
                Button(I(cls="fe fe-heart"), cls="btn btn-lg btn-circle btn-hover btn-primary mb-1"),
                Button(I(cls="fe fe-heart"), cls="btn btn-circle btn-hover btn-secondary mb-1"),
                Button(I(cls="fe fe-heart"), cls="btn btn-sm btn-circle btn-hover btn-success mb-1"),
                Button(I(cls="fe fe-heart"), cls="btn btn-xs btn-circle btn-hover btn-warning mb-1"),
                Button(I(cls="fe fe-heart"), cls="btn btn-xxs btn-circle btn-hover btn-info mb-1"),
                cls="card-body border"
            ),
            Div(
                Code(
                    '<button class="btn btn-lg btn-circle btn-hover btn-primary mb-1"><i class="fe fe-heart"></i></button>\n...',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        cls="px-md-10 py-10"
    )