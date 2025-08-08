from fasthtml.common import *


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
