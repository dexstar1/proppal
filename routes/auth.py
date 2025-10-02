from fasthtml.common import *
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
from backend.src.auth import crud, security
from components.layout import Layout

async def logout(request: Request):
    """Clears the user session and redirects to login."""
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)

def forgot_password_page():
    """Renders the forgot password page form."""
    form_content = Form(
        H1("Forgot Password", cls="mb-4"),
        P("Enter your email and we will send you a link to reset your password."),
        Div(Label("Email", cls="form-label"), Input(name="email", type="email", cls="form-control", required=True), cls="mb-3"),
        Button("Send Reset Link", cls="btn btn-primary"),
        P(A("Back to Login", href="/login"), cls="mt-3"),
        hx_post="/forgot-password",
        hx_target="#main-content",
        cls="card p-4 shadow-sm"
    )
    return Layout(Div(form_content, cls="container mt-5", style="max-width: 500px;"), show_nav=False)

async def forgot_password(request: Request):
    """Handles the forgot password form submission."""
    form = await request.form()
    email = form.get("email")
    user = crud.get_user_by_email(email)
    if user:
        # Generate and save reset token
        token = security.create_reset_token()
        crud.set_password_reset_token(email=user.email, token=token)
        
        # In a real app, you would email this link.
        # For now, we print it to the console for demonstration.
        from backend.src.utils.urls import absolute_url
        reset_link = absolute_url(request, f"/reset-password?token={token}")
        print("-" * 50)
        print(f"PASSWORD RESET LINK (for demo purposes): {reset_link}")
        print("-" * 50)

    return Div("If an account with that email exists, a password reset link has been sent.", cls="alert alert-info mt-3")

def reset_password_page(token: str):
    """Renders the form to enter a new password."""
    return Form(
        H1("Reset Password", cls="mb-4"),
        Input(type="hidden", name="token", value=token),
        Div(Label("New Password", cls="form-label"), Input(name="password", type="password", cls="form-control", required=True), cls="mb-3"),
        Div(Label("Confirm New Password", cls="form-label"), Input(name="confirm_password", type="password", cls="form-control", required=True), cls="mb-3"),
        Button("Reset Password", cls="btn btn-primary"),
        hx_post="/reset-password",
        hx_target="#main-content",
        cls="card p-4 shadow-sm"
    )

async def reset_password(request: Request):
    """Handles both displaying and processing the reset password form."""
    if request.method == "GET":
        token = request.query_params.get("token")
        user = crud.get_user_by_reset_token(token)
        if not user:
            return Layout(Div(H1("Invalid Link"), P("This password reset link is invalid or has expired."), cls="container mt-5 text-center"), show_nav=False)
        return Layout(Div(reset_password_page(token), cls="container mt-5", style="max-width: 500px;"), show_nav=False)

    if request.method == "POST":
        form = await request.form()
        token = form.get("token")
        password = form.get("password")
        confirm_password = form.get("confirm_password")

        user = crud.get_user_by_reset_token(token)
        if not user:
            return Div("Invalid or expired token. Please request a new reset link.", cls="alert alert-danger mt-3")
        
        if not password or password != confirm_password:
            return Div("Passwords do not match or are empty.", cls="alert alert-danger mt-3")

        crud.update_user_password(email=user.email, password=password)
        return Div("Your password has been reset successfully. You can now ", A("login", href="/login"), ".", cls="alert alert-success mt-3")
def login_page():
    """Renders the login page form."""
    form_content = Form(
        H1("Login", cls="mb-4"),
        Div(Label("Email", cls="form-label"), Input(name="email", type="email", cls="form-control", required=True), cls="mb-3"),
        Div(Label("Password", cls="form-label"), Input(name="password", type="password", cls="form-control", required=True), cls="mb-3"),
        Button("Login", cls="btn btn-primary"),
        P(A("Don't have an account? Register here.", href="/register"), cls="mt-3"),
        hx_post="/login",
        hx_target="#main-content",
        cls="card p-4 shadow-sm"
    )
    return Layout(Div(form_content, cls="container mt-5", style="max-width: 500px;"), show_nav=False)

