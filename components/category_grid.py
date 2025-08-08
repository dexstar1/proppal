from fasthtml.common import *

def category_grid():
    return Section(
        Div(
                H2("Best Sellers", cls="text-center"), 
                Div(   
                    Div(A("Sunglasses", href="", cls="bg-[#fff] text-[#000] p-[20px] mx-0 align-items-center max-w-[200px]"),
                        cls="text-center items-center h-[350px] w-[350px] bg-cover object-fit flex flex-col justify-center align-center", style="background-image: url('/assets/images/sunglasses-category.jpg');"
                        ),
                    Div(A("Flat Shoes", href="", cls="bg-[#fff] text-[#000] p-[20px] mx-0 align-center max-w-[200px]"),
                        cls="text-center items-center h-[350px] w-[350px] bg-cover object-fit flex flex-col justify-center align-center", style="background-image: url('/assets/images/flat_shoes-category.jpg');"
                        ),
                    Div(A("T-Shirts", href="", cls="bg-[#fff] text-[#000] p-[20px] mx-0 align-center max-w-[200px]"),
                        cls="text-center items-center h-[350px] w-[350px] bg-cover object-fit flex flex-col justify-center align-center", style="background-image: url('/assets/images/t_shirts-category.jpg');"
                        ),
                    Div(A("Sweatshirts", href="", cls="bg-[#fff] text-[#000] p-[20px] mx-0 align-center max-w-[200px]"),
                        cls="text-center items-center h-[350px] w-[350px] bg-cover object-fit flex flex-col justify-center align-center", style="background-image: url('/assets/images/sweatshirts-category.jpg');"
                        ),
                    Div(A("Dresses", href="", cls="bg-[#fff] text-[#000] p-[20px] mx-0 align-center max-w-[200px]"),
                        cls="text-center items-center h-[350px] w-[350px] bg-cover object-fit flex flex-col justify-center align-center", style="background-image: url('/assets/images/dresses-category.jpg');"
                        ),
                    Div(A("Bags", href="", cls="bg-[#fff] text-[#000] p-[20px] mx-0 align-center max-w-[200px]"),
                        cls="text-center items-center h-[350px] w-[350px] bg-cover object-fit flex flex-col justify-center align-center", style="background-image: url('/assets/images/bags-category.jpg');"
                        ),
                    cls="flex flex-wrap justify-center gap-4 items-center pt-8"  
                ),
            cls="flex flex-col gap-4 justify-center items-center w-full", 
        ),
        cls="py-12 px-20",
    )
