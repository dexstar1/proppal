from fasthtml.common import *
from controller.api import get_products

def products_carousel():
    products = get_products()
    return Section(
    Div(
        Div(
            Div(
                H2('Product Carousel', cls='mb-10 text-center'),
                Div(
                    Div(
                        Div(
                            *[Div(
                                A(
                                    Img(src=prod[5], alt='...', cls='card-img-top'),
                                    Div(
                                        Div('Cropped cotton Top', cls='text-body'),
                                        Div('$', prod[3], cls='text-muted'),
                                        cls='card-body font-weight-bold text-center'
                                    ),
                                    href='product-2.html',
                                    cls='card shadow-hover'
                                ),
                                style='max-width: 229px; position: absolute;',
                                cls='col pt-3 pb-7 best-seller-prod'
                            ) for prod in products],
                            style='left: 0px; transform: translateX(-150%);',
                            cls='flickity-slider'
                        ),
                        style='height: 372.75px; touch-action: pan-y;',
                        cls='flickity-viewport'
                    ),
                    Button(
                        Svg(
                            Path(d='M 10,50 L 60,100 L 70,90 L 30,50  L 70,10 L 60,0 Z'),
                            viewbox='0 0 100 100',
                            cls='flickity-button-icon'
                        ),
                        type='button',
                        aria_label='Previous',
                        cls='flickity-button flickity-prev-next-button previous'
                    ),
                    Button(
                        Svg(
                            Path(d='M 10,50 L 60,100 L 70,90 L 30,50  L 70,10 L 60,0 Z', transform='translate(100, 100) rotate(180) '),
                            viewbox='0 0 100 100',
                            cls='flickity-button-icon'
                        ),
                        type='button',
                        aria_label='Next',
                        cls='flickity-button flickity-prev-next-button next'
                    ),
                    data_flickity='{"prevNextButtons": true}',
                    tabindex='0',
                    cls='flickity-buttons-lg flickity-buttons-offset px-lg-12 flickity-enabled is-draggable'
                ),
                cls='col-12'
            ),
            cls='row'
        ),
        cls='container'
    ),
    cls='pt-12 pb-10'
)
