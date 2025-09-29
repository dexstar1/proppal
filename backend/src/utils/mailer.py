import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

# Read configuration from environment
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.zoho.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))  # 587 for STARTTLS, 465 for SSL
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
SMTP_FROM_ENV = os.getenv("SMTP_FROM")  # may be invalid; we will validate below
SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "true").lower() in ("1", "true", "yes")
SMTP_DEBUG = os.getenv("SMTP_DEBUG", "false").lower() in ("1", "true", "yes")


def _resolve_from_address() -> str:
    """Return a valid From email address.
    Prefer SMTP_FROM if it looks valid, otherwise fall back to SMTP_USER.
    """
    candidate = SMTP_FROM_ENV or SMTP_USER or ""
    if "@" in candidate and "." in (candidate.split("@", 1)[-1]):
        return candidate
    # Fall back to SMTP_USER if provided
    if SMTP_USER and ("@" in SMTP_USER and "." in SMTP_USER.split("@", 1)[-1]):
        return SMTP_USER
    raise RuntimeError("SMTP_FROM/SMTP_USER is not a valid email address. Set SMTP_FROM or SMTP_USER to a full email (e.g., user@domain.com).")


def send_mail(to_email: str, subject: str, text: str, html: Optional[str] = None) -> bool:
    """
    Send an email via SMTP using environment-configured credentials.
    Requires env vars: SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS and SMTP_FROM or a valid SMTP_USER.

    Returns True on success.
    On failure, logs a concise error and raises to allow callers to handle fallbacks.
    """
    # Basic validation
    if not all([SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS, to_email]):
        missing = [k for k, v in {
            "SMTP_HOST": SMTP_HOST,
            "SMTP_PORT": SMTP_PORT,
            "SMTP_USER": SMTP_USER,
            "SMTP_PASS": "***" if SMTP_PASS else None,
            "to_email": to_email,
        }.items() if not v]
        raise RuntimeError(f"Missing required SMTP configuration values: {', '.join(missing)}")

    from_email = _resolve_from_address()

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    part1 = MIMEText(text or "", "plain")
    msg.attach(part1)
    if html:
        part2 = MIMEText(html, "html")
        msg.attach(part2)

    try:
        # Decide connection mode: SSL for 465, STARTTLS for 587 when enabled, plain otherwise
        if SMTP_PORT == 465:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
                if SMTP_DEBUG:
                    server.set_debuglevel(1)
                server.login(SMTP_USER, SMTP_PASS)
                server.sendmail(from_email, [to_email], msg.as_string())
        else:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as server:
                if SMTP_DEBUG:
                    server.set_debuglevel(1)
                server.ehlo()
                if SMTP_USE_TLS:
                    context = ssl.create_default_context()
                    server.starttls(context=context)
                    server.ehlo()
                server.login(SMTP_USER, SMTP_PASS)
                server.sendmail(from_email, [to_email], msg.as_string())
        return True
    except Exception as e:
        # Log a concise error and re-raise so callers (e.g., routes) can trigger fallbacks
        print(f"[mailer] Failed to send email to {to_email}: {e}")
        raise
