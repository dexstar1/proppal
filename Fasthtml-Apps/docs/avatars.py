from fasthtml.common import *

def Avatars():
    return Div(
        H2("Avatars", cls="fs-4 fw-bold mb-4"),
        P("Avatars are used to represent users or entities in your application. They can be displayed in various sizes and styles.", cls="mb-3"),
        Div(
            Img(src="path/to/avatar1.png", alt="User Avatar 1", cls="avatar-lg"),
            P("User 1", cls="text-center"),
            cls="mb-4"
        ),
        Div(
            Img(src="path/to/avatar2.png", alt="User Avatar 2", cls="avatar-md"),
            P("User 2", cls="text-center"),
            cls="mb-4"
        ),
        Div(
            Img(src="path/to/avatar3.png", alt="User Avatar 3", cls="avatar-sm"),
            P("User 3", cls="text-center"),
            cls="mb-4"
        ),
        cls="px-md-10 py-10"
    )