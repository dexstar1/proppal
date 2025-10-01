from fasthtml.common import *
from starlette.middleware import Middleware 
from starlette.responses import Response, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from backend.src.middleware.auth_middleware import AuthMiddleware
from routes.admin import admin_dashboard, admin_properties_route, admin_users, admin_analytics
from routes.admin_sales import (
    admin_sales_list, admin_sale_detail, admin_sale_approve, admin_sale_reject,
    admin_payouts_list, admin_payout_pay,
    admin_sales_pending_count_fragment, admin_payouts_pending_count_fragment, admin_withdraw_pending_count_fragment,
    admin_withdraw_requests_list, admin_withdraw_request_approve, admin_withdraw_request_reject,
    admin_commissions_list, admin_commission_approve, admin_commission_reject
)
from routes.notifications import notifications_list, notifications_mark_read, notifications_unread_count_fragment, notifications_mark_all_read, notifications_dropdown_menu
from routes.realtor import (realtor_dashboard, realtor_properties, realtor_property_view, realtor_referrals, realtor_commissions, realtor_withdraw, realtor_sales)
from routes.realtor_profile import realtor_setup
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
    Link(rel='stylesheet', href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css', type='text/css'),
)

import os
import secrets

# Load .env if present
try:
    from backend.src.utils.env import load_dotenv_simple
    load_dotenv_simple()
except Exception:
    pass

if "SECRET_KEY" not in os.environ or not os.environ["SECRET_KEY"]:
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
def register_get(request: Request):
    ref = request.query_params.get("ref")
    return register_page(ref)

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

# Admin sales routes
@app.get("/admin/sales") # type: ignore
async def admin_sales_list_route(request: Request):
    return await admin_sales_list(request)

@app.get("/admin/sales/{sale_id:int}") # type: ignore
async def admin_sale_detail_route(request: Request):
    return await admin_sale_detail(request)

@app.post("/admin/sales/{sale_id:int}/approve") # type: ignore
async def admin_sale_approve_route(request: Request):
    return await admin_sale_approve(request)

@app.post("/admin/sales/{sale_id:int}/reject") # type: ignore
async def admin_sale_reject_route(request: Request):
    return await admin_sale_reject(request)

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


@app.get("/admin/properties/{property_id:int}") # type: ignore
async def admin_properties_view(request: Request):
    """View a single property"""
    return await admin_properties_route(request)


@app.get("/admin/properties/{property_id:int}/edit") # type: ignore
async def admin_properties_edit(request: Request):
    """Render edit form for a property"""
    return await admin_properties_route(request)


@app.put("/admin/properties/{property_id:int}") # type: ignore
async def admin_properties_put(request: Request):
    """Handle updating a property"""
    return await admin_properties_route(request)


@app.delete("/admin/properties/{property_id:int}") # type: ignore
async def admin_properties_delete(request: Request):
    """Handle deleting a property"""
    return await admin_properties_route(request)

@app.get("/admin/users") # type: ignore
async def admin_users_route(request: Request):
    return await admin_users(request)

@app.get("/admin/users/{user_id:int}") # type: ignore
async def admin_user_view_route(request: Request):
    from routes.admin import admin_user_view
    return await admin_user_view(request)

@app.get("/admin/users/{user_id:int}/edit") # type: ignore
async def admin_user_edit_route(request: Request):
    from routes.admin import admin_user_edit
    return await admin_user_edit(request)

@app.put("/admin/users/{user_id:int}") # type: ignore
async def admin_user_update_route(request: Request):
    from routes.admin import admin_user_update
    return await admin_user_update(request)

@app.post("/admin/users/{user_id:int}/suspend") # type: ignore
async def admin_user_suspend_route(request: Request):
    from routes.admin import admin_user_suspend
    return await admin_user_suspend(request)

@app.get("/admin/analytics") # type: ignore
async def admin_analytics_route(request: Request):
    return await admin_analytics(request)

@app.get("/admin/payouts") # type: ignore
async def admin_payouts_route(request: Request):
    return await admin_payouts_list(request)

# Admin commissions
@app.get("/admin/commissions") # type: ignore
async def admin_commissions_get(request: Request):
    return await admin_commissions_list(request)

@app.post("/admin/commissions/{commission_id}/approve") # type: ignore
async def admin_commissions_approve(request: Request):
    return await admin_commission_approve(request)

@app.post("/admin/commissions/{commission_id}/reject") # type: ignore
async def admin_commissions_reject(request: Request):
    return await admin_commission_reject(request)

# Admin withdraw requests
@app.get("/admin/withdraw-requests") # type: ignore
async def admin_withdraw_requests_get(request: Request):
    return await admin_withdraw_requests_list(request)

@app.post("/admin/withdraw-requests/{request_id}/approve") # type: ignore
async def admin_withdraw_requests_approve(request: Request):
    return await admin_withdraw_request_approve(request)

