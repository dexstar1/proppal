from fasthtml.common import *

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
                Div(Img(src="../assets/images/avatars/avatar-1.jpg", alt="...", cls="avatar-img rounded-circle"), cls="avatar avatar-xxl"),
                Div(Img(src="../assets/images/avatars/avatar-1.jpg", alt="...", cls="avatar-img rounded-circle"), cls="avatar avatar-xl"),
                Div(Img(src="../assets/images/avatars/avatar-1.jpg", alt="...", cls="avatar-img rounded-circle"), cls="avatar avatar-lg"),
                Div(Img(src="../assets/images/avatars/avatar-1.jpg", alt="...", cls="avatar-img rounded-circle"), cls="avatar"),
                Div(Img(src="../assets/images/avatars/avatar-1.jpg", alt="...", cls="avatar-img rounded-circle"), cls="avatar avatar-sm"),
                Div(Img(src="../assets/images/avatars/avatar-1.jpg", alt="...", cls="avatar-img rounded-circle"), cls="avatar avatar-xs"),
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
                Div(Img(src="../assets/images/avatars/avatar-1.jpg", alt="...", cls="avatar-img rounded-circle"), cls="avatar avatar-xxl avatar-offline"),
                Div(Img(src="../assets/images/avatars/avatar-1.jpg", alt="...", cls="avatar-img rounded-circle"), cls="avatar avatar-xl avatar-online"),
                Div(Img(src="../assets/images/avatars/avatar-1.jpg", alt="...", cls="avatar-img rounded-circle"), cls="avatar avatar-lg avatar-offline"),
                Div(Img(src="../assets/images/avatars/avatar-1.jpg", alt="...", cls="avatar-img rounded-circle"), cls="avatar avatar-online"),
                Div(Img(src="../assets/images/avatars/avatar-1.jpg", alt="...", cls="avatar-img rounded-circle"), cls="avatar avatar-sm avatar-offline"),
                Div(Img(src="../assets/images/avatars/avatar-1.jpg", alt="...", cls="avatar-img rounded-circle"), cls="avatar avatar-xs avatar-online"),
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
                Div(Img(src="../assets/images/avatars/avatar-1.jpg", alt="...", cls="avatar-img rounded"), cls="avatar avatar-xxl"),
                Div(Img(src="../assets/images/avatars/avatar-1.jpg", alt="...", cls="avatar-img rounded-circle"), cls="avatar avatar-xxl"),
                Div(Img(src="../assets/images/avatars/avatar-1.jpg", alt="...", cls="avatar-img rounded"), cls="avatar avatar-lg"),
                Div(Img(src="../assets/images/avatars/avatar-1.jpg", alt="...", cls="avatar-img rounded-circle"), cls="avatar avatar-lg"),
                Div(Img(src="../assets/images/avatars/avatar-1.jpg", alt="...", cls="avatar-img rounded"), cls="avatar"),
                Div(Img(src="../assets/images/avatars/avatar-1.jpg", alt="...", cls="avatar-img rounded-circle"), cls="avatar"),
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
                Div(Img(src="../assets/images/covers/cover-28.jpg", alt="...", cls="avatar-img rounded"), cls="avatar avatar-xxl avatar-4by3"),
                Div(Img(src="../assets/images/covers/cover-28.jpg", alt="...", cls="avatar-img rounded"), cls="avatar avatar-xl avatar-4by3"),
                Div(Img(src="../assets/images/covers/cover-28.jpg", alt="...", cls="avatar-img rounded"), cls="avatar avatar-lg avatar-4by3"),
                Div(Img(src="../assets/images/covers/cover-28.jpg", alt="...", cls="avatar-img rounded"), cls="avatar avatar-4by3"),
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
                Div(Span("CF", cls="avatar-title rounded-circle"), cls="avatar avatar-xxl"),
                Div(Span("CF", cls="avatar-title rounded-circle"), cls="avatar avatar-xl"),
                Div(Span("CF", cls="avatar-title rounded-circle"), cls="avatar avatar-lg"),
                Div(Span("CF", cls="avatar-title rounded-circle"), cls="avatar"),
                Div(Span("CF", cls="avatar-title rounded-circle"), cls="avatar avatar-sm"),
                Div(Span("CF", cls="avatar-title rounded-circle"), cls="avatar avatar-xs"),
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
                        Div(Img(src="../assets/images/avatars/avatar-1.jpg", alt="...", cls="avatar-img rounded-circle"), cls="avatar avatar-lg"),
                        Div(Img(src="../assets/images/avatars/avatar-1.jpg", alt="...", cls="avatar-img rounded-circle"), cls="avatar avatar-lg"),
                        Div(Img(src="../assets/images/avatars/avatar-1.jpg", alt="...", cls="avatar-img rounded-circle"), cls="avatar avatar-lg"),
                        Div(Span("CF", cls="avatar-title rounded-circle"), cls="avatar avatar-lg"),
                        cls="avatar-group"
                    ),
                    Div(
                        Div(Img(src="../assets/images/avatars/avatar-1.jpg", alt="...", cls="avatar-img rounded-circle"), cls="avatar"),
                        Div(Img(src="../assets/images/avatars/avatar-1.jpg", alt="...", cls="avatar-img rounded-circle"), cls="avatar"),
                        Div(Img(src="../assets/images/avatars/avatar-1.jpg", alt="...", cls="avatar-img rounded-circle"), cls="avatar"),
                        Div(Span("CF", cls="avatar-title rounded-circle"), cls="avatar"),
                        cls="avatar-group"
                    ),
                    Div(
                        Div(Img(src="../assets/images/avatars/avatar-1.jpg", alt="...", cls="avatar-img rounded-circle"), cls="avatar avatar-xs"),
                        Div(Img(src="../assets/images/avatars/avatar-1.jpg", alt="...", cls="avatar-img rounded-circle"), cls="avatar avatar-xs"),
                        Div(Img(src="../assets/images/avatars/avatar-1.jpg", alt="...", cls="avatar-img rounded-circle"), cls="avatar avatar-xs"),
                        Div(Span("CF", cls="avatar-title rounded-circle"), cls="avatar avatar-xs"),
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