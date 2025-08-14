from fasthtml.common import *

def ToolTips():
    return Section(
        H3('Tooltips'), P(A('Bootstrap documentation', href='http://getbootstrap.com/docs/5.1/components/tooltips/'), cls='text-gray-500'), Div(Div('Tooltip on top', 'Tooltip on right', 'Tooltip on bottom', 'Tooltip on left', cls='card-body border'), cls='card'),
        cls="px-md-10 py-10"
    )
