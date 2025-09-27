from fasthtml.common import *
from typing import Optional, List

def Card(
    title: str,
    content: Optional[Any] = None,
    img_src: Optional[str] = None,
    link_text: Optional[str] = None,
    link_href: Optional[str] = "#",
    card_cls: Optional[str] = "card",
    body_cls: Optional[str] = "card-body",
    img_cls: Optional[str] = "card-img-top",
    title_cls: Optional[str] = "card-title",
    text_cls: Optional[str] = "card-text text-gray-500",
    button_cls: Optional[str] = "btn btn-primary btn-sm",
    footer_content: Optional[Any] = None,
    header_content: Optional[Any] = None,
    style: Optional[str] = None,
):
    card_elements = []

    if header_content:
        card_elements.append(Div(header_content, cls="card-header"))

    if img_src:
        card_elements.append(Img(cls=img_cls, src=img_src, alt=title))

    card_body_elements = []
    if title:
        card_body_elements.append(H6(title, cls=title_cls))
    if content:
        card_body_elements.append(P(content, cls=text_cls))
    if link_text:
        card_body_elements.append(A(link_text, I(cls="fe fe-arrow-right ms-2"), href=link_href, cls=button_cls))

    if card_body_elements:
        card_elements.append(Div(*card_body_elements, cls=body_cls))

    if footer_content:
        card_elements.append(Div(footer_content, cls="card-footer"))

    return Div(*card_elements, cls=card_cls, style=style)