from fasthtml.common import *
from typing import List, Any, Optional

def Table(
    headers: List[str],
    data: List[List[Any]],
    table_cls: Optional[str] = "table table-hover table-sm",
    header_cls: Optional[str] = "text-uppercase text-muted fs-xxs fw-bold",
    row_cls: Optional[str] = "",
    cell_cls: Optional[str] = "",
):
    thead_content = Thead(Tr(*[Th(header, scope="col", cls=header_cls) for header in headers]))

    tbody_content = Tbody(
        *[Tr(*[Td(cell, cls=cell_cls) for cell in row], cls=row_cls) for row in data]
    )

    return Div(
        Table(thead_content, tbody_content, cls=table_cls),
        cls="table-responsive"
    )
