from fasthtml.common import *
from controller.api import get_products

def product_grid():
    products = get_products()
    return Div(
        Div(
            *[Div(
                Img(src=prod[5], alt="product image", style="width:220px; height:auto;"), 
                cls="swiper-slide") for prod in products
            ],
            cls="swiper-wrapper"
        ),
        Div(cls="swiper-pagination"),
        Div(cls="swiper-button-prev"),
        Div(cls="swiper-button-next"), 
        id="product-grid",
        cls="flex justify-center align-center gap-4 w-[1000px] flex-wrap my-16 mx-auto swiper h-auto"
    )
