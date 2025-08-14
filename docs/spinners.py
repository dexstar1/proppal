from fasthtml.common import *

def Spinners():
    return Section(
        H3('Spinners'), P('Indicate the loading state of a component or page with Bootstrap spinners.', A('Bootstrap documentation', href='https://getbootstrap.com/docs/5.1/components/spinners/'), cls='text-gray-500'), Div(Div(Div(Span('Loading...', cls='visually-hidden'), cls='spinner-border text-primary mb-1'), Div(Span('Loading...', cls='visually-hidden'), cls='spinner-grow text-primary mb-1'), Div(Span('Loading...', cls='visually-hidden'), cls='spinner-border text-secondary mb-1'), Div(Span('Loading...', cls='visually-hidden'), cls='spinner-grow text-secondary mb-1'), Div(Span('Loading...', cls='visually-hidden'), cls='spinner-border text-success mb-1'), Div(Span('Loading...', cls='visually-hidden'), cls='spinner-grow text-success mb-1'), Div(Span('Loading...', cls='visually-hidden'), cls='spinner-border text-danger mb-1'), Div(Span('Loading...', cls='visually-hidden'), cls='spinner-grow text-danger mb-1'), cls='card-body border'), cls='card'),
        cls="px-md-10 py-10"
    )
