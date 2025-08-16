from fasthtml.common import *
from components.hero_section import hero_section
from components.products_carousel import products_carousel
from components.top_item import top_item_of_the_week
from components.category_grid import category_grid
from components.our_story import our_story
from components.reel_section import reel_section
from components.testimonials import testimonials
from components.insta_cover import insta_cover
from components.footer import footer
from components.product_table_list import product_table_list
from components.create_product_form import create_product_form
from components.button import admin_button
from components.button import docs_button
from components.button import view_site_button

def render_homepage():
    return Div(
        admin_button(),
        docs_button(),
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