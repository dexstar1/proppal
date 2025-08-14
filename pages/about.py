from fasthtml.common import *

from wp_content import WPContent

def About():
    return Div(
        WPContent(),
        cls="my-page"
    )