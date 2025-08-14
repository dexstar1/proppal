from fasthtml.common import *

def Lift():
    return Section(
        H3('Lift'), P('Lifts utilities.', cls='text-gray-500'), Hr(), Code('.lift'), '- lifts an element on hover.',
        cls="px-md-10 py-10"
    )
