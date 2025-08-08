from fasthtml.common import *

def insta_cover():
    return Div(
        Button("@gastromart", cls="text-[1rem] text-black py-[1rem] bg-white w-[150px]"),
        cls="py-[96px] w-[1200px] flex flex-col justify-center align-center text-center items-center bg-cover bg-no-repeat object-center mx-auto mb-[97px]",
        style="background-image: url('/assets/images/insta-cover.jpg'); "
    )
