from fasthtml.common import *

def Shadow():
    return Section(
        H3('Shadow'), P('Shadow utilities.', A('Bootstrap documentation', href='https://getbootstrap.com/docs/5.1/utilities/shadows/'), cls='text-gray-500'), Hr(), H5('Border'), Code('.shadow-border'), "- adds a border-like box shadow. Useful if you don't want the border to affect element's positioning and sizing.", Code('.shadow-border-inset'), '- same as the above with the', Code('inset'), 'property set to true.', Hr(), H5('Hover'), Code('.shadow-hover'), '- adds a box shadow on hover.',
        cls="px-md-10 py-10"
    )
