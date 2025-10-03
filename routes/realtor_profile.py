from fasthtml.common import *
from components.layout import Layout
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response
from backend.src.api.realtor_profile import ensure_realtor_profile_schema, upsert_realtor_profile, get_realtor_profile
from backend.src.api.referrals import ensure_referrals_schema, set_referred_by, get_or_create_referral_code
import sqlite3
import os
import uuid

UPLOAD_DIR = "public/assets/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

async def realtor_setup(request: Request):
    user = request.scope.get('user')
    if not user:
        return RedirectResponse(url="/login")
    ensure_realtor_profile_schema()

    if request.method == 'GET':
        prof = get_realtor_profile(user.id)
        def to_val(k):
            return (prof[k] if prof and k in prof.keys() else '') if prof else ''
        # Determine referral linkage state and fetch user names
        ensure_referrals_schema()
        conn = sqlite3.connect('proppal.db'); conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT referred_by, first_name, last_name FROM users WHERE id = ?", (user.id,))
        row = cur.fetchone()
        referred_by = row['referred_by'] if row else None
        user_first = row['first_name'] if row and 'first_name' in row.keys() else ''
        user_last = row['last_name'] if row and 'last_name' in row.keys() else ''
        ref_display = None
        if referred_by:
            # Ensure referrer's code exists for display
            try:
                ref_display = get_or_create_referral_code(int(referred_by))
            except Exception:
                ref_display = None
        conn.close()
        referral_input = Div(
            Label("Referral Code", cls="form-label"),
            Input(type="text", name="referral_code", placeholder="e.g. RP000123", value=(ref_display or ""), cls="form-control", readonly=bool(referred_by), required=(not bool(referred_by))),
            Small("Required if you weren't referred during registration.", cls="text-muted") if not referred_by else Small("Linked to referrer; code cannot be changed.", cls="text-muted"),
            cls="col-md-2"
        )
        # Name inputs (always required in verification)
        first_name_input = Div(Label("First Name", cls="form-label"), Input(type="text", name="first_name", value=user_first or "", cls="form-control", required=True), cls="col-md-3")
        last_name_input = Div(Label("Last Name", cls="form-label"), Input(type="text", name="last_name", value=user_last or "", cls="form-control", required=True), cls="col-md-3")
        form = Form(
            H3("Profile Information", cls="mb-4"),
            Div(
                Div(
                    first_name_input,
                    last_name_input,
                    Div(Label("Gender", cls="form-label"), 
                    Select(
                        Option("Select", value=""),
                        Option("Male", value="male", selected=(to_val('gender')=='male')),
                        Option("Female", value="female", selected=(to_val('gender')=='female')),
                        name="gender", cls="form-select form-control", required=True
                        ), cls="col-md-3"),
                    Div(Label("Date of Birth", cls="form-label"), Input(type="date", name="date_of_birth", value=to_val('date_of_birth'), cls="form-control", required=True), cls="col-md-3"),
                    Div(Label("Address", cls="form-label"), Textarea(to_val('address'), name="address", rows="2", cls="form-control", required=True), cls="col-md-4"),
                    referral_input,
                    cls="row g-3 mb-4"
                ),
                cls="card"
            ),
            Div(
                H3("Profile Picture", cls="mb-4"),
                Div(Label("Upload Image", cls="form-label"), Input(type="file", name="profile_picture", accept=".jpg,.png,.jpeg,.webp", cls="form-control"), cls="mb-4"),
                cls="card"
            ),
            Div(
                H3("Bank Information", cls="mb-4"),
                Div(
                    Div(Label("Bank Name", cls="form-label"), Input(type="text", name="bank_name", value=to_val('bank_name'), cls="form-control", required=True), cls="col-md-4"),
                    Div(Label("Account Number", cls="form-label"), Input(type="text", name="account_number", value=to_val('account_number'), cls="form-control", required=True, pattern="\\d{10}", maxlength="10"), cls="col-md-4"),
                    Div(Label("Account Name", cls="form-label"), Input(type="text", name="account_name", value=to_val('account_name'), cls="form-control", required=True), cls="col-md-4"),
                    cls="row g-3 mb-4"
                ),
                cls="card"
            ),
            Button("Save & Continue", type="submit", cls="btn btn-primary"),
            enctype="multipart/form-data",
            hx_post="/realtor/setup",
            hx_target="#main-content",
            cls="card p-4"
        )
        # Flash toast
        flash = request.session.pop('flash', None) if hasattr(request, 'session') else None
        content = Div(H1("Complete Your Account"), form, cls="container mt-4")
        if flash and isinstance(flash, dict):
            # Guard against missing showToast when returning HTMX fragments
            content = Div(content, Script(f"window.showToast && showToast({(flash.get('message') or '')!r}, {(flash.get('level') or 'info')!r})"))
        # Wrap in Layout for full page requests to ensure #main-content exists
        return content if request.headers.get("HX-Request") else Layout(content, user_role="Realtor", show_nav=False)

    # POST
    form = await request.form()
    first_name = (form.get('first_name') or '').strip()
    last_name = (form.get('last_name') or '').strip()
    gender = form.get('gender')
    date_of_birth = form.get('date_of_birth')
    address = form.get('address')
    bank_name = form.get('bank_name')
    account_number = form.get('account_number')
    account_name = form.get('account_name')

    # Profile picture
    profile_picture = None
    file = form.get('profile_picture')
    try:
        from starlette.datastructures import UploadFile
        if isinstance(file, UploadFile) and file.filename:
            ext = os.path.splitext(file.filename)[1]
            fname = f"{uuid.uuid4()}{ext}"
            path = os.path.join(UPLOAD_DIR, fname)
            with open(path, 'wb') as f:
                f.write(await file.read())
            profile_picture = f"/assets/uploads/{fname}"
    except Exception:
        profile_picture = None

    # Server-side validation for setup (all required). On error, flash and redirect back to setup.
    def flash_and_redirect(msg: str):
        if hasattr(request, 'session'):
            request.session['flash'] = {'message': msg, 'level': 'danger'}
        return Response(headers={'HX-Redirect': '/realtor/setup'})

    if not first_name or not last_name:
        return flash_and_redirect("Please provide your first and last name.")
    if not gender or gender not in ['male','female']:
        return flash_and_redirect("Please select a valid gender.")
    if not date_of_birth:
        return flash_and_redirect("Please provide your date of birth.")
    if not address or not address.strip():
        return flash_and_redirect("Please provide your address.")
    if not bank_name or not bank_name.strip():
        return flash_and_redirect("Please provide your bank name.")
    if not account_number or not account_number.isdigit() or len(account_number) != 10:
        return flash_and_redirect("Please provide a valid 10-digit account number.")
    if not account_name or not account_name.strip():
        return flash_and_redirect("Please provide your account name.")

    # Check referral linkage/state
    ensure_referrals_schema()
    conn = sqlite3.connect('proppal.db'); conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT referred_by FROM users WHERE id = ?", (user.id,))
    row = cur.fetchone(); conn.close()
    already_linked = bool(row and row['referred_by'])
    ref_code = form.get('referral_code')
    if not already_linked and (not ref_code or not str(ref_code).strip()):
        return flash_and_redirect("Please enter a valid referral code.")

    upsert_realtor_profile(user.id, gender, date_of_birth, address, profile_picture, bank_name, account_number, account_name)
    # Save first/last name into users table (ensure columns)
    try:
        conn2 = sqlite3.connect('proppal.db'); cur2 = conn2.cursor()
        # Ensure columns
        cur2.execute("PRAGMA table_info(users)"); cols = {r[1] for r in cur2.fetchall()}
        if 'first_name' not in cols:
            try: cur2.execute("ALTER TABLE users ADD COLUMN first_name TEXT")
            except Exception: pass
        if 'last_name' not in cols:
            try: cur2.execute("ALTER TABLE users ADD COLUMN last_name TEXT")
            except Exception: pass
        cur2.execute("UPDATE users SET first_name = ?, last_name = ? WHERE id = ?", (first_name, last_name, int(user.id)))
        conn2.commit(); conn2.close()
    except Exception:
        pass
    # Link referral if provided and not already linked
    try:
        if not already_linked and ref_code:
            set_referred_by(int(user.id), str(ref_code))
    except Exception:
        pass
    if hasattr(request, 'session'):
        request.session['flash'] = {'message': 'Profile saved successfully', 'level': 'success'}
    return Response(headers={'HX-Redirect': '/realtor/dashboard'})

