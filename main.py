from fasthtml.common import *
# from fasthtml.templates import Template
import sqlite3
from datetime import datetime


hdrs = [Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/tailwindcss@3.4.3/dist/tailwind.min.css"),
        Link(rel="stylesheet", href="assets/libs/flickity/dist/flickity.min.css"),
        Link(rel="stylesheet", href="assets/libs/flickity/dist/flickity.min.css"),
        Link(rel="stylesheet", href="assets/libs/fancyapps/fancybox/dist/jquery.fancybox.min.css"),
        Link(rel="stylesheet", href="assets/libs/fortawesome/fontawesome-free/css/all.min.css"),
        Link(rel="stylesheet", href="assets/libs/flickity/dist/flickity.min.css"),
        Link(rel="stylesheet", href="assets/libs/highlightjs/styles/vs2015.css"),
        Link(rel="stylesheet", href="assets/libs/simplebar/dist/simplebar.min.css"),
        Link(rel="stylesheet", href="assets/libs/flickity-fade/flickity-fade.css"),
        Link(rel="stylesheet", href="assets/fonts/feather/feather.css"),
        Link(rel='stylesheet', href='/assets/css/theme.min.css', type='text/css'),
        Link(rel='stylesheet', href='/assets/css/main.css', type='text/css'),
        ]

app, rt = fast_app(
    static_path='public', 
    live=True, 
    hdrs=hdrs, 
    pico=False
)

DB_PATH = "guestbook.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            price REAL NOT NULL,
            size TEXT NOT NULL, -- Comma-separated sizes
            featured_image TEXT NOT NULL,
            gallery_image TEXT NOT NULL,
            date_added TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Constants
MAX_NAME_CHAR = 15
MAX_MESSAGE_CHAR = 50

# CRUD Operations
def get_products():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, description, price, size, featured_image, gallery_image, date_added
        FROM products
        ORDER BY id DESC
    """)
    products = cursor.fetchall()
    conn.close()
    return products

def add_product(name, description, price, size, featured_image, gallery_image, date_added):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO products (name, description, price, size, featured_image, gallery_image, date_added)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, description, price, size, featured_image, gallery_image, date_added ))
    conn.commit()
    conn.close()

def update_product(product_id, name, description, price, size, featured_image, gallery_image):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE products
        SET name = ?, description = ?, price = ?, size = ?, featured_image = ?, gallery_image = ?
        WHERE id = ?
    """, (name, description, price, size, featured_image, gallery_image, product_id))
    conn.commit()
    conn.close()

