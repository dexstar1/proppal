from fasthtml.common import *
from components.sidebar import Sidebar
from components.nav import Navbar


def Layout(content, user_role: str = "Client", show_nav: bool = True):
    """
    Base layout that wraps all pages with a responsive fixed/off-canvas sidebar, a top navbar, and the main content area.
    Set show_nav=False for public pages (e.g., login/register) to avoid rendering authenticated UI elements.
    """
    # CSS for handling the responsive margin and the collapsed state of the desktop sidebar
    style = Style("""
        .main-content-wrapper {
            transition: margin-left 0.2s ease-in-out;
        }
        @media (min-width: 992px) {
            .main-content-wrapper {
                margin-left: 240px;
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

    # Bootstrap toast helper
    toast_container = Div(id="toast-container", cls="position-fixed top-0 end-0 p-3", style="z-index: 1100;")
    toast_js = Script("""
        window.showToast = function(message, type) {
            try {
                const container = document.getElementById('toast-container');
                const toastEl = document.createElement('div');
                const bg = type === 'success' ? 'bg-success' : (type === 'danger' ? 'bg-danger' : 'bg-info');
                toastEl.className = `toast text-white ${bg}`;
                toastEl.setAttribute('role', 'alert');
                toastEl.setAttribute('aria-live', 'assertive');
                toastEl.setAttribute('aria-atomic', 'true');
                toastEl.innerHTML = `
                    <div class=\"d-flex\">
                        <div class=\"toast-body\">${message}</div>
                        <button type=\"button\" class=\"btn-close btn-close-white me-2 m-auto\" data-bs-dismiss=\"toast\" aria-label=\"Close\"></button>
                    </div>`;
                container.appendChild(toastEl);
                const toast = new bootstrap.Toast(toastEl, { delay: 4000 });
                toast.show();
                toastEl.addEventListener('hidden.bs.toast', () => toastEl.remove());
            } catch (e) {}
        }
    """)

    if not show_nav:
        # Public/simple layout without sidebar/navbar to avoid protected HTMX calls
        return Div(
            style,
            Div(
                content,
                id="main-content",
                cls="p-8",
                style="background-color:#f5f6fa;"
            ),
            toast_container,
            bootstrap_js,
            toast_js
        )

    return Div(
        style,
        Sidebar(user_role=user_role),
        Div(
            Navbar(user_role=user_role),
            Div(
                content,
                id="main-content",
                cls="p-8", style="background-color:#f5f6fa;"
            ),
            cls="main-content-wrapper"
        ),
        toast_container,
        bootstrap_js,
        desktop_toggle_js,
        toast_js
    )
