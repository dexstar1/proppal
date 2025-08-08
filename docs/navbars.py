from fasthtml.common import *

def Navbars():
    return Section(
        H3("Navbar"),
        P(
            "Powerful and responsive navigation header, the navbar. Includes support for branding, navigation, and more, including support for the collapse plugin. ",
            Br(),
            A("Bootstrap documentation", href="http://getbootstrap.com/docs/5.1/components/navbar/", target="_blank"),
            cls="text-gray-500"
        ),
        P(
            "Shopper comes with multiple navbar combinations and layout options including vertical variation of the navbar component. Please see corresponding partials in ",
            Code("src/partials/"),
            " for code samples.",
            cls="text-gray-500"
        ),
        cls="px-md-10 py-10"
    )