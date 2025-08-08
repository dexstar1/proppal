from fasthtml.common import *

def Cards():
    return Section(
        H3("Cards"),
        P(
            "Bootstrap’s cards provide a flexible and extensible content container with multiple variants and options. ",
            Br(),
            A("Bootstrap documentation", href="https://getbootstrap.com/docs/5.1/components/card/", target="_blank"),
            cls="text-gray-500"
        ),
        Div(
            Img(cls="card-img-top", src="../assets/img/covers/cover-28.jpg", alt="..."),
            Div(
                H6("Card title"),
                P(
                    "Some quick example text to build on the card title and make up the bulk of the card's content.",
                    cls="text-gray-500"
                ),
                A(
                    "Go somewhere ",
                    I(cls="fe fe-arrow-right ms-2"),
                    href="#",
                    cls="btn btn-primary btn-sm"
                ),
                cls="card-body border"
            ),
            cls="card", style="max-width: 320px;"
        ),
        Hr(cls="my-7"),
        H5("Sizing"),
        P(
            "Control the padding of ",
            Code(".card-body"),
            " and ",
            Code(".card-footer"),
            " elements with the following modifiers:",
            cls="text-gray-500"
        ),
        Div(
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
        ),
        Div(
            Code(
                '<div class="card card-xl"><div class="card-body">...</div></div>',
                cls="highlight html hljs xml"
            ),
            cls="card-footer fs-sm bg-dark"
        ),
        Hr(cls="my-7"),
        H5("Image hover"),
        P(
            "Switch between two images on hover with the following markup:",
            cls="text-gray-500"
        ),
        Div(
            Div(
                Div(
                    Div(
                        Img(cls="card-img-top card-img-back", src="../assets/img/products/product-120.jpg", alt="..."),
                        Img(cls="card-img-top card-img-front", src="../assets/img/products/product-5.jpg", alt="..."),
                        cls="card-img-hover"
                    ),
                    cls="card-img"
                ),
                cls="card", style="max-width: 320px;"
            ),
            cls="card-body border"
        ),
        Div(
            Code(
                '<div class="card"><div class="card-img"><div class="card-img-hover"><img class="card-img-top card-img-back" ...><img class="card-img-top card-img-front" ...></div></div></div>',
                cls="highlight html hljs xml"
            ),
            cls="card-footer fs-sm bg-dark"
        ),
        Hr(cls="my-7"),
        H5("Background"),
        P(
            "Add a background image that translates on hover with the following markup:",
            cls="text-gray-500"
        ),
        Div(
            Div(
                Div(
                    Div(
                        style="background-image: url(../assets/img/products/product-22.jpg);",
                        cls="card-bg-img bg-cover"
                    ),
                    cls="card-bg"
                ),
                Div(
                    H5("Summer Hats", cls="mb-0"),
                    A(
                        "Shop Now ",
                        I(cls="fe fe-arrow-right ms-2"),
                        href="#!",
                        cls="btn btn-link stretched-link px-0 text-reset"
                    ),
                    cls="card-body my-auto"
                ),
                cls="card card-xl", style="min-height: 280px; max-width: 320px;"
            ),
            cls="card-body border"
        ),
        Div(
            Code(
                '<div class="card card-xl" style="min-height:280px;max-width:320px;"><div class="card-bg"><div class="card-bg-img bg-cover" style="background-image:url(...)"></div></div><div class="card-body my-auto">...</div></div>',
                cls="highlight html hljs xml"
            ),
            cls="card-footer fs-sm bg-dark"
        ),
        Hr(cls="my-7"),
        H5("Circle"),
        P(
            "A circle badge with two sizing and three positioning options.",
            cls="text-gray-500"
        ),
        Div(
            Div(
                Div(
                    Strong("save"),
                    Span("30%", cls="fs-4 fw-bold"),
                    cls="card-circle card-circle-lg position-relative", style="top: 0;"
                ),
                cls="card-body border"
            ),
            cls="card"
        ),
        Div(
            Code(
                '<div class="card"><div class="card-body"><div class="card-circle card-circle-lg position-relative" style="top:0;">...</div></div></div>',
                cls="highlight html hljs xml"
            ),
            cls="card-footer fs-sm bg-dark"
        ),
        Hr(cls="my-7"),
        H5("Badge"),
        P(
            "A standard badge component with two positioning options.",
            cls="text-gray-500"
        ),
        Div(
            Div(
                Div("New!", cls="badge bg-dark text-uppercase"),
                Div("New!", cls="badge bg-white text-body text-uppercase"),
                cls="card-body border"
            ),
            cls="card"
        ),
        Div(
            Code(
                '<div class="card"><div class="card-body"><div class="badge bg-dark text-uppercase">New!</div><div class="badge bg-white text-body text-uppercase">New!</div></div></div>',
                cls="highlight html hljs xml"
            ),
            cls="card-footer fs-sm bg-dark"
        ),
        Hr(cls="my-7"),
        H5("Price"),
        P(
            "Adds a pricing badge in the top left or right corner of a card.",
            cls="text-gray-500"
        ),
        Div(
            Div(
                Div(
                    Div("$59.00", cls="btn btn-white btn-sm card-price card-price-start"),
                    Img(src="../assets/img/products/product-65.jpg", alt="...", cls="card-img-top"),
                    cls="card", style="max-width: 320px;"
                ),
                cls="card-body border"
            ),
            cls="card"
        ),
        Div(
            Code(
                '<div class="card" style="max-width:320px;"><div class="btn btn-white btn-sm card-price card-price-start">$59.00</div><img src="..." class="card-img-top"></div>',
                cls="highlight html hljs xml"
            ),
            cls="card-footer fs-sm bg-dark"
        ),
        Hr(cls="my-7"),
        H5("Actions"),
        P(
            "Card action buttons fading in on hover.",
            cls="text-gray-500"
        ),
        Div(
            Div(
                Div(
                    Div(
                        Img(cls="card-img-top", src="../assets/img/products/product-6.jpg", alt="..."),
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
        Div(
            Code(
                '<div class="card"><div class="card-img"><img ...><div class="card-actions"><span class="card-action"><button ...></button></span>...</div></div></div>',
                cls="highlight html hljs xml"
            ),
            cls="card-footer fs-sm bg-dark"
        ),
        Hr(cls="my-7"),
        H5("Action"),
        P(
            "Card action button always visible in the top left or right corner.",
            cls="text-gray-500"
        ),
        Div(
            Div(
                Div(
                    Img(cls="card-img-top", src="../assets/img/products/product-7.jpg", alt="..."),
                    Button(
                        I(cls="fe fe-heart"),
                        cls="btn btn-xs btn-circle btn-white-primary card-action card-acton-start",
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
                    Img(cls="card-img-top", src="../assets/img/products/product-7.jpg", alt="..."),
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
            Code(
                '<div class="card"><div class="card-img"><img ...><button ...></button></div></div>',
                cls="highlight html hljs xml"
            ),
            cls="card-footer fs-sm bg-dark"
        ),
        Hr(cls="my-7"),
        H5("Button"),
        P(
            "Card button visible in the bottom of a card on hover.",
            cls="text-gray-500"
        ),
        Div(
            Div(
                Div(
                    Img(cls="card-img-top", src="../assets/img/products/product-9.jpg", alt="..."),
                    Button(
                        I(cls="fe fe-eye me-2 mb-1"),
                        " Quick View",
                        cls="btn btn-xs w-100 btn-dark card-btn",
                        data_bs_toggle="modal",
                        data_bs_target="#modalProduct"
                    ),
                    cls="card-img"
                ),
                cls="card", style="max-width: 320px;"
            ),
            cls="card-body border w-auto"
        ),
        Div(
            Code(
                '<div class="card"><div class="card-img"><img ...><button ...>Quick View</button></div></div>',
                cls="highlight html hljs xml"
            ),
            cls="card-footer fs-sm bg-dark"
        ),
        Hr(cls="my-7"),
        H5("Collapse"),
        P(
            "Card collapse toggled on hover.",
            cls="text-gray-500"
        ),
        Div(
            Div(
                Div(
                    Img(cls="card-img-top", src="../assets/img/products/product-7.jpg", alt="..."),
                    Div(
                        Div(
                            Div(
                                A(
                                    "Leather Sneakers",
                                    href="https://yevgenysim-turkey.github.io/shopper/product.html",
                                    cls="d-block fw-bold text-body"
                                ),
                                A(
                                    "Shoes",
                                    href="https://yevgenysim-turkey.github.io/shopper/shop.html",
                                    cls="fs-xs text-muted"
                                ),
                                cls="col"
                            ),
                            Div(
                                Div(
                                    "$115.00",
                                    cls="fs-xs fw-bold text-gray-350 text-decoration-line-through"
                                ),
                                Div(
                                    "$85.00",
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
            cls="card-body border"
        ),
        Div(
            Code(
                '<div class="card" data-toggle="card-collapse"><img ...><div class="card-collapse-parent">...</div></div>',
                cls="highlight html hljs xml"
            ),
            cls="card-footer fs-sm bg-dark"
        ),
        cls="px-md-10 py-10"
    )