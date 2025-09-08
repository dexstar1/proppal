from fasthtml.common import *
from components.card import card_default, card_sizing, card_imageHover, card_imageBg, card_circle, card_badge, card_price, card_actions, card_action, card_button, card_collapse

def Cards():
    return Section(
        H3("Cards"),
        P(
            "Bootstrap’s cards provide a flexible and extensible content container with multiple variants and options. ",
            Br(),
            A("Bootstrap documentation", href="https://getbootstrap.com/docs/5.1/components/card/", target="_blank"),
            cls="text-gray-500"
        ),
        card_default(img_src='../assets/images/covers/cover-28.jpg', title='Some quick example text to build on the card title and make up the bulk of the cards content.', link_text='Go somewhere'),
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
        card_sizing(),
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
        card_imageHover(img_src1='../assets/images/products/product-120.jpg', img_src2='../assets/images/products/product-5.jpg'),
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
        card_imageBg(img_bg='../assets/images/products/product-22.jpg', title='Summer Hats', link_text='Shop Now'),
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
        card_circle(text='save', discount='30%'),
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
        card_badge(text='NEW', type='dark'),
        card_badge(text='NEW', type='white'),
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
        card_price(price='$59.00', img_src='../assets/images/products/product-65.jpg'),
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
        card_actions(img_src="../assets/images/products/product-6.jpg"),
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
        card_action(img_src1="../assets/images/products/product-6.jpg", img_src2="../assets/images/products/product-7.jpg"),
        
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
            card_button(text=" Quick View"),
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
            card_collapse(text1="Leather Sneakers", text2="Shoes", price1="$115.00", price2 ="$85.00"),
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