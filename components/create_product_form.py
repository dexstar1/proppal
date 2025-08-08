from fasthtml.common import *



# Constants
MAX_NAME_CHAR = 15
MAX_MESSAGE_CHAR = 50

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
    )
