from fasthtml.common import *

def BigPicture():
    return Section(
        H3('BigPicture'), P("Vanilla JavaScript image / video viewer. Doesn't sit on the DOM when inactive.", A('Plugin documentation', href='https://github.com/henrygd/bigpicture'), cls='text-gray-500'), Hr(), H5(), Div(Div(A(, href='#'), cls='card-body border'), Div(Code('<a\xa0href="#"\xa0data-bigpicture=\'{\xa0"ytSrc":\xa0"BGrY85i-skk"}\'>', '<img\xa0src="https://img.youtube.com/vi/BGrY85i-skk/maxresdefault.jpg"\xa0class="img-fluid"\xa0alt="..."\xa0style="max-width:\xa0320px;">', '</a>', cls='highlight html'), cls='card-footer fs-sm bg-dark'), cls='card'),
        cls="px-md-10 py-10"
    )