def register_page(ref: str | None = None):
    """Renders the registration page form."""
    hidden_ref = (Input(type="hidden", name="ref", value=ref) if ref else Fragment())
    form_content = Form(
        H1("Create an Account", cls="mb-4"),
        (Div(Span(f"Referred by code: {ref}", cls="text-muted small mb-2")) if ref else Fragment()),
        Div(Label("Email", cls="form-label"), Input(name="email", type="email", cls="form-control", required=True), cls="mb-3"),
        Div(Label("Password", cls="form-label"), Input(name="password", type="password", cls="form-control", required=True), cls="mb-3"),
        Div(Label("Confirm Password", cls="form-label"), Input(name="confirm_password", type="password", cls="form-control", required=True), cls="mb-3"),
        hidden_ref,
        Button("Register", cls="btn btn-primary", type="submit"),
        P(A("Already have an account? Login here.", href="/login"), cls="mt-3"),
        hx_post="/register",
        hx_target="#main-content",
        cls="card p-4 shadow-sm"
    )
    return Layout(Div(form_content, cls="container mt-5", style="max-width: 500px;"), show_nav=False)

async def register(request: Request):
    """Handles registration, creates a verification token, and prints the link."""
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    confirm_password = form.get("confirm_password")
    ref = form.get("ref")

    if password != confirm_password:
        return Layout(Div(Div("Passwords do not match.", cls="alert alert-danger mt-3"), register_page(ref)), show_nav=False)
    if await crud.get_user_by_email(email):
        return Layout(Div(Div("Email already registered.", cls="alert alert-danger mt-3"), register_page(ref)), show_nav=False)

    user, token = await crud.create_realtor_user(email=email, password=password)

    # If a referral code was provided, link referrer immediately
    try:
        from backend.src.api.referrals import ensure_referrals_schema, set_referred_by
        ensure_referrals_schema()
        if ref:
            set_referred_by(int(user.id), str(ref))
    except Exception:
        pass
    
    from backend.src.utils.urls import absolute_url
    verify_link = absolute_url(request, f"/verify-account?token={token}")
    # Send verification email via SMTP
    try:
        from backend.src.utils.mailer import send_mail
        send_mail(
            to_email=email,
            subject="Verify your Proppal account",
            text=f"Please verify your account by visiting: {verify_link}",
            html=f"""
                <p>Welcome to <strong>Proppal</strong>!</p>
                <p>Please verify your account by clicking the link below:</p>
                <p><a href='{verify_link}'>Verify my account</a></p>
                <p>If you did not request this, you can ignore this email.</p>
            """
        )
    except Exception:
        # Fallback to console log if email fails
        print("-" * 50)
        print(f"ACCOUNT VERIFICATION LINK: {verify_link}")
        print("-" * 50)
    
    return Layout(Div(Div("Registration successful! Please check your email for the verification link.", cls="alert alert-success mt-3"), login_page()))

async def login(request: Request):
    """Handles login, checking for verification status."""
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    
    user = await crud.get_user_by_email(email)
    if not user or not security.verify_password(password, user.hashed_password):
        return Layout(Div(Div("Invalid email or password.", cls="alert alert-danger mt-3"), login_page()), show_nav=False)
    
    if not user.is_verified:
        return Layout(Div(Div("Your account is not verified. Please check your email for the verification link.", cls="alert alert-warning mt-3"), login_page()), show_nav=False)

    request.session['user_id'] = user.id
    request.session['user_role'] = user.role
    
    if user.role == 'admin': 
        return Response(headers={'HX-Redirect': '/admin/dashboard'})
    elif user.role == 'realtor': 
        try:
            from backend.src.api.realtor_profile import is_realtor_profile_complete
            if not is_realtor_profile_complete(int(user.id)):
                return Response(headers={'HX-Redirect': '/realtor/setup'})
        except Exception:
            pass
        return Response(headers={'HX-Redirect': '/realtor/dashboard'})
    
    return Response(headers={'HX-Redirect': '/login'})

async def verify_account(request: Request):
    """Handles the account verification by validating the token."""
    token = request.query_params.get("token")
    success = crud.verify_user_by_token(token)
    if not success:
        return Layout(Div(H1("Verification Failed"), P("This verification link is invalid or has expired."), cls="container mt-5 text-center"), show_nav=False)
    return Layout(Div(H1("Account Verified!"), P("Your account has been successfully verified. You can now ", A("login", href="/login"), "."), cls="container mt-5 text-center"), show_nav=False)
