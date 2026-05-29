#!/usr/bin/env python3
"""
send_email.py — real SMTP sender for the Switchy weekly report (and any HTML email).
Sends through Gmail using an App Password (NOT the account password), so the Monday
task can actually deliver to the inbox instead of leaving a draft.

CREDENTIALS (never printed, never committed):
- Sender address: --from or env GMAIL_SENDER (default graehamwatts@gmail.com)
- App password:   file C:\\Users\\Graeham Watts\\Documents\\Claude\\Skills\\gmail-app-password.txt
                  (or --pwfile, or env GMAIL_APP_PASSWORD). This is a 16-char Google
                  App Password generated at myaccount.google.com/apppasswords.

USAGE:
  python send_email.py --to a@b.com --subject "..." --html-file report.html [--text-file body.txt]
Exit 0 on success; non-zero with a message on failure.
"""
import os, sys, ssl, argparse, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

DEFAULT_PWFILE = Path.home().parent / "Graeham Watts" / "Documents" / "Claude" / "Skills" / "gmail-app-password.txt"


def load_pw(args):
    if args.pwfile and Path(args.pwfile).exists():
        return Path(args.pwfile).read_text(encoding="utf-8").strip().replace(" ", "")
    env = os.environ.get("GMAIL_APP_PASSWORD")
    if env:
        return env.strip().replace(" ", "")
    # common locations
    for p in [DEFAULT_PWFILE, Path("gmail-app-password.txt"),
              Path("/sessions") / os.environ.get("SESSION", "") / "mnt/Skills/gmail-app-password.txt"]:
        try:
            if p.exists():
                return p.read_text(encoding="utf-8").strip().replace(" ", "")
        except OSError:
            pass
    sys.exit("No Gmail app password found (--pwfile / GMAIL_APP_PASSWORD / gmail-app-password.txt).")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--to", required=True, action="append", help="recipient (repeatable)")
    ap.add_argument("--subject", required=True)
    ap.add_argument("--html-file")
    ap.add_argument("--text-file")
    ap.add_argument("--html")
    ap.add_argument("--text")
    ap.add_argument("--from", dest="sender", default=os.environ.get("GMAIL_SENDER", "graehamwatts@gmail.com"))
    ap.add_argument("--pwfile")
    a = ap.parse_args()

    html = a.html or (Path(a.html_file).read_text(encoding="utf-8") if a.html_file else None)
    text = a.text or (Path(a.text_file).read_text(encoding="utf-8") if a.text_file else None) \
        or "Your Switchy report is ready. Open in an HTML-capable client."
    pw = load_pw(a)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = a.subject
    msg["From"] = a.sender
    msg["To"] = ", ".join(a.to)
    msg.attach(MIMEText(text, "plain"))
    if html:
        msg.attach(MIMEText(html, "html"))

    ctx = ssl.create_default_context()
    # try STARTTLS:587 then SSL:465
    last = None
    for host, port, mode in [("smtp.gmail.com", 587, "starttls"), ("smtp.gmail.com", 465, "ssl")]:
        try:
            if mode == "starttls":
                s = smtplib.SMTP(host, port, timeout=30); s.starttls(context=ctx)
            else:
                s = smtplib.SMTP_SSL(host, port, context=ctx, timeout=30)
            s.login(a.sender, pw)
            s.sendmail(a.sender, a.to, msg.as_string())
            s.quit()
            print(f"SENT via {host}:{port} to {', '.join(a.to)}")
            return
        except Exception as e:
            last = f"{host}:{port} -> {type(e).__name__}: {e}"
            continue
    sys.exit(f"Send failed. Last error: {last}")


if __name__ == "__main__":
    main()
