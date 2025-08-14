from fasthtml.common import *

def nav():
    return Nav(
                Button(
                    Span(cls="navbar-toggler-icon"),
                    cls="navbar-toggler",
                    type="button",
                    data_bs_toggle="collapse",
                    data_bs_target="#docsCollapse",
                    aria_controls="docsCollapse",
                    aria_expanded="false",
                    aria_label="Toggle navigation"
                ),
                Div(
                    Nav(
                        P(
                            'Getting Started',
                            cls="mb-5 fs-xxs fw-bold text-uppercase"
                        ),
                        Ul(
                            Li(
                                A(
                                  'Introduction',  href="#", cls="list-styled-link"
                                ),
                                cls="list-styled-item"
                            ),
                            Li(
                                A(
                                  'Changelog',  href="#", cls="list-styled-link"
                                ),
                                cls="list-styled-item"
                            ),
                            cls="list-styled"
                        ),
                        P('Component', cls="mt-7 mb-5 fs-xxs fw-bold text-uppercase"),
                        Ul(
                            Li(A('Alerts', href="../docs/alerts.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Avatars', href="../docs/avatars.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Badges', href="../docs/badges.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Brands', href="../docs/brands.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Breadcrumb', href="../docs/breadcrumbs.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Buttons', href="../docs/buttons.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Cards', href="../docs/cards.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Dropdowns', href="../docs/dropdowns.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Form', href="../docs/form.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Icons', href="../docs/icons.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Lists', href="../docs/lists.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Modals', href="../docs/modals.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Navbar', href="../docs/navbar.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Navs', href="../docs/navs.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Pagination', href="../docs/pagination.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Popovers', href="../docs/popovers.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Progress', href="../docs/progress.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Rate', href="../docs/rate.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Rating', href="../docs/rating.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Review', href="../docs/review.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Spinners', href="../docs/spinners.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Tables', href="../docs/tables.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Toasts', href="../docs/toasts.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Tooltips', href="../docs/tooltips.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Typography', href="../docs/typography.html", cls="list-styled-link"), cls="list-styled-item"),
                            cls="list-styled"
                        ),
                        P('Plugins', cls="mt-7 mb-5 fs-xxs fw-bold text-uppercase"),
                        Ul(
                            Li(A('BigPicture', href="../docs/bigpicture.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Flickity', href="../docs/flickity.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Jarallax', href="../docs/jarallax.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('List.js', href="../docs/listjs.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Map', href="../docs/map.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Simplebar', href="../docs/simplebar.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Smooth Scroll', href="../docs/smooth-scroll.html", cls="list-styled-link"), cls="list-styled-item"),
                            cls="list-styled"
                        ),
                        P('Utilities', cls="mt-7 mb-5 fs-xxs fw-bold text-uppercase"),
                        Ul(
                            Li(A('Background', href="../docs/background.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Border', href="../docs/border.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Lift', href="../docs/lift.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Opacity', href="../docs/opacity.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Position', href="../docs/position.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Ratio', href="../docs/ratio.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Shadow', href="../docs/shadow.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Sizing', href="../docs/sizing.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Text', href="../docs/text.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Video', href="../docs/video.html", cls="list-styled-link"), cls="list-styled-item"),
                            Li(A('Z-index', href="../docs/zindex.html", cls="list-styled-link"), cls="list-styled-item"),
                            cls="list-styled"
                        ),
                        P('Design', cls="mt-7 mb-5 fs-xxs fw-bold text-uppercase"),
                        Ul(
                            Li(A('Figma', href="../docs/figma.html", cls="list-styled-link"), cls="list-styled-item"),
                            cls="list-styled mb-0"
                        ),
                        cls="py-3 py-md-10 px-md-8"
                    ),
                    cls="collapse navbar-collapse", id="docsCollapse"
                ),
                cls="navbar navbar-expand-md navbar-light sticky-start mx-n4 mx-md-0 py-3 py-md-0 px-4 px-md-0"
        )