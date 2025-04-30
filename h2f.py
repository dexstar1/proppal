from fasthtml.common import (
    FT, fast_app, serve, Titled, Form, Fieldset,
    Input, Button, Pre, Code, Select, Option,
    Textarea, Div
)

app, rt = fast_app()

@rt("/convert")
def post(html: str):
    return Pre(Code(html)) if html else ''

@rt("/")
def get():
    return Titled(
        "Convert HTML to FT",
        Form(hx_post='/convert', target_id="ft")(
            Textarea(placeholder='Paste HTML here', id="html", rows=10)
        ),
        Div(id="ft")
    )

if __name__ == "__main__":
    serve(app)
