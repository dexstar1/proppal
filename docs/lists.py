from fasthtml.common import *

def Lists():
    return Section(
        H3('List.js'),
        P(
            'Create searchable, sortable, and filterable lists and tables with the simple but powerful List.js plugin.',
            A('Plugin documentation', href='http://listjs.com/'),
            cls='text-gray-500'
        ),
        Code('data-list'),
        '- initializes the plugin.',
        Hr(),
        H5(),
        Div(
            Div(
                'Input group',
                Div(
                    'Button',
                    Div(
                        I('', cls='fe fe-search'),
                        cls='input-group-append'
                    ),
                    cls='input-group input-group-merge mb-6'
                ),
                'Form group',
                Div(
                    Div(
                        Div('Dsquared2', cls='form-check mb-3'),
                        Div('Alexander McQueen', cls='form-check mb-3'),
                        Div('Balenciaga', cls='form-check mb-3'),
                        Div('Adidas', cls='form-check mb-3'),
                        Div('Balmain', cls='form-check mb-3'),
                        Div('Burberry', cls='form-check mb-3'),
                        Div('Chloé', cls='form-check mb-3'),
                        Div('Kenzo', cls='form-check mb-3'),
                        Div('Givenchy', cls='form-check'),
                        cls='list'
                    ),
                    cls='form-group form-group-overflow mb-0'
                )
            ),
            cls='card-body border'
        ),
        Div(
            Code(
                '<div data-list=\'{"valueNames": ["name"]}\'>',
                '<!-- Input group -->',
                '<div class="input-group input-group-merge mb-6">',
                '<input class="form-control form-control-xs search" type="search" placeholder="Search Brand">',
                '<!-- Button -->',
                '<div class="input-group-append">',
                '<button class="btn btn-outline-border btn-xs">',
                '<i class="fe fe-search"></i>',
                '</button>',
                '</div>',
                '</div>',
                '<!-- Form group -->',
                '<div class="form-group form-group-overflow mb-0" id="brandGroup">',
                '<div class="list">',
                '<div class="form-check custom-checkbox mb-3">',
                '<input class="form-check-input" id="brandOne" type="checkbox">',
                '<label class="form-check-label name" for="brandOne">',
                'Dsquared2',
                '</label>',
                '</div>',
                '<div class="form-check custom-checkbox mb-3">',
                '<input class="form-check-input" id="brandTwo" type="checkbox" disabled>',
                '<label class="form-check-label name" for="brandTwo">',
                'Alexander McQueen',
                '</label>',
                '</div>',
                '<div class="form-check custom-checkbox mb-3">',
                '<input class="form-check-input" id="brandThree" type="checkbox">',
                '<label class="form-check-label name" for="brandThree">',
                'Balenciaga',
                '</label>',
                '</div>',
                '</div>',
                '</div>',
                '</div>',
                cls='highlight html'
            ),
            cls='card-footer fs-sm bg-dark'
        ),
        cls='card'
    ),
    cls="px-md-10 py-10"
    )
