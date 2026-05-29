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
import os, sys, ssl, argparse, smtplib, mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
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
    ap.add_argument("--attach", action="append", default=[], help="file path to attach (repeatable)")
    a = ap.parse_args()

    html = a.html or (Path(a.html_file).read_text(encoding="utf-8") if a.html_file else None)
    text = a.text or (Path(a.text_file).read_text(encoding="utf-8") if a.text_file else None) \
        or "Your Switchy report is ready. Open in an HTML-capable client."
    pw = load_pw(a)

    # Build the text/html body as a multipart/alternative (this structure delivers
    # reliably). Only wrap in multipart/mixed when there are real attachments —
    # an empty mixed wrapper was getting dropped by Gmail.
    alt = MIMEMultipart("alternative")
    alt.attach(MIMEText(text, "plain"))
    if html:
        alt.attach(MIMEText(html, "html"))

    if a.attach:
        msg = MIMEMultipart("mixed")
        msg.attach(alt)
        for path in a.attach:
            p = Path(path)
            if not p.exists():
                sys.exit(f"Attachment not found: {path}")
            ctype, _ = mimetypes.guess_type(str(p))
            maintype, subtype = (ctype.split("/", 1) if ctype else ("application", "octet-stream"))
            part = MIMEBase(maintype, subtype)
            part.set_payload(p.read_bytes())
            encoders.encode_base6