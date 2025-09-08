from fasthtml.common import *

def card_default(img_src, title, link_text):
    return Div(
            Img(cls="card-img-top", src=img_src, alt="..."),
            Div(
                H6("Card title"),
                P(
                    title,
                    cls="text-gray-500"
                ),
                A(
                    link_text,
                    I(cls="fe fe-arrow-right ms-2"),
                    href="#",
                    cls="btn btn-primary btn-sm"
                ),
                cls="card-body border"
            ),
            cls="card", style="max-width: 320px;"
        )

def card_sizing():
    return Div(
            Div(
                Div(
                    H6("Extra Large"),
                    P(
                        "Lorem, ipsum dolor sit amet consectetur adipisicing elit. Excepturi debitis accusamus saepe, inventore quas, dolorem porro, quod iure neque maxime vel amet!",
                        cls="mb-0 text-gray-500"
                    ),
                    cls="card-body border"
                ),
                cls="card card-xl mb-5"
            ),
            Div(
                Div(
                    H6("Large"),
                    P(
                        "Lorem, ipsum dolor sit amet consectetur adipisicing elit. Excepturi debitis accusamus saepe, inventore quas, dolorem porro, quod iure neque maxime vel amet!",
                        cls="mb-0 text-gray-500"
                    ),
                    cls="card-body border"
                ),
                cls="card card-lg mb-5"
            ),
            Div(
                Div(
                    H6("Base"),
                    P(
                        "Lorem, ipsum dolor sit amet consectetur adipisicing elit. Excepturi debitis accusamus saepe, inventore quas, dolorem porro, quod iure neque maxime vel amet!",
                        cls="mb-0 text-gray-500"
                    ),
                    cls="card-body border"
                ),
                cls="card"
            ),
            cls="card-body border"
        )

def card_imageHover(img_src1, img_src2):
    return Div(
            Div(
                Div(
                    Div(
                        Img(cls="card-img-top card-img-back", src=img_src1, alt="..."),
                        Img(cls="card-img-top card-img-front", src=img_src2, alt="..."),
                        cls="card-img-hover"
                    ),
                    cls="card-img"
                ),
                cls="card", style="max-width: 320px;"
            ),
            cls="card-body border"
        )

def card_imageBg(img_bg, title, link_text):
    return Div(
            Div(
                Div(
                    Div(
                        style=f"background-image: url({img_bg});",
                        cls="card-bg-img bg-cover"
                    ),
                    cls="card-bg"
                ),
                Div(
                    H5(title, cls="mb-0"),
                    A(
                        link_text,
                        I(cls="fe fe-arrow-right ms-2"),
                        href="#!",
                        cls="btn btn-link stretched-link px-0 text-reset"
                    ),
                    cls="card-body my-auto"
                ),
                cls="card card-xl", style="min-height: 280px; max-width: 320px;"
            ),
            cls="card-body border"
        )

def card_circle(text, discount):
    return Div(
            Div(
                Div(
                    Strong(text),
                    Span(discount, cls="fs-4 fw-bold"),
                    cls="card-circle card-circle-lg position-relative", style="top: 0;"
                ),
                cls="card-body border"
            ),
            cls="card"
        )

def card_badge(text, type):
        textbody= 'text-body' if type=='white' else '',
        return Div(
                Div(
                    Div(text, cls=f"badge bg-{type} {textbody} text-uppercase"),
                    cls="card-body border"
                ),
                cls="card"
            )

def card_price(price, img_src):
    return Div(
            Div(
                Div(
                    Div(price, cls="btn btn-white btn-sm card-price card-price-start"),
                    Img(src=img_src, alt="...", cls="card-img-top"),
                    cls="card", style="max-width: 320px;"
                ),
                cls="card-body border"
            ),
            cls="card"
        )

def card_actions(img_src):
    return Div(
            Div(
                Div(
                    Div(
                        Img(cls="card-img-top", src=img_src, alt="..."),
                        Div(
                            Span(
                                Button(
                                    I(cls="fe fe-eye"),
                                    cls="btn btn-xs btn-circle btn-white-primary",
                                    data_bs_toggle="modal",
                                    data_bs_target="#modalProduct"
                                ),
                                cls="card-action"
                            ),
                            Span(
                                Button(
                                    I(cls="fe fe-shopping-cart"),
                                    cls="btn btn-xs btn-circle btn-white-primary",
                                    data_toggle="button"
                                ),
                                cls="card-action"
                            ),
                            Span(
                                Button(
                                    I(cls="fe fe-heart"),
                                    cls="btn btn-xs btn-circle btn-white-primary",
                                    data_toggle="button"
                                ),
                                cls="card-action"
                            ),
                            cls="card-actions"
                        ),
                        cls="card-img"
                    ),
                    cls="card", style="max-width: 320px;"
                ),
                cls="card-body border"
            ),
            cls="card"
        ),

