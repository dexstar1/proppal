from fasthtml.common import *

    
def product_table(entry):
    sizes = entry[4].split(",")  # Assuming size is the 5th column
    return Tr(
        Td(P(f"{entry[1]}")),
        Td(P(f"{entry[2]}")),
        Td(P(f"${entry[3]:.2f}")),
        Td(P(f"{', '.join(sizes)}")),
        Td(Img(src=entry[5], alt="Featured Image", style="width: 35px; height: auto;")),
        # Div(
        #     *[Img(src=img, alt="Gallery Image", style="width: 100px; height: auto; margin-right: 10px;")
        #       for img in entry[6].split(",")],
        #     cls="flex"
        # ),
        Td(Footer(Small(Em(f"{entry[7]}")))),
        Td(Div
           (
            A("Edit",
              href="#",
              hx_get=f"/edit/{entry[0]}",
              hx_target="#form-container",
              hx_swap="innerHTML"),
            A("Delete",
              href="#",
              hx_post=f"/delete/{entry[0]}",
              hx_target="#product-list",
              hx_swap="outerHTML",
              style="color: red;",
              hx_confirm="Are you sure you want to delete this message?"),
        )
    )
    )
