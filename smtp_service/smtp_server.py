#!/usr/bin/env python3
"""
Direct SMTP Email Dispatch Service for Portfolio Website
---------------------------------------------------------
Accepts HTTP POST requests from the website contact form and dispatches emails
directly through Outlook / Office 365 SMTP (smtp-mail.outlook.com:587).

Zero third-party dependencies required (pure standard Python 3).
"""

import os
import sys
import json
import ssl
import smtplib
from http.server import HTTPServer, BaseHTTPRequestHandler
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate, make_msgid
from datetime import datetime

# Load configuration with environment variable fallbacks
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
LOCAL_CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.local.json")
CONFIG = {
    "smtp_host": "smtp-mail.outlook.com",
    "smtp_port": 587,
    "smtp_user": "aishwar253@outlook.com",
    "smtp_password": "",
    "receiver_email": "aishwar253@outlook.com",
    "http_host": "0.0.0.0",
    "http_port": 5000,
    "allowed_origins": "*"
}

for cfg_path in (CONFIG_FILE, LOCAL_CONFIG_FILE):
    if os.path.exists(cfg_path):
        try:
            with open(cfg_path, "r", encoding="utf-8") as f:
                CONFIG.update(json.load(f))
        except Exception as e:
            print(f"[WARN] Could not load {os.path.basename(cfg_path)}: {e}", file=sys.stderr)

# Allow environment variables to override config
CONFIG["smtp_host"] = os.getenv("SMTP_HOST", CONFIG["smtp_host"])
CONFIG["smtp_port"] = int(os.getenv("SMTP_PORT", CONFIG["smtp_port"]))
CONFIG["smtp_user"] = os.getenv("SMTP_USER", CONFIG["smtp_user"])
CONFIG["smtp_password"] = os.getenv("SMTP_PASSWORD", CONFIG["smtp_password"])
CONFIG["receiver_email"] = os.getenv("RECEIVER_EMAIL", CONFIG["receiver_email"])
CONFIG["http_host"] = os.getenv("HTTP_HOST", CONFIG["http_host"])
CONFIG["http_port"] = int(os.getenv("HTTP_PORT", CONFIG["http_port"]))
CONFIG["allowed_origins"] = os.getenv("ALLOWED_ORIGINS", CONFIG["allowed_origins"])


