from fasthtml.common import *
from controller.api import get_products


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
