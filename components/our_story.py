from fasthtml.common import *


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
