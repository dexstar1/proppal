from fasthtml.common import *
from components.sidebar import Sidebar
from components.nav import Navbar

def Layout(content, user_role: str = "Client"):
    """
    Base layout that wraps all pages with a responsive fixed/off-canvas sidebar, a top navbar, and the main content area.
    """
    # CSS for handling the responsive margin and the collapsed state of the desktop sidebar
    style = Style("""
        .main-content-wrapper {
            transition: margin-left 0.2s ease-in-out;
        }
        @media (min-width: 992px) {
            .main-content-wrapper {
                margin-left: 280px;
            }
            body.sidebar-collapsed .main-content-wrapper {
                margin-left: 0;
            }
            body.sidebar-collapsed #desktop-sidebar {
                display: none !important;
            }
        }
    """)

    # JS for the desktop sidebar toggle
    desktop_toggle_js = Script("""
        const toggleButton = document.getElementById('desktop-sidebar-toggle');
        if (toggleButton) {
            toggleButton.addEventListener('click', function() {
                document.body.classList.toggle('sidebar-collapsed');
            });
        }
    """)

    bootstrap_js = Script(src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js")

    return Div(
        style,
        Sidebar(user_role=user_role),
        Div(
            Navbar(),
            Div(
                content,
                id="main-content",
                cls="p-4"
            ),
            cls="main-content-wrapper"
        ),
        bootstrap_js,
        desktop_toggle_js
    )
