from fasthtml.common import *
from components.avatar import avatar
from components.avatar import avatar_title
from components.avatar import avatar_group

def Avatars():
    return Section(
        H3("Avatars"),
        P(
            "Create and group avatars of different sizes and shapes with a single component.",
            cls="text-gray-500"
        ),
        Hr(cls="my-7"),
        H5("Sizing"),
        P(
            "Using Bootstrap’s typical naming structure, you can create a standard avatar, or scale it up to different sizes based on what’s needed.",
            cls="text-gray-500"
        ),
        Div(
            Div(
                avatar(avatar_size="xxl", shape="circle", src="../assets/images/avatars/avatar-1.jpg", alt="..."),
                avatar(avatar_size="xl", shape="circle", src="../assets/images/avatars/avatar-1.jpg", alt="..."),
                avatar(avatar_size="lg", shape="circle", src="../assets/images/avatars/avatar-1.jpg", alt="..."),
                avatar(avatar_size="", shape="circle", src="../assets/images/avatars/avatar-1.jpg", alt="..."),
                avatar(avatar_size="sm", shape="circle", src="../assets/images/avatars/avatar-1.jpg", alt="..."),
                avatar(avatar_size="xs", shape="circle", src="../assets/images/avatars/avatar-1.jpg", alt="..."),
                cls="card-body border" 
            ),
            Div(
                Code(
                    '<div class="avatar avatar-xxl">\n  <img src="../assets/images/avatars/avatar-1.jpg" alt="..." class="avatar-img rounded-circle">\n</div>\n...',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card card-lg"
        ),
        Hr(cls="my-7"),
        H5("Status Indicator"),
        P(
            "Add an online or offline status indicator to show user's availability.",
            cls="text-gray-500"
        ),
        Div(
            Div(
                avatar(avatar_size="xxl", shape="circle", src="../assets/images/avatars/avatar-1.jpg", alt="..."),
                avatar(avatar_size="xl", status="online", shape="circle", src="../assets/images/avatars/avatar-1.jpg", alt="..."),
                avatar(avatar_size="lg", shape="circle", src="../assets/images/avatars/avatar-1.jpg", alt="..."),
                avatar(avatar_size="", status="online", shape="circle", src="../assets/images/avatars/avatar-1.jpg", alt="..."),
                avatar(avatar_size="sm", shape="circle", src="../assets/images/avatars/avatar-1.jpg", alt="..."),
                avatar(avatar_size="xs", shape="circle", src="../assets/images/avatars/avatar-1.jpg", alt="..."),
                
                cls="card-body border"
            ),
            Div(
                Code(
                    '<div class="avatar avatar-online">\n  <img src="../assets/images/avatars/avatar-1.jpg" alt="..." class="avatar-img rounded-circle">\n</div>\n...',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        Hr(cls="my-7"),
        H5("Shape"),
        P(
            "Change the shape of an avatar with the default Bootstrap image classes.",
            cls="text-gray-500"
        ),
        Div(
            Div(
                avatar(avatar_size="xxl", src="../assets/images/avatars/avatar-1.jpg", alt="..."),
                avatar(avatar_size="xxl", shape="circle", src="../assets/images/avatars/avatar-1.jpg", alt="..."),
                avatar(avatar_size="lg", src="../assets/images/avatars/avatar-1.jpg", alt="..."),
                avatar(avatar_size="lg", shape="circle", src="../assets/images/avatars/avatar-1.jpg", alt="..."),
                avatar(avatar_size="", src="../assets/images/avatars/avatar-1.jpg", alt="..."),
                avatar(avatar_size="", shape="circle", src="../assets/images/avatars/avatar-1.jpg", alt="..."),
                
                cls="card-body border"
            ),
            Div(
                Code(
                    '<div class="avatar">\n  <img src="../assets/images/avatars/avatar-1.jpg" alt="..." class="avatar-img rounded">\n</div>\n...',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        Hr(cls="my-7"),
        H5("Ratio"),
        P(
            "Change the proportional relationship between the width and height of an avatar to 4 by 3 with an ",
            Code(".avatar-4by3"),
            " modifier.",
            cls="text-gray-500"
        ),
        Div(
            Div(
                avatar(avatar_size="xxl", src="../assets/images/avatars/avatar-1.jpg", alt="...", ratio="4by3"),
                avatar(avatar_size="xl", src="../assets/images/avatars/avatar-1.jpg", alt="...", ratio="4by3"),
                avatar(avatar_size="lg", src="../assets/images/avatars/avatar-1.jpg", alt="...", ratio="4by3"),
                avatar(src="../assets/images/avatars/avatar-1.jpg", alt="...", ratio="4by3"),
                cls="card-body border"
            ),
            Div(
                Code(
                    '<div class="avatar avatar-lg avatar-4by3">\n  <img src="../assets/images/covers/cover-28.jpg" alt="..." class="avatar-img rounded">\n</div>\n...',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        Hr(cls="my-7"),
        H5("Initials"),
        P(
            "You won't always have an image for every user, so easily use initials instead.",
            cls="text-gray-500"
        ),
        Div(
            Div(
                avatar_title(type="avatar-title", title_text="CF", shape="circle", avatar_size="xxl"),
                avatar_title(type="avatar-title", title_text="CF", shape="circle", avatar_size="xl"),
                avatar_title(type="avatar-title", title_text="CF", shape="circle", avatar_size="lg"),
                avatar_title(type="avatar-title", title_text="CF", shape="circle", avatar_size=""),
                avatar_title(type="avatar-title", title_text="CF", shape="circle", avatar_size="sm"),
                avatar_title(type="avatar-title", title_text="CF", shape="circle", avatar_size="xs"),
                cls="card-body border"
            ),
            Div(
                Code(
                    '<div class="avatar avatar-xxl">\n  <span class="avatar-title rounded-circle">CF</span>\n</div>\n...',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        Hr(cls="my-7"),
        H5("Groups"),
        P(
            "Easily group avatars of any size, shape and content with a single component. Each avatar can also use an to link to the corresponding profile.",
            cls="text-gray-500"
        ),
        Div(
            Div(
                Div(
                    Div(
                        avatar_group(src="../assets/images/avatars/avatar-1.jpg", alt="...", shape="circle", avatar_size="lg"),
                        avatar_group(src="../assets/images/avatars/avatar-1.jpg", alt="...", shape="circle", avatar_size="lg"),
                        avatar_group(src="../assets/images/avatars/avatar-1.jpg", alt="...", shape="circle", avatar_size="lg"),
                        avatar_title(type="title", title_text="CF", shape="circle", avatar_size="lg"),
                        cls="avatar-group"
                    ),
                    Div(
                        avatar_group(src="../assets/images/avatars/avatar-1.jpg", alt="...", shape="circle"),
                        avatar_group(src="../assets/images/avatars/avatar-1.jpg", alt="...", shape="circle"),
                        avatar_group(src="../assets/images/avatars/avatar-1.jpg", alt="...", shape="circle"),
                        avatar_title(type="title", title_text="CF", shape="circle"),
                        cls="avatar-group"
                    ),
                    Div(
                        avatar_group(src="../assets/images/avatars/avatar-1.jpg", alt="...", shape="circle", avatar_size="xs"),
                        avatar_group(src="../assets/images/avatars/avatar-1.jpg", alt="...", shape="circle", avatar_size="xs"),
                        avatar_group(src="../assets/images/avatars/avatar-1.jpg", alt="...", shape="circle", avatar_size="xs"),
                        avatar_title(type="title", title_text="CF", shape="circle", avatar_size="xs"),
                        cls="avatar-group"
                    ),
                    cls="card-body"
                ),
                cls="card-body border"
            ),
            Div(
                Code(
                    '<div class="avatar-group">\n  <div class="avatar">\n    <img src="../assets/images/avatars/avatar-1.jpg" alt="..." class="avatar-img rounded-circle">\n  </div>\n  ...\n</div>',
                    cls="highlight html hljs xml"
                ),
                cls="card-footer fs-sm bg-dark"
            ),
            cls="card"
        ),
        cls="px-md-10 py-10"
    )