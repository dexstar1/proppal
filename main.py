from fasthtml.common import *
import sqlite3
from datetime import datetime
import sqlite3
import os

# Use environment variable for database path
DB_PATH = os.getenv('DB_PATH', "guestbook.db")


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
              hx_confirm="Are you sure you want to delete this message?"),
        )
    )

def render_message_list():
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
        hx_target="#message-list",
        hx_swap="outerHTML",
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
    message = form_data.get('message')
    if name and message:
        add_message(name, message, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    return Div(
        render_message_list()
    )

@rt('/delete/{message_id}', methods=['post'])
async def delete(message_id: int):
    delete_message(message_id)
    return render_message_list()

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
            Div(create_base_form(), id="form-container"),
            render_message_list()
        )
    return "Error updating product"

@rt('/refresh-messages', methods=['get'])
async def refresh_messages():
    return render_content()

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