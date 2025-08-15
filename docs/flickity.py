from fasthtml.common import *

def Flickity():
    return Section(
        H3('Flickity'),
        P(
            'Touch, responsive, flickable carousels.',
            A('Plugin documentation', href='https://flickity.metafizzy.co/'),
            cls='text-gray-500'
        ),
        Div(
            Div(
                Div('', cls='col-12 col-md-3 px-1'),
                Div('', cls='col-12 col-md-3 px-1'),
                Div('', cls='col-12 col-md-3 px-1'),
                Div('', cls='col-12 col-md-3 px-1'),
                Div('', cls='col-12 col-md-3 px-1'),
                cls='card-body border'
            ),
            Div(
                Code(
                    '<div data-flickity=\'{"prevNextButtons": true}\'>',
                    '<div class="col-12 col-md-3 px-1">',
                    '<img src="../assets/img/products/product-25.jpg" class="img-fluid" alt="...">',
                    '</div>',
                    '<div class="col-12 col-md-3 px-1">',
                    '<img src="../assets/img/products/product-26.jpg" class="img-fluid" alt="...">',
                    '</div>',
                    '<div class="col-12 col-md-3 px-1">',
                    '<img src="../assets/img/products/product-27.jpg" class="img-fluid" alt="...">',
                    '</div>',
                    '<div class="col-12 col-md-3 px-1">',
                    '<img src="../assets/img/products/product-28.jpg" class="img-fluid" alt="...">',
                    '</div>',
                    '<div class="col-12 col-md-3 px-1">',
                    '<img src="../assets/img/products/product-29.jpg" class="img-fluid" alt="...">',
                    '</div>',
                    '</div>',
                    cls='highlight html'
                ),
                cls='card-footer fs-sm bg-dark'
            ),
            cls='card'
        ),
        Hr(),
        H5('Responsive initialization'),
        P(
            'Easily initialize Flickity depending on the viewport width with',
            Code('.flickity-{breakpoint}'),
            'or',
            Code('.flickity-{breakpoint}-none'),
            'modifiers. Flickity will be enabled or disabled at the specified and all subsequent breakpoints. Requires',
            Code('watchCSS'),
            'to be set to',
            Code('true'),
            '.',
            cls='text-gray-500'
        ),
        Div(
            Div(
                Div('', cls='col-12 col-md-3 px-1'),
                Div('', cls='col-12 col-md-3 px-1'),
                Div('', cls='col-12 col-md-3 px-1'),
                Div('', cls='col-12 col-md-3 px-1'),
                Div('', cls='col-12 col-md-3 px-1'),
                cls='flickity-none flickity-md'
            ),
            cls='card-body border'
        ),
        Div(
            Code(
                '<div class="flickity-none flickity-md" data-flickity=\'{"watchCSS": true}\'>',
                '<div class="col-12 col-md-3 px-1">',
                '<img src="../assets/img/products/product-25.jpg" class="img-fluid" alt="...">',
                '</div>',
                '<div class="col-12 col-md-3 px-1">',
                '<img src="../assets/img/products/product-26.jpg" class="img-fluid" alt="...">',
                '</div>',
                '<div class="col-12 col-md-3 px-1">',
                '<img src="../assets/img/products/product-27.jpg" class="img-fluid" alt="...">',
                '</div>',
                '<div class="col-12 col-md-3 px-1">',
                '<img src="../assets/img/products/product-28.jpg" class="img-fluid" alt="...">',
                '</div>',
                '<div class="col-12 col-md-3 px-1">',
                '<img src="../assets/img/products/product-29.jpg" class="img-fluid" alt="...">',
                '</div>',
                '</div>',
                cls='highlight html'
            ),
            cls='card-footer fs-sm bg-dark'
        ),
        cls="px-md-10 py-10"
    )