def delete_message(product_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()


# Render Functions

def render_product(entry):
    sizes = entry[4].split(",")  # Assuming size is the 5th column
    return Tr(
        Td(P(f"{entry[1]}")),
        Td(P(f"{entry[2]}")),
        Td(P(f"${entry[3]:.2f}")),
        Td(P(f"{', '.join(sizes)}")),
        Td(Img(src=entry[5], alt="Featured Image", style="width: 35px; height: auto;")),
        # Div(
        #     *[Img(src=img, alt="Gallery Image", style="width: 100px; height: auto; margin-right: 10px;")
        #       for img in entry[6].split(",")],
        #     cls="flex"
        # ),
        Td(Footer(Small(Em(f"{entry[7]}")))),
        Td(Div
           (
            A("Edit",
              href="#",
              hx_get=f"/edit/{entry[0]}",
              hx_target="#form-container",
              hx_swap="innerHTML"),
            A("Delete",
              href="#",
              hx_post=f"/delete/{entry[0]}",
              hx_target="#product-list",
              hx_swap="outerHTML",
              style="color: red;",
              hx_confirm="Are you sure you want to delete this product?"),
            cls="flex gap-2"
            ),
        ),
        cls="flex justify-start align-start border-1 border-bottom mb-4"
    )

def render_product_list():
    return Table(
        Tr(
            Th(H5("Name")),
            Th(H5("Description")),
            Th(H5("Price")),
            Th(H5("Sizes")),
            Th(H5("Image")),
            Th(H5("Date")),
            Th(H5("Action")),
            cls="flex text-left mb-4"
        ),
        *[render_product(entry) for entry in get_products()],
        id="product-list",
        cls="mt-4"
    )

def render_product_grid():
    products = get_products()
    return Div(
        Div(
            *[Div(
                Img(src=prod[5], alt="product image", style="width:220px; height:auto;"), 
                cls="swiper-slide") for prod in products
            ],
            cls="swiper-wrapper"
        ),
        Div(cls="swiper-pagination"),
        Div(cls="swiper-button-prev"),
        Div(cls="swiper-button-next"), 
        id="product-grid",
        cls="flex justify-center align-center gap-4 w-[1000px] flex-wrap my-16 mx-auto swiper h-auto"
    )

def products_carousel():
    products = get_products()
    return Section(
    Div(
        Div(
            Div(
                H2('Best Sellers', cls='mb-10 text-center'),
                Div(
                    Div(
                        Div(
                            *[Div(
                                A(
                                    Img(src=prod[5], alt='...', cls='card-img-top'),
                                    Div(
                                        Div('Cropped cotton Top', cls='text-body'),
                                        Div('$', prod[3], cls='text-muted'),
                                        cls='card-body font-weight-bold text-center'
                                    ),
                                    href='product-2.html',
                                    cls='card shadow-hover'
                                ),
                                style='max-width: 229px; position: absolute;',
                                cls='col pt-3 pb-7 best-seller-prod'
                            ) for prod in products],
                            style='left: 0px; transform: translateX(-150%);',
                            cls='flickity-slider'
                        ),
                        style='height: 372.75px; touch-action: pan-y;',
                        cls='flickity-viewport'
                    ),
                    Button(
                        Svg(
                            Path(d='M 10,50 L 60,100 L 70,90 L 30,50  L 70,10 L 60,0 Z'),
                            viewbox='0 0 100 100',
                            cls='flickity-button-icon'
                        ),
                        type='button',
                        aria_label='Previous',
                        cls='flickity-button flickity-prev-next-button previous'
                    ),
                    Button(
                        Svg(
                            Path(d='M 10,50 L 60,100 L 70,90 L 30,50  L 70,10 L 60,0 Z', transform='translate(100, 100) rotate(180) '),
                            viewbox='0 0 100 100',
                            cls='flickity-button-icon'
                        ),
                        type='button',
                        aria_label='Next',
                        cls='flickity-button flickity-prev-next-button next'
                    ),
                    data_flickity='{"prevNextButtons": true}',
                    tabindex='0',
                    cls='flickity-buttons-lg flickity-buttons-offset px-lg-12 flickity-enabled is-draggable'
                ),
                cls='col-12'
            ),
            cls='row'
        ),
        cls='container'
    ),
    cls='pt-12 pb-10'
)

def hero_section():
    return Section(
            Div(
                Div(
                    Div(
                            H1("Better Things In a Better Way", cls="display-4 mb-10"),
                            A("Shop Now", cls="link-underline text-reset mx-4 my-4"),
                            cls="col-12 col-md-7 col-lg-5 text-center text-white"
                    ),
                    cls="row justify-content-center align-items-center min-vh-100 pt-15 pb-12"
                ),
                cls="container d-flex flex-column",
            ),
            cls="mt-n12",
            style="text-align: center; padding: 20px; background-image: url('/assets/images/cover.jpg'); background-size:cover; background-repeat:no-repeat;height: 100vh; width: 100vw; display:flex;flex-direction:column;justify-content:center;align-items:center;"
        )

def category_grid():
    return Section(
        Div(
                H2("Best Sellers", cls="mb-10 text-center"), 
                Div(   
                    Div(A("Sunglasses", href="", cls="bg-[#fff] text-[#000] p-[20px] text-center align-center"),
                        cls="text-center h-[350px] w-[350px] bg-cover object-fit flex flex-column justify-center align-center", style="background-image: url('/assets/images/sunglasses-category.jpg');"
                        ),
                    Div(A("Flat Shoes", href="", cls="bg-[#fff] text-[#000] p-[20px] text-center align-center"),
                        cls="text-center h-[350px] w-[350px] bg-cover object-fit flex flex-column justify-center align-center", style="background-image: url('/assets/images/flat_shoes-category.jpg');"
                        ),
                    Div(A("T-Shirts", href="", cls="bg-[#fff] text-[#000] p-[20px] text-center align-center"),
                        cls="text-center h-[350px] w-[350px] bg-cover object-fit flex flex-column justify-center align-center", style="background-image: url('/assets/images/t_shirts-category.jpg');"
                        ),
                    Div(A("Sweatshirts", href="", cls="bg-[#fff] text-[#000] p-[20px] text-center align-center"),
                        cls="text-center h-[350px] w-[350px] bg-cover object-fit flex flex-column justify-center align-center", style="background-image: url('/assets/images/sweatshirts-category.jpg');"
                        ),
                    Div(A("Dresses", href="", cls="bg-[#fff] text-[#000] p-[20px] text-center align-center"),
                        cls="text-center h-[350px] w-[350px] bg-cover object-fit flex flex-column justify-center align-center", style="background-image: url('/assets/images/dresses-category.jpg');"
                        ),
                    Div(A("Bags", href="", cls="bg-[#fff] text-[#000] p-[20px] text-center align-center"),
                        cls="text-center h-[350px] w-[350px] bg-cover object-fit flex flex-column justify-center align-center", style="background-image: url('/assets/images/bags-category.jpg');"
                        ),
                    cls="flex gap-5 justify-start items-start pt-8"  
                ),
            cls="flex flex-column" 
        ),
        cls="pt-12 pb-10",
        )

def top_item_of_the_week():
    # Fetch the first product
    products = get_products()
    if not products:
        return Div(H2("No products available", cls="text-[2.25rem] text-center"))

    product = products[0]  # Get the first product
    name = product[1]
    description = product[2]
    price = product[3]
    sizes = product[4].split(",")
    featured_image = product[5]
    gallery_images = product[6].split(",")  # Split gallery images into a list

    return Div(
        H2("Top Item Of The Week", cls="text-[2.25rem]"),
        Div(
            Div(
                Img(src=featured_image, style="width:100%;object-fit:cover;"),
                Div(
                    *[Img(src=img, style="width:97px;height:97px;object-fit:center;") for img in gallery_images],
                    cls="flex gap-4", style="width:300px; margin-top:15px;"
                ),
                cls="w-[58%]"
            ),
            Div(
                H6("Category: Featured"),
                H3(name, cls="text-[2rem]"),
                P(f"${price:.2f}", cls="text-[1.5rem]"),
                P(description, cls="text-[1rem] text-gray-600"),
                P("Available Sizes:", cls="text-[1rem] font-bold"),
                Div(
                    *[P(size, cls="border border-1 border-gray-300 p-4 text-[#000] mr-2 w-[60px] text-center") for size in sizes],
                    cls="flex flex-row flex-wrap gap-2",
                ),
                Div(
                    Button("Add to Cart", cls="text-[#fff] bg-[#1f1f1f] p-4 w-[300px]"),
                    Button("Wishlist", cls="text-[#fff] bg-[#000] p-4 w-[250px]"),
                    cls="flex gap-4",
                ),
                Div(
                    P("Is your size or color not available?"),
                    A("Join the Wait List!", cls="text-[#000]"),
                    cls="flex gap-4",
                ),
                cls="flex flex-col gap-4 justify-center items-start",
            ),
            cls="flex gap-16 justify-between w-[90vw] h-auto bg-[#fff] p-16 mt-16",
        ),
        cls="flex flex-col justify-center items-center bg-[#f5f5f5] py-24 px-4 w-full",
    )

def our_story():
    return Div(
        H2("Our Story", cls="text-[2.25rem]"),
        Div(
            Div(
                Img(src="/assets/images/our_story.jpg", style="width:640px;object-fit:cover;"),
                cls="w-[58%]"
            ),  
            Div(
                H6("Our Story"),
                H2("About Our Store", cls="text-[2.25rem]"),
                P("Open created shall two he second moving whose. He face whose two upon, fowl behold waters. Fly there their day creepeth. Darkness beginning spirit after. Creepeth subdue. Brought may, first. Under living that.", 
                  cls="text-[1.25rem] text-[#767676]"),
                P("`Third. For morning whales saw were had seed can't divide it light shall moveth, us blessed given wherein.", 
                  cls="text-[1.25rem] text-[#767676]"),
                A("Discover More", cls="text-[#000] text-[1.25rem] mt-8"),
                cls="flex flex-col gap-4 justify-center items-start w-[40%]",
            ),
            cls="flex gap-16 justify-center h-auto bg-[#fff] p-16 mt-16",
        ),
        cls="flex flex-col gap-4 justify-center items-center bg-[#fff] py-24 px-4 w-full",
    )

def reel_section():
    return Div(
        Video(src="/assets/videos/reel.mp4", autoplay=True, loop=True, muted=True, cls="w-[100vw] h-[512px] object-cover mx-auto"),
        cls="flex flex-col justify-center items-center w-full h-[auto]",
    )

def create_product_form(action="/add", button_text="Add Product", product=None):
    sizes = ["S", "M", "L", "XL", "XXL"]
    selected_sizes = product["size"].split(",") if product else []

    return Form(
        Fieldset(
            Div(
                Label("Product Name", cls="block text-sm font-medium text-gray-700"),
                Input(
                    type='text',
                    name='name',
                    placeholder='Product Name',
                    value=product["name"] if product else "",
                    required=True,
                    maxlength=50,
                    cls="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                ),
                cls="mb-4"
            ),
            Div(
                Label("Description", cls="block text-sm font-medium text-gray-700"),
                Textarea(
                    name='description',
                    placeholder='Product Description',
                    required=True,
                    maxlength=200,
                    cls="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                )(product["description"] if product else ""),
                cls="mb-4"
            ),
            Div(
                Label("Price", cls="block text-sm font-medium text-gray-700"),
                Input(
                    type='number',
                    name='price',
                    placeholder='Price',
                    required=True,
                    step="0.01",
                    value=product["price"] if product else "",
                    cls="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                ),
                cls="mb-4"
            ),
            Div(
                Label("Sizes", cls="block text-sm font-medium text-gray-700"),
                Div(
                    *[Div(
                        Input(
                            type="checkbox",
                            name="size[]",  # Use "size[]" to allow multiple selections
                            value=size,
                            checked=(size in selected_sizes),
                            cls="h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
                        ),
                        Label(size, cls="ml-2 text-sm text-gray-700"),
                        cls="inline-flex items-center mr-4"
                    ) for size in sizes],
                    cls="mt-2"
                ),
                cls="mb-4"
            ),
            Div(
                Label("Featured Image URL", cls="block text-sm font-medium text-gray-700"),
                Input(
                    type='text',
                    name='featured_image',
                    placeholder='Featured Image URL',
                    value=product["featured_image"] if product else "",
                    required=True,
                    cls="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                ),
                cls="mb-4"
            ),
            Div(
                Label("Gallery Image URLs (comma-separated)", cls="block text-sm font-medium text-gray-700"),
                Input(
                    type='text',
                    name='gallery_image',
                    placeholder='Gallery Image URLs',
                    value=product["gallery_image"] if product else "",
                    required=True,
                    cls="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                ),
                cls="mb-4"
            ),
            Div(
                Button(
                    button_text,
                    type="submit",
                    cls="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                ),
                cls="mt-4"
            ),
        ),
        method="post",
        hx_post=action,
        hx_target="#product-list",
        hx_swap="outerHTML",
        cls="space-y-6 bg-white p-6 rounded-lg shadow-md"
    )

def testimonials():
    return Div(
        H6("WHAT BUYERS SAY", cls="text-[1rem]"),
        H2("Customer Reviews", cls="text-[2rem]"),
        P("Given wherein. Doesn't called also and air sea to make first subdue \
           beginning. Appear seasons the it after whose beginning. Hath can't good life. " \
           "They're multiply made give divided open, be likeness Cattle be have.Life tree " \
           "darkness. She'd very. \
        ", cls="text-[1.25rem]"),
        P("Darell Baker, 18 May 2025", cls="text-[1rem]"),
        P("..."),
        cls="flex flex-col justify-center align-center text-center w-[1000px] gap-8 py-[96px] mx-auto"
    )
 
def insta_cover():
    return Div(
        Button("@gastromart", cls="text-[1rem] text-black py-[1rem] bg-white w-[150px]"),
        cls="py-[96px] w-[1200px] flex flex-col justify-center align-center text-center items-center bg-cover bg-no-repeat object-center mx-auto mb-[97px]",
        style="background-image: url('/assets/images/insta-cover.jpg'); "
    )

def footer():
    return Div(
        H2("Gastro Mart", cls="text-[2rem] text-white"),
        Ul(
            Li("Contact Us", cls="text-[#eee]"),
            Li("FAQs", cls="text-[#eee]"),
            Li("Size Guide", cls="text-[#eee]"),
            Li("Shippings & Returns", cls="text-[#eee]"),
            Li("Our Story", cls="text-[#eee]"),
            cls="flex justify-center align-center gap-4"
        ),
            cls="flex flex-col text-center justify-center align-center gap-8 bg-black w-full py-[96px]"
    )

def render_content():
    return Div(
        admin_button(),
        hero_section(),
        products_carousel(),
        category_grid(),
        top_item_of_the_week(),
        our_story(),
        reel_section(),
        testimonials(),
        insta_cover(),
        footer(),
        id="theBody",
    )

def admin_button():
    return Div(
        Button("Admin",
                hx_get=f"/add-product",
                hx_swap="outerHTML",
                hx_target="#theBody",
               cls="btn btn-primary btn-lg")
    )

def view_site_button():
    return Div(
        Button("Back",
                hx_get=f"/",
                hx_swap="innerHTML",
                hx_target="#addProduct",
               cls="btn btn-outline-primary btn-underline mb-1")
    )


# Routes
@rt('/add', methods=['post'])
async def add(req):
    form_data = await req.form()
    name = form_data.get('name')
    description = form_data.get('description')
    price = form_data.get('price')
    sizes = form_data.get('size[]')
    sizes = ",".join(sizes)
    featured_image = form_data.get('featured_image')
    gallery_image = form_data.get('gallery_image')
    if name and description and price and sizes and featured_image and gallery_image:
        add_product(name, description, float(price), sizes, featured_image, gallery_image, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return Div(
        render_product_list()
    )

@rt('/edit/{product_id}', methods=['get'])
async def edit(product_id: int):
    product = [prod for prod in get_products() if prod[0] == product_id][0]
    form = create_product_form(action=f"/update/{product_id}", button_text="Update Product", product={
        "name": product[1],
        "description": product[2],
        "price": product[3],
        "size": product[4],
        "featured_image": product[5],
        "gallery_image": product[6],
    })
    return form

@rt('/update/{product_id}', methods=['post'])
async def update(product_id: int, req):
    form_data = await req.form()
    name = form_data.get('name')
    description = form_data.get('description')
    price = form_data.get('price')
    sizes = form_data.get('size[]')
    sizes = ",".join(sizes)
    featured_image = form_data.get('featured_image')
    gallery_image = form_data.get('gallery_image')
    if name and description and price and sizes and featured_image and gallery_image:
        update_product(product_id, name, description, float(price), sizes, featured_image, gallery_image)
        return Div(
            render_product_list()
        )
    return "Error updating product"

@rt('/delete/{product_id}', methods=['post'])
async def delete(product_id: int):
    delete_message(product_id)
    return render_product_list()

@rt('/')
def get():
    return Div(
                render_content(),
               )


@rt('/add-product')
def get():
    return Div(
                view_site_button(),
                Div(
                    Div(
                        create_product_form(), id="form-container",
                        cls="w-[25%]"
                        ),
                    Div(
                        render_product_list(), 
                        cls="w-[70%]"
                    ), 
                    cls="flex justify-between align-center",
                ),
                id="addProduct"
               )

serve()