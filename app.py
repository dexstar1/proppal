from fasthtml.common import *
from starlette.middleware import Middleware 
from starlette.responses import Response, RedirectResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from backend.src.middleware.auth_middleware import AuthMiddleware
from routes.admin import admin_dashboard, admin_properties_route, admin_users, admin_analytics, admin_payouts
from routes.realtor import (realtor_dashboard, realtor_properties, realtor_property_view, realtor_referrals, realtor_commissions, realtor_payouts)
from routes.client import client_dashboard, client_properties, client_enquiries
from routes.auth import (
    login_page, login, 
    register_page, register, 
    logout, 
    forgot_password_page, forgot_password,
    reset_password_page, reset_password, 
    verify_account
)

hdrs = (
    Link(rel='stylesheet', href='/assets/css/main.css', type='text/css'),    
    Link(rel='stylesheet', href='/assets/css/theme.min.css', type='text/css'),
    Link(rel='stylesheet', href='/assets/fonts/feather/feather.css', type='text/css'),
    Link(rel='stylesheet', href='/assets/libs/highlightjs/styles/vs2015.css', type='text/css'),
    Link(rel='stylesheet', href='/assets/libs/fortawesome/fontawesome-free/css/all.min.css', type='text/css'),
)

import os
import secrets

if "SECRET_KEY" not in os.environ:
    os.environ["SECRET_KEY"] = secrets.token_urlsafe(32)

middleware = [
    Middleware(SessionMiddleware, secret_key=os.environ["SECRET_KEY"]),
    Middleware(AuthMiddleware)
]

app = FastHTML(static_path='public', hdrs=hdrs, pico=False, middleware=middleware)

@app.route("/{fname:path}.{ext:static}")
async def static_files(fname:str, ext:str):
    """Serve static files."""
    return FileResponse(f'public/{fname}.{ext}')

@app.get("/") # type: ignore
def index():
    # Redirect to the login page by default
    return RedirectResponse(url="/login")

@app.get("/login")
def login_get():
    return login_page()

@app.post("/login")
async def login_post(request: Request):
    return await login(request)

@app.get("/register")
def register_get():
    return register_page()

@app.post("/register")
async def register_post(request: Request):
    return await register(request)

@app.get("/logout")
async def logout_route(request: Request):
    return await logout(request)

@app.get("/forgot-password")
def forgot_password_get():
    return forgot_password_page()

@app.post("/forgot-password")
async def forgot_password_post(request: Request):
    return await forgot_password(request)

@app.get("/reset-password")
def reset_password_get(request: Request):
    token = request.query_params.get("token")
    return reset_password_page(token)

@app.post("/reset-password")
async def reset_password_post(request: Request):
    return await reset_password(request)

@app.get("/verify-account")
async def verify_account_route(request: Request):
      return await verify_account(request)

@app.get("/admin/dashboard")  # type: ignore
async def admin_dashboard_route(request: Request):
    return await admin_dashboard(request)

@app.get("/admin/properties") # type: ignore
async def admin_properties_get(request: Request):
    """Handle GET /admin/properties and list view"""
    return await admin_properties_route(request)


@app.post("/admin/properties") # type: ignore
async def admin_properties_post(request: Request):
    """Handle POST /admin/properties (create)"""
    return await admin_properties_route(request)


@app.get("/admin/properties/new") # type: ignore
async def admin_properties_new(request: Request):
    """Render new property form"""
    return await admin_properties_route(request)


@app.get("/admin/properties/{property_id}") # type: ignore
async def admin_properties_view(request: Request):
    """View a single property"""
    return await admin_properties_route(request)


@app.get("/admin/properties/{property_id}/edit") # type: ignore
async def admin_properties_edit(request: Request):
    """Render edit form for a property"""
    return await admin_properties_route(request)


@app.put("/admin/properties/{property_id}") # type: ignore
async def admin_properties_put(request: Request):
    """Handle updating a property"""
    return await admin_properties_route(request)


@app.delete("/admin/properties/{property_id}") # type: ignore
async def admin_properties_delete(request: Request):
    """Handle deleting a property"""
    return await admin_properties_route(request)

@app.get("/admin/users") # type: ignore
async def admin_users_route(request: Request):
    return await admin_users(request)

@app.get("/admin/analytics") # type: ignore
async def admin_analytics_route(request: Request):
    return await admin_analytics(request)

@app.get("/admin/payouts") # type: ignore
async def admin_payouts_route(request: Request):
    return await admin_payouts(request)

@app.get("/client/dashboard") # type: ignore
async def client_dashboard_route(request: Request):
    return client_dashboard(request)

@app.get("/client/properties") # type: ignore
async def client_properties_route(request: Request):
    return client_properties(request)

@app.get("/client/enquiries") # type: ignore
async def client_enquiries_route(request: Request):
    return client_enquiries(request)

@app.get("/realtor/dashboard") # type: ignore
async def realtor_dashboard_route(request: Request):
    return realtor_dashboard(request)

@app.get("/realtor/properties") # type: ignore
async def realtor_properties_route(request: Request):
    return realtor_properties(request)

@app.get("/realtor/properties/{property_id}") # type: ignore
async def realtor_property_view_route(request: Request):
    return realtor_property_view(request)

@app.get("/realtor/referrals") # type: ignore
async def realtor_referrals_route(request: Request):
    return realtor_referrals(request)

@app.get("/realtor/commissions") # type: ignore
async def realtor_commissions_route(request: Request):
    return realtor_commissions(request)

@app.get("/realtor/payouts") # type: ignore
async def realtor_payouts_route(request: Request):
    return realtor_payouts(request)
