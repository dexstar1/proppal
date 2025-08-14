from fasthtml.common import *

def Position():
    return Section(
        H3('Position'), P('Position utilities.', cls='text-gray-500'), Hr(), Code('.cover'), '- positions an element absolutely to cover the whole area.', Code('.center'), '- centers an absolutely positioned element vertically and horizontally.',
        cls="px-md-10 py-10"
    )
