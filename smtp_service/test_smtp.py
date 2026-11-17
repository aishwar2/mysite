#!/usr/bin/env python3
"""
Test Outlook SMTP Connection & Send Diagnostic Email
----------------------------------------------------
Run this script from terminal to test credentials directly against smtp-mail.outlook.com:587.

Usage:
    python3 smtp_service/test_smtp.py
"""

import sys
import ssl
import json
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from datetime import datetime

CONFIG_PATH = "smtp_service/config.json"

for cfg_file in ("smtp_service/config.local.json", "smtp_service/config.json"):
    if os.path.exists(cfg_file):
        try:
            with open(cfg_file, "r") as f:
                config.update(json.load(f))
                CONFIG_PATH = cfg_file
        except Exception:
            pass

print("=" * 60)
print("  Outlook SMTP Connectivity & Authentication Diagnostic")
print("=" * 60)

host = config.get("smtp_host", "smtp-mail.outlook.com")
port = int(config.get("smtp_port", 587))
user = config.get("smtp_user", "aishwar253@outlook.com")
password = config.get("smtp_password", "")

if not password or password == "YOUR_OUTLOOK_APP_PASSWORD_HERE":
    print(f"\n[!] Password not yet set in {CONFIG_PATH}")
    import getpass
    password = getpass.getpass(f"Enter Outlook App Password for {user}: ")

print(f"\n1. Resolving & Connecting to {host}:{port}...")
try:
    context = ssl.create_default_context()
    with smtplib.SMTP(host, port, timeout=15) as server:
        server.set_debuglevel(1)
        print("\n2. Sending EHLO...")
        server.ehlo()

        print("\n3. Upgrading to TLS (STARTTLS)...")
        server.starttls(context=context)
        server.ehlo()

        print(f"\n4. Authenticating as '{user}'...")
        server.login(user, password)
        print("\n[+] AUTHENTICATION SUCCESSFUL!")

        print("\n5. Sending test dispatch to target mailbox...")
        msg = MIMEText(f"This is a verified test email sent via Python direct Outlook SMTP on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")
        msg["Subject"] = "✅ [TEST] Direct SMTP Dispatch Verified"
        msg["From"] = f"Portfolio Diagnostics <{user}>"
        msg["To"] = config.get("receiver_email", user)
        msg["Date"] = formatdate(localtime=True)

        server.sendmail(user, [config.get("receiver_email", user)], msg.as_string())
        print(f"\n[+] SUCCESS: Test message delivered to {config.get('receiver_email', user)}!")

except smtplib.SMTPAuthenticationError as e:
    print(f"\n[-] AUTHENTICATION FAILED: {e}")
    print("\nTroubleshooting tips:")
    print(" 1. For Outlook accounts with 2FA, generate an App Password at:")
    print("    https://account.microsoft.com/security -> Advanced Security -> App passwords")
    print(" 2. Ensure POP/IMAP/SMTP access is allowed on your Microsoft account.")
except Exception as e:
    print(f"\n[-] ERROR: {e}")