@app.post("/admin/withdraw-requests/{request_id}/reject") # type: ignore
async def admin_withdraw_requests_reject(request: Request):
    return await admin_withdraw_request_reject(request)

# Admin counts fragments
@app.get("/admin/sales/pending-count") # type: ignore
async def admin_sales_pending_count_route(request: Request):
    return await admin_sales_pending_count_fragment(request)

@app.get("/admin/payouts/pending-count") # type: ignore
async def admin_payouts_pending_count_route(request: Request):
    return await admin_payouts_pending_count_fragment(request)

# Withdraw requests pending count fragment
@app.get("/admin/withdraws/pending-count") # type: ignore
async def admin_withdraws_pending_count_route(request: Request):
    return await admin_withdraw_pending_count_fragment(request)

@app.post("/admin/payouts/{payout_id}/pay") # type: ignore
async def admin_payout_pay_route(request: Request):
    return await admin_payout_pay(request)

# Notifications
@app.get("/notifications") # type: ignore
async def notifications_list_route(request: Request):
    return await notifications_list(request)

@app.post("/notifications/{notification_id}/read") # type: ignore
async def notifications_mark_read_route(request: Request):
    return await notifications_mark_read(request)

@app.post("/notifications/mark-all-read") # type: ignore
async def notifications_mark_all_read_route(request: Request):
    return await notifications_mark_all_read(request)

@app.get("/notifications/unread-count") # type: ignore
async def notifications_unread_count_route(request: Request):
    return await notifications_unread_count_fragment(request)

@app.get("/notifications/menu") # type: ignore
async def notifications_dropdown_menu_route(request: Request):
    return await notifications_dropdown_menu(request)

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

@app.get("/realtor/properties/{property_id:int}") # type: ignore
async def realtor_property_view_route(request: Request):
    return realtor_property_view(request)

@app.get("/realtor/referrals") # type: ignore
async def realtor_referrals_route(request: Request):
    return realtor_referrals(request)

@app.get("/realtor/commissions") # type: ignore
async def realtor_commissions_route(request: Request):
    return realtor_commissions(request)

@app.get("/realtor/transactions") # type: ignore
async def realtor_transactions_route(request: Request):
    from routes.realtor import realtor_transactions
    return realtor_transactions(request)

# Realtor avatar (navbar)
@app.get("/realtor/profile/avatar") # type: ignore
async def realtor_profile_avatar(request: Request):
    from routes.realtor_profile import realtor_avatar
    return await realtor_avatar(request)

# Realtor account password change
@app.post("/realtor/account/password") # type: ignore
async def realtor_account_change_password(request: Request):
    from routes.realtor_profile import realtor_change_password
    return await realtor_change_password(request)

# Realtor account
@app.get("/realtor/account") # type: ignore
async def realtor_account_get(request: Request):
    from routes.realtor_profile import realtor_account
    return await realtor_account(request)

@app.post("/realtor/account") # type: ignore
async def realtor_account_post(request: Request):
    from routes.realtor_profile import realtor_account
    return await realtor_account(request)

# Realtor setup (profile completion)
@app.get("/realtor/setup") # type: ignore
async def realtor_setup_get(request: Request):
    return await realtor_setup(request)

@app.post("/realtor/setup") # type: ignore
async def realtor_setup_post(request: Request):
    return await realtor_setup(request)

# Realtor withdraw funds
@app.get("/realtor/withdraw") # type: ignore
async def realtor_withdraw_get(request: Request):
    return await realtor_withdraw(request)

@app.post("/realtor/withdraw") # type: ignore
async def realtor_withdraw_post(request: Request):
    return await realtor_withdraw(request)

# Backwards compat
@app.get("/realtor/payouts") # type: ignore
async def realtor_payouts_route(request: Request):
    return RedirectResponse(url="/realtor/withdraw")

@app.get("/realtor/sales") # type: ignore
async def realtor_sales_route(request: Request):
    return await realtor_sales(request)

@app.post("/realtor/sales") # type: ignore
async def realtor_sales_create_route(request: Request):
    return await realtor_sales(request)

@app.get("/realtor/sales/new") # type: ignore
async def realtor_sales_new_route(request: Request):
    return await realtor_sales(request)

@app.get("/realtor/sales/{sale_id:int}") # type: ignore
async def realtor_sales_detail_route(request: Request):
    return await realtor_sales(request)

@app.get("/realtor/sales/{sale_id:int}/edit") # type: ignore
async def realtor_sales_edit_route(request: Request):
    return await realtor_sales(request)

@app.put("/realtor/sales/{sale_id:int}") # type: ignore
async def realtor_sales_update_route(request: Request):
    return await realtor_sales(request)

@app.delete("/realtor/sales/{sale_id:int}") # type: ignore
async def realtor_sales_delete_route(request: Request):
    return await realtor_sales(request)
