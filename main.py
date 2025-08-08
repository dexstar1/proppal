from fasthtml.common import *
from datetime import datetime
from controller.api import add_product, get_products, update_product, delete_message
from components.button import view_site_button
from components.product_table_list import product_table_list
from components.create_product_form import create_product_form

from pages.homepage import render_homepage
from pages.docs import design_system




hdrs = (
    Link(rel='stylesheet', href='/assets/css/main.css', type='text/css'),    
    Link(rel='stylesheet', href='/assets/css/theme.min.css', type='text/css'),
    Link(rel='stylesheet', href='/assets/fonts/feather.css', type='text/css'),
    Link(rel='stylesheet', href='/assets/libs/highlightjs/styles/vs2015.css', type='text/css'),
    Link(rel='stylesheet', href='/assets/libs/fortawesome/fontawesome-free/css/all.min.css', type='text/css'),
)

app, rt = fast_app(
    static_path='public', 
    live=True, 
    hdrs=hdrs, 
    pico=False
)


# Routes
@rt('/add', methods=['post'])
async def add(req):
    form_data = await req.form()
    name = form_data.get('name')
    description = form_data.get('description')
    price = form_data.get('price')
    sizes = form_data.get('size[]')
    if isinstance(sizes, list):
        sizes = ",".join(sizes)
    elif sizes is None:
        sizes = ""
    featured_image = form_data.get('featured_image')
    gallery_image = form_data.get('gallery_image')
    if name and description and price and sizes and featured_image and gallery_image:
        add_product(
        name,
        description,
        float(price),
        sizes,
        featured_image,
        gallery_image,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
    return Div(
        Div(create_product_form(), id="form-container"),
        product_table_list()
    )

@rt('/delete/{product_id}', methods=['post'])
async def delete(product_id: int):
    delete_message(product_id)
    return product_table_list()

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
            Div(create_product_form(), id="form-container"),
            product_table_list()
        )
    return "Error updating product"

@rt('/')
def get_homepage():
    return render_homepage(),

@rt('/docs')
def get_docs():
    return design_system(),


@rt('/add-product')
def get_add_product():
    return Div(
                view_site_button(),
                Div(
                    Div(
                        create_product_form(), id="form-container",
                        cls="w-[25%]"
                        ),
                    Div(
                        product_table_list(), 
                        cls="w-[70%]"
                        ), 
                        cls="flex justify-between align-center",
                    ),
                    id="addProduct"
                )
