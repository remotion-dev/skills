#!/usr/bin/env python3
"""
Send the postcard options preview email via Gmail SMTP.

Reads the Gmail App Password from C:\\Users\\Graeham Watts\\Documents\\Claude\\Skills\\gmail-app-password.txt
Sends FROM graehamwatts@gmail.com TO Graeham + Peter + Ellie.

Usage:
    python send_options_email.py <html_path> "<subject>" <plaintext_path>

Or from Python:
    from send_options_email import send_options_email
    send_options_email(html_body, subject, plaintext_body)
"""
import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

# Locked recipients (matches design-tokens.md continuity rule)
SENDER = "graehamwatts@gmail.com"
RECIPIENTS = ["graehamwatts@gmail.com", "graehamwattsvideo@gmail.com", "graehamwattsvideo2@gmail.com"]  # Graeham + Peter

# Credential resolution (2026-06-29, per Fugu reliability review):
#   1. Env var GMAIL_APP_PASSWORD  — the ONLY source in production (GitHub Actions secret).
#   2. Local Windows file          — convenience for manual/interactive runs only.
# The old APP_PASSWORD_FILE_LINUX path was pinned to a retired Cowork session id
# (`inspiring-awesome-hawking`) and silently failed credential resolution. It has been
# REMOVED — production credentials must come from the env-var secret, never a local path.
APP_PASSWORD_FILE = Path(r"C:\Users\Graeham Watts\Documents\Skills LLMS\Claude\Skills\gmail-app-password.txt")


def load_app_password():
    """Resolve the Gmail App Password: env var first (production), then local file. Returns None if not found."""
    env_pwd = os.environ.get("GMAIL_APP_PASSWORD", "").strip().replace(" ", "")
    if env_pwd and env_pwd != "PASTE_YOUR_GMAIL_APP_PASSWORD_HERE":
        return env_pwd
    if APP_PASSWORD_FILE.exists():
        pwd = APP_PASSWORD_FILE.read_text().strip().replace(" ", "")
        if pwd and pwd != "PASTE_YOUR_GMAIL_APP_PASSWORD_HERE":
            return pwd
    return None


def send_options_email(html_body: str, subject: str, plaintext_body: str = ""):
    """Send the options preview email to both Graeham + Peter via Gmail SMTP."""
    app_password = load_app_password()
    if not app_password:
        raise RuntimeError(
            "Gmail App Password not found. Set the GMAIL_APP_PASSWORD env var (production / "
            f"GitHub Actions secret), or save it to {APP_PASSWORD_FILE} for local runs.\n"
            "Generate one at https://myaccount.google.com/apppasswords."
        )

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"Graeham Watts <{SENDER}>"
    msg["To"] = ", ".join(RECIPIENTS)

    if plaintext_body:
        msg.attach(MIMEText(plaintext_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER, app_password)
        server.sendmail(SENDER, RECIPIENTS, msg.as_string())

    return {"sent_to": RECIPIENTS, "subject": subject}


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: send_options_email.py <html_path> '<subject>' [<plaintext_path>]")
        sys.exit(1)

    html_path = sys.argv[1]
    subject = sys.argv[2]
    plaintext_path = sys.argv[3] if len(sys.argv) > 3 else None

    html_body = Path(html_path).read_text(encoding="utf-8")
    plaintext_body = Path(plaintext_path).read_text(encoding="utf-8") if plaintext_path else ""

    result = send_options_email(html_body, subject, plaintext_body)
    print(f"SENT to {result['sent_to']}: {result['subject']}")
