from fasthtml.common import *

def badge_span(text, type):
    return  Span(text, cls=f"badge bg-{type}"),


def badge_link(text, type, href):
    return A(text, href, cls=f"badge bg-{type}"),