async def realtor_avatar(request: Request):
    user = request.scope.get('user')
    if not user or getattr(user, 'role', '') != 'realtor':
        return Span("", id="nav-profile-avatar")
    prof = get_realtor_profile(user.id)
    src = (prof['profile_picture'] if prof and 'profile_picture' in prof.keys() and prof['profile_picture'] else '/assets/img/properties/placeholder.png')
    return Img(src=src, cls="rounded-circle", style="width:32px;height:32px;object-fit:cover;", id="nav-profile-avatar")

async def realtor_account(request: Request):
    user = request.scope.get('user')
    if not user:
        return RedirectResponse(url="/login")
    ensure_realtor_profile_schema()

    if request.method == 'GET':
        prof = get_realtor_profile(user.id)
        def to_val(k):
            return (prof[k] if prof and k in prof.keys() else '') if prof else ''
        # Referral info
        ensure_referrals_schema()
        conn = sqlite3.connect('proppal.db'); conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT referred_by FROM users WHERE id = ?", (user.id,))
        rrow = cur.fetchone()
        ref_by = rrow['referred_by'] if rrow else None
        ref_by_code = get_or_create_referral_code(int(ref_by)) if ref_by else None
        my_code = None
        try:
            my_code = get_or_create_referral_code(int(user.id))
        except Exception:
            my_code = None
        conn.close()
        # Also fetch names for display
        connn = sqlite3.connect('proppal.db'); connn.row_factory = sqlite3.Row
        c2 = connn.cursor(); c2.execute("SELECT first_name, last_name FROM users WHERE id = ?", (user.id,)); nrow = c2.fetchone(); connn.close()
        name_display = (f"{(nrow['first_name'] or '').strip()} {(nrow['last_name'] or '').strip()}" if nrow else '').strip()
        summary = Div(
            H2("My Account", cls="mb-4"),
            Div(
                Div(
                    Img(src=(to_val('profile_picture') or '/assets/img/properties/placeholder.png'), cls="rounded-circle", style="width: 200px; height: 200px; object-fit: cover;")
                    ,cls="col-12 col-md-3 mb-4"
                ),
                Div(
                    Div(
                        
                    P(Strong("Name: "), Span(name_display or '—')),
                    P(Strong("Email: "), Span(getattr(user, 'email', ''))),
                    P(Strong("Gender: "), Span(to_val('gender') or '-')),
                    P(Strong("DOB: "), Span(to_val('date_of_birth') or '-')),
                    P(Strong("Address: "), Span(to_val('address') or '-')),
                    P(Strong("Bank: "), Span(to_val('bank_name') or '-')),
                    P(Strong("Account No: "), Span(to_val('account_number') or '-')),
                    P(Strong("Account Name: "), Span(to_val('account_name') or '-')),
                    P(
                        Strong("My Referral Code: "),
                        Span(my_code or '—', id='my-ref-code-account'),
                        A('Copy Code', cls='badge badge-secondary ms-2', onclick="navigator.clipboard.writeText(document.getElementById('my-ref-code-account').innerText).then(()=>{this.innerText='Copied'; setTimeout(()=>this.innerText='Copy Code',1200)})"),
                        A('Copy Link', cls='badge badge-primary ms-2', onclick="(()=>{const c=document.getElementById('my-ref-code-account').innerText||''; const link=`${location.origin}/register?ref=${c}`; navigator.clipboard.writeText(link).then(()=>{this.innerText='Link Copied'; setTimeout(()=>this.innerText='Copy Link',1200)})})()"),
                        cls='mb-2'
                    ),
                    P(Strong("Referred By Code: "), Span(ref_by_code or '—')),
                    cls="card"
                    ),
                    cls="col-12 col-md-7 card p-4 mb-4"
                ),
                cls="row mb-4"
            )
        )
        form = Form(
            Div(
                H6("Update Profile Information", cls="mb-4"),
                Div(Label("Gender", cls="form-label"), Select(
                    Option("Select", value=""),
                    Option("Male", value="male", selected=(to_val('gender')=='male')),
                    Option("Female", value="female", selected=(to_val('gender')=='female')),
                    name="gender", cls="form-select form-control"), cls="col-md-4"),
                Div(Label("Address", cls="form-label"), Textarea(to_val('address'), name="address", rows="2", cls="form-control"), cls="col-md-8"),
                cls="card col-12 g-3 my-4 p-4"
            ),
            Div(
                H6("Profile Picture", cls="mb-4"),
                Div(Label("Upload Image", cls="form-label"), Input(type="file", name="profile_picture", accept=".jpg,.png,.jpeg,.webp", cls="form-control"), cls="mb-4")
            , cls="card col-12 my-4 p-4"
            ),
            Div(
                H6("Bank Information", cls="mb-4"),
                Div(
                   Div(Label("Bank Name", cls="form-label"), Input(type="text", name="bank_name", value=to_val('bank_name'), cls="form-control"), cls="col-md-4"),
                   Div(Label("Account Number", cls="form-label"), Input(type="text", name="account_number", value=to_val('account_number'), cls="form-control"), cls="col-md-4"),
                   Div(Label("Account Name", cls="form-label"), Input(type="text", name="account_name", value=to_val('account_name'), cls="form-control"), cls="col-md-4"),
                   cls="row mb-4"
                ), cls="card col-12 my-4 p-4"
            ),
            Button("Save Changes", type="submit", cls="btn btn-primary"),
            enctype="multipart/form-data",
            hx_post="/realtor/account",
            hx_target="#main-content",
            cls="row my-4"
        )

        change_password_form = Form(
            H6("Change Password", cls="mb-4"),
            Div(Label("Current Password", cls="form-label"), Input(type="password", name="current_password", required=True, cls="form-control"), cls="mb-4"),
            Div(Label("New Password", cls="form-label"), Input(type="password", name="new_password", required=True, minlength="8", cls="form-control"), cls="mb-4"),
            Div(Label("Confirm New Password", cls="form-label"), Input(type="password", name="confirm_password", required=True, minlength="8", cls="form-control"), cls="mb-4"),
            Button("Update Password", type="submit", cls="btn btn-outline-primary"),
            hx_post="/realtor/account/password",
            hx_target="#main-content",
            cls="card row p-4 my-4"
        )
        content = Div(summary, form, change_password_form, cls="container mt-4")
        # Wrap in Layout when not HTMX
        return content if request.headers.get("HX-Request") else Layout(content, user_role="Realtor")

    # POST
    form = await request.form()
    gender = form.get('gender')
    date_of_birth = form.get('date_of_birth')
    address = form.get('address')
    bank_name = form.get('bank_name')
    account_number = form.get('account_number')
    account_name = form.get('account_name')

    # Profile picture
    profile_picture = None
    file = form.get('profile_picture')
    try:
        from starlette.datastructures import UploadFile
        if isinstance(file, UploadFile) and file.filename:
            ext = os.path.splitext(file.filename)[1]
            fname = f"{uuid.uuid4()}{ext}"
            path = os.path.join(UPLOAD_DIR, fname)
            with open(path, 'wb') as f:
                f.write(await file.read())
            profile_picture = f"/assets/uploads/{fname}"
    except Exception:
        profile_picture = None

    # Server-side light validation for updates (if provided)
    if gender and gender not in ['male','female']:
        if hasattr(request, 'session'):
            request.session['flash'] = {'message': 'Invalid gender selected', 'level': 'danger'}
        return Response(headers={'HX-Redirect': '/realtor/account'})
    if account_number and (not account_number.isdigit() or len(account_number) != 10):
        if hasattr(request, 'session'):
            request.session['flash'] = {'message': 'Account number must be 10 digits', 'level': 'danger'}
        return Response(headers={'HX-Redirect': '/realtor/account'})

    upsert_realtor_profile(user.id, gender, date_of_birth, address, profile_picture, bank_name, account_number, account_name)
    if hasattr(request, 'session'):
        request.session['flash'] = {'message': 'Account updated', 'level': 'success'}
    return Response(headers={'HX-Redirect': '/realtor/account'})

