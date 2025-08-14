from fasthtml.common import *

def Jarallax():
    return Section(
        H3('Jarallax'), P('Smooth parallax scrolling effect for background images, videos and inline elements.', A('Plugin documentation', href='https://github.com/nk-o/jarallax'), cls='text-gray-500'), Div(Div(, cls='card-body py-14'), Div(Code('<div\xa0data-jarallax\xa0data-speed=".8"\xa0style="background-image:\xa0url(../assets/img/covers/cover-13.jpg);"></div>', cls='highlight html'), cls='card-footer fs-sm bg-dark'), cls='card'),
        cls="px-md-10 py-10"
    )
