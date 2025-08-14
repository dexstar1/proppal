from fasthtml.common import *

def WPContent():
    return Section(
        Div(cls='wp-block-group alignfull has-global-padding is-layout-constrained wp-container-core-group-is-layout-22 wp-block-group-is-layout-constrained'),
        cls='wp-content'
    )