async def realtor_change_password(request: Request):
    user = request.scope.get('user')
    if not user:
        return RedirectResponse(url="/login")
    form = await request.form()
    current_password = form.get('current_password')
    new_password = form.get('new_password')
    confirm_password = form.get('confirm_password')

    from backend.src.auth import crud, security
    # Validate
    if not security.verify_password(current_password or '', user.hashed_password):
        if hasattr(request, 'session'):
            request.session['flash'] = {'message': 'Current password is incorrect', 'level': 'danger'}
        return Response(headers={'HX-Redirect': '/realtor/account'})
    if not new_password or len(new_password) < 8:
        if hasattr(request, 'session'):
            request.session['flash'] = {'message': 'New password must be at least 8 characters', 'level': 'danger'}
        return Response(headers={'HX-Redirect': '/realtor/account'})
    if new_password != (confirm_password or ''):
        if hasattr(request, 'session'):
            request.session['flash'] = {'message': 'New password and confirmation do not match', 'level': 'danger'}
        return Response(headers={'HX-Redirect': '/realtor/account'})

    # Update
    try:
        crud.update_user_password(email=getattr(user, 'email', ''), password=new_password)
        # In-app notification and optional email log
        try:
            from backend.src.api.notifications import create_notification, ensure_notifications_schema
            from backend.src.utils.mailer import send_mail
            ensure_notifications_schema()
            create_notification(int(user.id), 'Password Changed', 'Your account password was changed. If this was not you, contact support immediately.', type='security')
            # Send email via Zoho SMTP (configured via env)
            to_addr = getattr(user, 'email', '')
            if to_addr:
                send_mail(
                    to_email=to_addr,
                    subject="Your password was changed",
                    text="Your account password on Proppal was changed. If this was not you, please reset your password immediately and contact support.",
                    html="""
                        <p>Your account password on <strong>Proppal</strong> was changed.</p>
                        <p>If this was not you, please <a href='/forgot-password'>reset your password</a> immediately and contact support.</p>
                    """
                )
        except Exception:
            pass
        # Force re-login
        try:
            request.session.clear()
        except Exception:
            pass
        return Response(headers={'HX-Redirect': '/login'})
    except Exception as e:
        if hasattr(request, 'session'):
            request.session['flash'] = {'message': f'Failed to update password: {e}', 'level': 'danger'}
        return Response(headers={'HX-Redirect': '/realtor/account'})
