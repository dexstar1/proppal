from fasthtml.common import *
from components.sidebar import Sidebar
from components.nav import Navbar


def Layout(content, user_role: str = "Client", show_nav: bool = True, user_display: str | None = None):
    """
    Base layout that wraps all pages with a responsive fixed/off-canvas sidebar, a top navbar, and the main content area.
    Set show_nav=False for public pages (e.g., login/register) to avoid rendering authenticated UI elements.
    """


    bootstrap_js = Script(src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js")

    # Minimal offcanvas CSS to ensure correct hidden/slide behavior if Bootstrap CSS is not present
    offcanvas_style = Style("""
        .offcanvas {
            position: fixed;
            top: 0;
            bottom: 0;
            z-index: 1045;
            visibility: hidden;
            transform: translateX(-100%);
            transition: transform .3s ease-in-out, visibility 0s linear .3s;
            background-color: inherit;
        }
        .offcanvas-start { left: 0; width: 280px; }
        .offcanvas.show {
            visibility: visible;
            transform: none;
            transition: transform .3s ease-in-out;
        }
        .offcanvas-backdrop { position: fixed; top:0; left:0; width:100%; height:100%; background-color: rgba(0,0,0,.5); z-index: 1040; }
        .offcanvas-backdrop.fade { opacity: 0; transition: opacity .15s linear; }
        .offcanvas-backdrop.show { opacity: .5; }
    """)

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
            offcanvas_style,
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

    
    mobile_footnav = Div(
        A(I(cls="fa-solid fa-gauge"), href="/realtor/dashboard", hx_get="/realtor/dashboard", hx_target="#main-content", hx_push_url="true", data_bs_dismiss="offcanvas", cls="text-white btn btn-dark", title="View"),
        A(I(cls="fa-solid fa-building"), href="/realtor/dashboard", hx_get="/realtor/dashboard", hx_target="#main-content", hx_push_url="true", data_bs_dismiss="offcanvas", cls="text-white btn btn-dark", title="View"),
        A(I(cls="fa fa-solid fa-chart-line"), href="/realtor/sales", hx_get="/realtor/sales", hx_target="#main-content", hx_push_url="true", data_bs_dismiss="offcanvas", cls="text-white btn btn-dark", title="View"),
        A(I(cls="fa-solid fa-wallet"), href="/realtor/withdraw", hx_get="/realtor/withdraw", hx_target="#main-content", hx_push_url="true", data_bs_dismiss="offcanvas", cls="text-white btn btn-dark", title="View"),
        A(I(cls="fe fe-menu"), id="hamburger", cls="text-white btn btn-dark", title="Menu", data_bs_toggle="offcanvas", data_bs_target="#mobileSidebar", aria_controls="mobileSidebar"),
        id="foot_nav",
        cls="d-flex d-lg-none border-top"
    )

    offcanvas_close_js = Script("""
        document.addEventListener('click', function(ev){
            const a = ev.target.closest('#mobileSidebar a, #foot_nav a');
            if (!a) return;
            if (a.id === 'hamburger') return;
            const el = document.getElementById('mobileSidebar');
            if (!el) return;
            const inst = bootstrap.Offcanvas.getInstance(el);
            if (inst) { inst.hide(); }
        });
    """)

    return Div(
        offcanvas_style,
        Sidebar(user_role=user_role, user_display=user_display),
        Div(
            Div(Navbar(user_role=user_role), cls="d-sm-none d-lg-flex"),
            Div(
                content,
                id="main-content",
                cls="p-8", style="background-color:#f5f6fa;"
            ),
            mobile_footnav,
            cls="main-content-wrapper"
        ),
        toast_container,
        bootstrap_js,
        toast_js,
        offcanvas_close_js
    )
