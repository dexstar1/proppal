from fasthtml.common import *

def Ratio():
    return Section(
        H3('Ratio'), P('Responsive ratio utilities.', A('Bootstrap documentation', href='https://getbootstrap.com/docs/5.1/helpers/ratio/'), cls='text-gray-500'), Hr(), H5('Text'), Code('.ratio-item-text'), '- replacement for the default', Code('.ratio'), 'child element. Allows you to use text as the child of the', Code('.ratio'), 'container and centers it.',
        cls="px-md-10 py-10"
    )
