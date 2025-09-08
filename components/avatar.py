from fasthtml.common import *

def avatar(src, alt, shape=None, avatar_size=None, status=None, ratio=None):
    shape_class = "rounded-circle" if shape == "circle" else "rounded"
    online_status = f"avatar-{status}" if status else ""
    avatar_ratio = "avatar-4by3" if ratio == "4by3" else ""
    the_size = f"avatar-{avatar_size}"

    return Div(
        Img(
            src=src,
            alt=alt,
            cls=f"avatar-img {shape_class}"
        ),
        cls=f"avatar {the_size} {avatar_ratio} {online_status}"
    ) 

def avatar_title(type, title_text, shape=None, avatar_size=None):
    shape_class = "rounded-circle" if shape == "circle" else "rounded"
    the_size = f"avatar-{avatar_size}"
    
    return Div(
                Span(title_text, cls=f"{type} {shape_class}"), 
                cls=f"avatar {the_size}"
        ),       

def avatar_group(src, alt, shape=None, avatar_size=None):
    shape_class = "rounded-circle" if shape == "circle" else "rounded"
    the_size = f"avatar-{avatar_size}"
    return Div(Img(src=src, alt="...", cls=f"avatar-img {shape_class}"), 
               cls=f"avatar {the_size}"),


