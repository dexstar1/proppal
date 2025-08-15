from fasthtml.common import *

def Toasts():
    return Section(
        H3('Toasts'),
        P(
            'Push notifications to your visitors with a toast, a lightweight and easily customizable alert message.',
            A('Bootstrap documentation', href='https://getbootstrap.com/docs/5.1/components/toasts/'),
            cls='text-gray-500'
        ),
        Hr(),
        H5(),
        Div(
            Div(
                Div(
                    Div('Bootstrap', '11 mins ago', cls='toast-header'),
                    Div('Hello, world! This is a toast message.', cls='toast-body'),
                    cls='toast fade show'
                ),
                cls='card-body border'
            ),
            Div(
                Code(
                    '<div\xa0class="toast"\xa0role="alert"\xa0aria-live="assertive"\xa0aria-atomic="true">',
                    '<div\xa0class="toast-header">',
                    '<strong\xa0class="me-auto">Bootstrap</strong>',
                    '<small>11\xa0mins\xa0ago</small>',
                    '<button\xa0type="button"\xa0class="btn-close"\xa0data-bs-dismiss="toast"\xa0aria-label="Close"></button>',
                    '</div>',
                    '<div\xa0class="toast-body">',
                    'Hello,\xa0world!\xa0This\xa0is\xa0a\xa0toast\xa0message.',
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
