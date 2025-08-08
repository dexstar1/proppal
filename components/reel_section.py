from fasthtml.common import *


def reel_section():
    return Div(
        Video(src="/assets/videos/reel.mp4", autoplay=True, loop=True, muted=True, cls="w-[100vw] h-[512px] object-cover mx-auto"),
        cls="flex flex-col justify-center items-center w-full h-[auto]"
       )
