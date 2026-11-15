# Aishwar Yadav — Professional Engineering Portfolio & GitHub Pages Site

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live%20Site-38bdf8?style=flat&logo=github)](https://aishwar2.github.io/)
[![Role](https://img.shields.io/badge/Role-Application%20Support%20Engineer-10b981?style=flat)](https://linkedin.com/in/aishwar-yadav)
[![Linux](https://img.shields.io/badge/Fleet-250%2B%20RHEL%20Nodes-f59e0b?style=flat&logo=redhat)](https://aishwar2.github.io/)
[![MySQL](https://img.shields.io/badge/Database-MySQL%208.4%2F9.7-0284c7?style=flat&logo=mysql)](https://aishwar2.github.io/)

A high-performance, responsive personal engineering portfolio designed specifically for **Aishwar Yadav** (Application Support Engineer – Linux & MySQL). Built to showcase production reliability, low-latency kernel tuning, enterprise MySQL replication, and 6+ years of mission-critical systems support to recruiters and hiring managers.

---

## 🚀 Live Demo & Repository Setup

When published to your GitHub account (`aishwar2`), your site will be live at:
👉 **`https://aishwar2.github.io/`**

---

## 📂 Project Structure

```text
├── index.html                   # Main semantic HTML5 portfolio document
├── assets/
│   ├── Aishwar_Yadav_Resume.pdf # Downloadable resume PDF (synced from your source)
│   └── favicon.svg              # Custom sysadmin terminal SVG favicon
├── css/
│   └── styles.css               # Modern styling (Dark/Light mode, CSS Grid, Glassmorphism)
├── js/
│   └── main.js                  # Interactive terminal simulator, copy-to-clipboard, theme switcher
├── .github/
│   └── workflows/
│       └── deploy.yml           # Automated GitHub Pages CI/CD workflow
├── .nojekyll                    # Ensures GitHub Pages serves all static assets as-is
├── .gitignore                   # Ignores lock files and OS temp files
└── README.md                    # Setup and deployment documentation
```

---

## ⚡ How to Publish to GitHub Pages (2-Minute Setup)

You can publish this directly using either **Option 1 (User Site: `aishwar2.github.io`)** or **Option 2 (Project Site: `portfolio`)**.

### Option 1: Main User Site (`https://aishwar2.github.io`) — Recommended!

1. Open your terminal in this directory:
   ```bash
   cd /home/Aishwar/Documents/resume
   ```

2. Initialize git and commit your files:
   ```bash
   git init
   git add .
   git commit -m "feat: initial commit of professional portfolio website"
   git branch -M main
   ```

3. Create a new repository on your GitHub account ([github.com/new](https://github.com/new)):
   - Repository name: **`aishwar2.github.io`**
   - Make it **Public**
   - Do **NOT** initialize with a README (this folder already has it)

4. Link the remote and push:
   ```bash
   git remote add origin https://github.com/aishwar2/aishwar2.github.io.git
   git push -u origin main
   ```

5. **Done!** GitHub will automatically detect the `aishwar2.github.io` name and publish your site at:
   👉 **`https://aishwar2.github.io`**

---

### Option 2: As a Project Repository (e.g. `github.com/aishwar2/portfolio`)

1. Create a repository named `portfolio` on GitHub.
2. Push your code:
   ```bash
   git init
   git add .
   git commit -m "feat: initial portfolio commit"
   git branch -M main
   git remote add origin https://github.com/aishwar2/portfolio.git
   git push -u origin main
   ```
3. Go to **Settings** → **Pages** in your GitHub repository:
   - Under **Build and deployment** > **Source**, choose **Deploy from a branch**.
   - Branch: `main` / `/(root)`.
   - Click **Save**.
   Your site will be live at: `https://aishwar2.github.io/portfolio/`

---

## 💻 Local Testing & Preview

To preview the website locally on your computer before pushing:

```bash
# Start a quick Python web server
python3 -m http.server 8000
```

Then open your browser and navigate to:
👉 `http://localhost:8000`

---

## 🌟 Key Features Built for Recruiters & Hiring Managers

- **Interactive Sysadmin Terminal Widget**: Allows technical interviewers to interact with command pills (`onload`, `mysql_fleet`, `rhel_upgrades`, `dr_failover`, `skills`) and view real configuration diagnostics.
- **Production Architecture Case Studies**:
  - *Kernel Bypass & Multicast Feed Tuning (Solarflare Onload, sysctl, NUMA, CPU Core Pinning)*
  - *Zero-Downtime RHEL 7.9 to 8.10 In-Place Fleet Migration via Leapp & Satellite*
  - *Production MySQL High Availability, GTID Replication & PITR Recovery*
  - *45-Minute Enterprise DC-to-DR Failover Benchmark*
- **One-Click Contact & Copy**: Instant copy for your email (`aishwar253@outlook.com`) and phone (`+91 8691 805492`) with toast notifications.
- **Direct Resume Download**: Links directly to `assets/Aishwar_Yadav_Resume.pdf`.
- **Theme Switcher**: Dark mode (default high-tech obsidian theme) and Light mode with persistent state.
- **Zero Heavy Dependencies**: Pure semantic HTML5, modern CSS3, and vanilla JavaScript for ultra-fast loading speed and 100/100 Lighthouse performance score.

---

## 📬 Contact & Links

- **Email**: [aishwar253@outlook.com](mailto:aishwar253@outlook.com)
- **Phone**: +91 8691 805492
- **LinkedIn**: [linkedin.com/in/aishwar-yadav](https://linkedin.com/in/aishwar-yadav)
- **GitHub**: [github.com/aishwar2](https://github.com/aishwar2)
- **Location**: Thane, Maharashtra, India
