from fasthtml.common import *
from components.product_table import product_table
from controller.api import get_products


def product_table_list():
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
        *[product_table(entry) for entry in get_products()],
        id="product-list",
        cls="mt-4"
    )