def card_action(img_src1, img_src2):
    return Div(
                Div(
                        Div(
                            Div(
                                Img(cls="card-img-top", src=img_src1, alt="..."),
                                Button(
                                    I(cls="fe fe-heart"),
                                    cls="btn btn-xs btn-circle btn-white-primary card-action card-action-end",
                                    data_toggle="button"
                                ),
                                cls="card-img"
                            ),
                            cls="card", style="max-width: 320px;"
                        ),
                        cls="card-body border"
                    ),
                    Div(
                        Div(
                            Div(
                                Img(cls="card-img-top", src=img_src2, alt="..."),
                                Button(
                                    I(cls="fe fe-heart"),
                                    cls="btn btn-xs btn-circle btn-white-primary card-action card-action-end",
                                    data_toggle="button"
                                ),
                                cls="card-img"
                            ),
                            cls="card", style="max-width: 320px;"
                        ),
                        cls="card-body border"
                    ),
            ),

def card_button(text):
    return Div(
                Div(
                    Img(cls="card-img-top", src="../assets/images/products/product-9.jpg", alt="..."),
                    Button(
                        I(cls="fe fe-eye me-2 mb-1"),
                        text,
                        cls="btn btn-xs w-100 btn-dark card-btn",
                        data_bs_toggle="modal",
                        data_bs_target="#modalProduct"
                    ),
                    cls="card-img"
                ),
                cls="card", style="max-width: 320px;"
            ),

def card_collapse(text1,text2,price1,price2):
    return Div(
                Div(
                    Img(cls="card-img-top", src="../assets/images/products/product-7.jpg", alt="..."),
                    Div(
                        Div(
                            Div(
                                A(
                                    text1,
                                    href="https://yevgenysim-turkey.github.io/shopper/product.html",
                                    cls="d-block fw-bold text-body"
                                ),
                                A(
                                    text2,
                                    href="https://yevgenysim-turkey.github.io/shopper/shop.html",
                                    cls="fs-xs text-muted"
                                ),
                                cls="col"
                            ),
                            Div(
                                Div(
                                    price1,
                                    cls="fs-xs fw-bold text-gray-350 text-decoration-line-through"
                                ),
                                Div(
                                    price2,
                                    cls="fs-sm fw-bold text-primary"
                                ),
                                cls="col-auto"
                            ),
                            cls="row gx-0"
                        ),
                        cls="card-body px-0 pb-0 bg-white"
                    ),
                    Div(
                        Div(
                            Form(
                                Div(
                                    Div(
                                        Input(
                                            type="radio",
                                            id="docsProductThreeColorOne",
                                            name="docsProductThreeColor",
                                            cls="form-check-input",
                                            style="background-color: #f9f9f9",
                                            checked=True
                                        ),
                                        cls="form-check form-check-inline form-check-color"
                                    ),
                                    cls="mb-1"
                                ),
                                Div(
                                    Div(
                                        Input(
                                            cls="form-check-input",
                                            id="docsProductThreeSizeOne",
                                            type="radio",
                                            name="sizeRadio"
                                        ),
                                        Label("6", cls="form-check-label", for_="docsProductThreeSizeOne"),
                                        cls="form-check form-check-inline form-check-text fs-xs"
                                    ),
                                    Div(
                                        Input(
                                            cls="form-check-input",
                                            id="docsProductThreeSizeTwo",
                                            type="radio",
                                            name="sizeRadio"
                                        ),
                                        Label("6.5", cls="form-check-label", for_="docsProductThreeSizeTwo"),
                                        cls="form-check form-check-inline form-check-text fs-xs"
                                    ),
                                    Div(
                                        Input(
                                            cls="form-check-input",
                                            id="docsProductThreeSizeThree",
                                            type="radio",
                                            name="sizeRadio"
                                        ),
                                        Label("7", cls="form-check-label", for_="docsProductThreeSizeThree"),
                                        cls="form-check form-check-inline form-check-text fs-xs"
                                    ),
                                    Div(
                                        Input(
                                            cls="form-check-input",
                                            id="docsProductThreeSizeFour",
                                            type="radio",
                                            name="sizeRadio"
                                        ),
                                        Label("7.5", cls="form-check-label", for_="docsProductThreeSizeFour"),
                                        cls="form-check form-check-inline form-check-text fs-xs"
                                    ),
                                    Div(
                                        Input(
                                            cls="form-check-input",
                                            id="docsProductThreeSizeFive",
                                            type="radio",
                                            name="sizeRadio"
                                        ),
                                        Label("8.5", cls="form-check-label", for_="docsProductThreeSizeFive"),
                                        cls="form-check form-check-inline form-check-text fs-xs"
                                    ),
                                ),
                                cls=""
                            ),
                            cls="card-footer px-0 bg-white"
                        ),
                        cls="card-collapse collapse"
                    ),
                    cls="card-collapse-parent"
                ),
                cls="card", data_toggle="card-collapse", style="max-width: 320px;"
            ),

