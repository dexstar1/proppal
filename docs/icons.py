from fasthtml.common import *

def Icons():
    return Section(
        H3("Icons"),
        P(
            "The following icon sets are used in Shopper. Please go to their official documentation pages for a full list of icons:",
            cls="text-gray-500"
        ),
        Ul(
            Li(
                A("Font Awesome", href="https://fontawesome.com/", target="_blank")
            ),
            Li(
                A("Feather Icons", href="https://feathericons.com/", target="_blank")
            ),
            Li(
                A("Beauty Icon Pack designed by Flaticon", href="https://www.flaticon.com/packs/beauty-9", target="_blank")
            )
        ),
        cls="px-md-10 py-10"
    )