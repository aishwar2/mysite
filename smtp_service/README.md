# Direct Outlook SMTP Dispatch Service

This service enables your portfolio website contact form to send emails directly to **`aishwar253@outlook.com`** using Microsoft Outlook's official SMTP server (`smtp-mail.outlook.com:587`).

Built with pure Python 3 standard library (`smtplib`, `email.mime`, `http.server`) — **zero third-party dependencies required**.

---

## 🚀 Quick Setup (3 Steps)

### 1. Generate an Outlook App Password
Because Microsoft requires Modern Authentication / 2FA:
1. Log in to [Microsoft Account Security](https://account.microsoft.com/security).
2. Go to **Advanced security options** > **App passwords**.
3. Click **Create a new app password**.
4. Copy the 16-character generated password (e.g., `abcd efgh ijkl mnop`).

### 2. Configure the Service
Open `smtp_service/config.json`:
```json
{
  "smtp_host": "smtp-mail.outlook.com",
  "smtp_port": 587,
  "smtp_user": "aishwar253@outlook.com",
  "smtp_password": "YOUR_16_CHAR_APP_PASSWORD_HERE",
  "receiver_email": "aishwar253@outlook.com",
  "http_host": "0.0.0.0",
  "http_port": 5000,
  "allowed_origins": "*"
}
```

### 3. Verify SMTP Connection
Run the diagnostic script:
```bash
python3 smtp_service/test_smtp.py
```
If credentials are valid, a test email will arrive in your Outlook inbox immediately.

---

## 🛠️ Running the Service

### Manual Run (Testing)
```bash
python3 smtp_service/smtp_server.py
```

### Run as a Background `systemd` Service (Production)
```bash
# 1. Copy service file to systemd directory
sudo cp smtp_service/portfolio-smtp.service /etc/systemd/system/

# 2. Reload systemd daemon
sudo systemctl daemon-reload

# 3. Enable and start the service
sudo systemctl enable --now portfolio-smtp

# 4. Check status & logs
systemctl status portfolio-smtp
journalctl -u portfolio-smtp -f
```

---

## 🌐 Endpoints

- **`GET /`** or **`GET /api/health`**: Health check.
- **`POST /api/send`**: Dispatches email directly via Outlook SMTP.
  - Payload: `{ "name": "...", "email": "...", "subject": "...", "message": "..." }`
