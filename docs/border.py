from fasthtml.common import *

def Border():
    return Section(
        H3('Border'), P('Border utilities to easily change border color and width, as well as make them responsive.', A('Bootstrap documentation', href='https://getbootstrap.com/docs/5.1/utilities/borders/'), cls='text-gray-500'), Hr(), H5('Responsive'), Code('.border-{breakpoint}, .border-top-{breakpoint}, .border-end-{breakpoint}, .border-bottom-{breakpoint}, .border-start-{breakpoint}'), '- adds a border at the specified and subsequent breakpoints.', Code('.border-{breakpoint}-0, .border-top-{breakpoint}-0, .border-end-{breakpoint}-0, .border-bottom-{breakpoint}-0, .border-start-{breakpoint}-0'), '- removes a border at the specified and subsequent breakpoints.', Hr(), H5('Colors'), Code('.border-gray-700'), '- changes the border color to', Code('$gray-700'), '.', Hr(), H5('Width'), Code('.border-2'), '- doubles the default border width.',
        cls="px-md-10 py-10"
    )
