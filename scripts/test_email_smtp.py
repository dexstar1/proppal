import os
import sys
from pathlib import Path

# Ensure project root is on sys.path so 'backend' can be imported reliably
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.src.utils.env import load_dotenv_simple
from backend.src.utils.mailer import send_mail

if __name__ == "__main__":
    # Load environment
    loaded = load_dotenv_simple()
    print(f"[test] .env loaded: {loaded}")
    present = {k: (k in os.environ) for k in ("SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASS", "SMTP_FROM", "SMTP_USE_TLS")}
    print(f"[test] SMTP keys present: {present}")
    to = os.getenv("TEST_EMAIL_TO") or os.getenv("SMTP_USER")
    if not to:
        raise SystemExit("No recipient configured. Set TEST_EMAIL_TO or SMTP_USER in environment.")
    print(f"[test] Sending test email to: {to}")
    try:
        send_mail(to, "Proppal SMTP test", "This is a test email from the Proppal SMTP check.")
        print("[test] Email send returned success.")
    except Exception as e:
        print(f"[test] Email send raised an error: {e}")
        raise
