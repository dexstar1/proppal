from fasthtml.common import *

from fasthtml.common import *

def Shadow():
    return Section(
        H3("Shadow"),
        P(
            "Add or remove shadows to elements with box-shadow utilities.", 
            cls="text-gray-500"
        ),
        Hr(cls="my-7"),
        
        # Example section
        H5("Example"),
        Div(
            Div(
                Div(
                    "No shadow",
                    cls="shadow-none p-4 mb-6 bg-white"
                ),
                Div(
                    "Small shadow",
                    cls="shadow-sm p-4 mb-6 bg-white"
                ),
                Div(
                    "Regular shadow",
                    cls="shadow p-4 mb-6 bg-white"
                ),
                Div(
                    "Larger shadow",
                    cls="shadow-lg p-4 bg-white"
                ),
                cls="card-body border"
            ),
            Div(
                Code(
                    '<div class="shadow-none">No shadow</div>\n'
                    '<div class="shadow-sm">Small shadow</div>\n'
                    '<div class="shadow">Regular shadow</div>\n'
                    '<div class="shadow-lg">Larger shadow</div>',
                    cls="highlight html"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        cls="px-md-10 py-10"
    )
