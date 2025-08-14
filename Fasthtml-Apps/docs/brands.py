from fasthtml.common import *

def Brands():
    return Div(
        H1("Brands", cls="mb-4"),
        P("Explore our collection of brands that offer a variety of products and services. Each brand is carefully selected to ensure quality and satisfaction."),
        Div(
            H2("Brand A", cls="mt-5"),
            P("Brand A is known for its innovative products and commitment to sustainability."),
            cls="px-md-10 py-10"
        ),
        Div(
            H2("Brand B", cls="mt-5"),
            P("Brand B offers a wide range of products that cater to different customer needs."),
            cls="px-md-10 py-10"
        ),
        Div(
            H2("Brand C", cls="mt-5"),
            P("Brand C specializes in high-quality goods and exceptional customer service."),
            cls="px-md-10 py-10"
        ),
        cls="container"
    )