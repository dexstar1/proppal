from fasthtml.common import *

def BigPicture():
    return Section(
        H3('BigPicture'),
        P(
            "Vanilla JavaScript image / video viewer. Doesn't sit on the DOM when inactive.",
            A('Plugin documentation', href='https://github.com/henrygd/bigpicture'),
            cls='text-gray-500'
        ),
        Hr(),
        H5(),
        Div(
            Div(
                A(
                    '',  # Empty anchor text
                    href='#'
                ),
                cls='card-body border'
            ),
            Div(
                Code(
                    '<a href="#" data-bigpicture=\'{ "ytSrc": "BGrY85i-skk"}\'>',
                    '<img src="https://img.youtube.com/vi/BGrY85i-skk/maxresdefault.jpg" class="img-fluid" alt="..." style="max-width: 320px;">',
                    '</a>',
                    cls='highlight html'
                ),
                cls='card-footer fs-sm bg-dark'
            ),
            cls='card'
        ),
        cls="px-md-10 py-10"
    )
