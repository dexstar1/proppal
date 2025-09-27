from fasthtml.common import *
from typing import Optional, Any

def Modal(
    modal_id: str,
    title: str,
    body_content: Any,
    footer_content: Optional[Any] = None,
    size: Optional[str] = "", # e.g., modal-sm, modal-lg, modal-xl
):
    return Div(
        Div(
            Div(
                Div(
                    H5(title, cls="modal-title"),
                    Button(
                        type="button",
                        cls="btn-close",
                        data_bs_dismiss="modal",
                        aria_label="Close"
                    ),
                    cls="modal-header"
                ),
                Div(body_content, cls="modal-body"),
                Div(footer_content, cls="modal-footer") if footer_content else None,
                cls="modal-content"
            ),
            cls=f"modal-dialog modal-dialog-centered {size}"
        ),
        cls="modal fade",
        id=modal_id,
        tabindex="-1",
        aria_labelledby=f"{modal_id}Label",
        aria_hidden="true"
    )