def send_direct_email(sender_name, sender_email, subject, message_body):
    """
    Connects directly to the Outlook SMTP server using STARTTLS and delivers the message.
    """
    host = CONFIG["smtp_host"]
    port = CONFIG["smtp_port"]
    user = CONFIG["smtp_user"]
    password = CONFIG["smtp_password"]
    receiver = CONFIG["receiver_email"]

    if not password or password == "YOUR_OUTLOOK_APP_PASSWORD_HERE":
        raise ValueError(
            "SMTP password not set! Please configure 'smtp_password' in smtp_service/config.json "
            "or set the SMTP_PASSWORD environment variable with your Outlook App Password."
        )

    # Construct MIME message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"[Portfolio Contact] {subject} - from {sender_name}"
    msg["From"] = f"{sender_name} via Portfolio <{user}>"
    msg["To"] = receiver
    msg["Reply-To"] = sender_email
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="outlook.com")

    # Plain text version
    text_content = f"""
=====================================================
NEW MESSAGE FROM PORTFOLIO CONTACT FORM
=====================================================

Sender Name : {sender_name}
Sender Email: {sender_email}
Subject     : {subject}
Date/Time   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Message Body:
-----------------------------------------------------
{message_body}
-----------------------------------------------------

To reply directly to {sender_name}, simply hit Reply in Outlook.
"""

    # HTML version
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1e293b; background-color: #f8fafc; padding: 20px; }}
    .container {{ max-width: 600px; margin: 0 auto; background: #ffffff; border-radius: 8px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }}
    .header {{ background: #0284c7; color: #ffffff; padding: 20px; }}
    .header h2 {{ margin: 0; font-size: 1.25rem; font-weight: 700; }}
    .body {{ padding: 24px; }}
    .meta-table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 0.95rem; }}
    .meta-table td {{ padding: 8px 12px; border-bottom: 1px solid #f1f5f9; }}
    .meta-label {{ font-weight: 600; color: #64748b; width: 130px; }}
    .meta-val {{ color: #0f172a; }}
    .message-box {{ background: #f8fafc; border-left: 4px solid #0284c7; padding: 16px; border-radius: 4px; font-size: 1rem; white-space: pre-wrap; word-break: break-word; color: #334155; }}
    .footer {{ background: #f1f5f9; padding: 14px 24px; font-size: 0.85rem; color: #64748b; text-align: center; border-top: 1px solid #e2e8f0; }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h2>📬 Direct Portfolio Message</h2>
    </div>
    <div class="body">
      <table class="meta-table">
        <tr>
          <td class="meta-label">From Name:</td>
          <td class="meta-val"><strong>{sender_name}</strong></td>
        </tr>
        <tr>
          <td class="meta-label">Reply Email:</td>
          <td class="meta-val"><a href="mailto:{sender_email}">{sender_email}</a></td>
        </tr>
        <tr>
          <td class="meta-label">Subject:</td>
          <td class="meta-val">{subject}</td>
        </tr>
        <tr>
          <td class="meta-label">Received At:</td>
          <td class="meta-val">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td>
        </tr>
      </table>

      <h3 style="font-size: 0.95rem; color: #475569; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.05em;">Message</h3>
      <div class="message-box">{message_body}</div>
    </div>
    <div class="footer">
      Hit <strong>Reply</strong> in your mail client to reply directly to {sender_email}.
    </div>
  </div>
</body>
</html>
"""

    msg.attach(MIMEText(text_content, "plain", "utf-8"))
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    # Connect to SMTP server with TLS
    context = ssl.create_default_context()
    with smtplib.SMTP(host, port, timeout=20) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(user, password)
        server.sendmail(user, [receiver], msg.as_string())


class SMTPRequestHandler(BaseHTTPRequestHandler):
    """
    HTTP handler to receive contact form submissions and trigger direct SMTP delivery.
    """

    def _set_cors_headers(self):
        origin = self.headers.get("Origin", "*")
        allowed = CONFIG.get("allowed_origins", "*")
        if allowed == "*" or origin in allowed.split(","):
            self.send_header("Access-Control-Allow-Origin", origin)
        else:
            self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Accept, Authorization")
        self.send_header("Access-Control-Max-Age", "86400")

    def do_OPTIONS(self):
        """Handle CORS pre-flight requests."""
        self.send_response(204)
        self._set_cors_headers()
        self.end_headers()

    def do_GET(self):
        """Health check endpoint."""
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._set_cors_headers()
        self.end_headers()

        status = {
            "status": "healthy",
            "service": "Direct Outlook SMTP Service",
            "smtp_target": CONFIG["receiver_email"],
            "smtp_host": f"{CONFIG['smtp_host']}:{CONFIG['smtp_port']}",
            "configured": bool(CONFIG["smtp_password"] and CONFIG["smtp_password"] != "YOUR_OUTLOOK_APP_PASSWORD_HERE")
        }
        self.wfile.write(json.dumps(status, indent=2).encode("utf-8"))

    def do_POST(self):
        """Handle contact form submissions."""
        content_len = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_len)

        # Parse request body (JSON or URL-encoded)
        payload = {}
        content_type = self.headers.get("Content-Type", "")

        try:
            if "application/json" in content_type:
                payload = json.loads(post_data.decode("utf-8"))
            else:
                from urllib.parse import parse_qs
                parsed = parse_qs(post_data.decode("utf-8"))
                payload = {k: v[0] for k, v in parsed.items()}
        except Exception as e:
            self.send_response(400)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self._set_cors_headers()
            self.end_headers()
            resp = {"success": False, "message": f"Malformed request body: {str(e)}"}
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return

        name = payload.get("name", "").strip()
        email = payload.get("email", "").strip()
        subject = payload.get("_subject") or payload.get("subject", "Portfolio Contact Form")
        message = payload.get("message", "").strip()

        # Validation
        if not name or not email or not message:
            self.send_response(400)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self._set_cors_headers()
            self.end_headers()
            resp = {"success": False, "message": "Missing required fields: name, email, or message."}
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return

        # Attempt direct SMTP delivery
        try:
            send_direct_email(name, email, subject, message)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self._set_cors_headers()
            self.end_headers()
            resp = {
                "success": True,
                "message": f"Message delivered directly to {CONFIG['receiver_email']} via Outlook SMTP."
            }
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Email from '{name}' <{email}> dispatched successfully.")

        except smtplib.SMTPAuthenticationError as auth_err:
            print(f"[AUTH ERROR] Outlook SMTP authentication failed: {auth_err}", file=sys.stderr)
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self._set_cors_headers()
            self.end_headers()
            resp = {
                "success": False,
                "message": "SMTP Authentication Failed. Check Outlook email and App Password in config.json."
            }
            self.wfile.write(json.dumps(resp).encode("utf-8"))

        except Exception as err:
            print(f"[ERROR] Failed to send email via SMTP: {err}", file=sys.stderr)
            self.send_response(500)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self._set_cors_headers()
            self.end_headers()
            resp = {
                "success": False,
                "message": f"SMTP Delivery Error: {str(err)}"
            }
            self.wfile.write(json.dumps(resp).encode("utf-8"))


def run_server():
    host = CONFIG["http_host"]
    port = CONFIG["http_port"]
    server_address = (host, port)
    httpd = HTTPServer(server_address, SMTPRequestHandler)

    print("=" * 60)
    print(f"  Direct Outlook SMTP Dispatch Service")
    print("=" * 60)
    print(f"  Listening on: http://{host}:{port}")
    print(f"  SMTP Relay  : {CONFIG['smtp_host']}:{CONFIG['smtp_port']} (STARTTLS)")
    print(f"  Target Mail : {CONFIG['receiver_email']}")
    print(f"  Config File : {CONFIG_FILE}")
    print("=" * 60)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Server shutting down gracefully.")
        httpd.server_close()


if __name__ == "__main__":
    run_server()
