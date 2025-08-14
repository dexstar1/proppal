from fasthtml.common import *

def Sizing():
    return Section(
        H3('Sizing'), P('Responsive and viewport sizing utilities.', A('Bootstrap documentation', href='https://getbootstrap.com/docs/5.1/utilities/sizing/'), cls='text-gray-500'), Hr(), H5('Responsive'), Code('.w-{25|50|75|100|auto}, .h-{25|50|75|100|auto}'), '- default Bootstrap sizing utilities.', Code('.w-{breakpoint}-{25|50|75|100|auto}, .h-{breakpoint}-{25|50|75|100|auto}'), '- responsive sizing utilites.', Code('.min-w-{25|50|75|100|auto}, .min-h-{25|50|75|100|auto}'), '- sets the minimum width and height to a specified value.', Code('.min-w-{breakpoint}-{25|50|75|100|auto}, .min-h-{breakpoint}-{25|50|75|100|auto}'), '- responsive minimum width and height sizing utilities.', Hr(), H5('Viewport'), Code('.vw-50'), '- sets the width to 50% of the viewport width.',
        cls="px-md-10 py-10"
    )
