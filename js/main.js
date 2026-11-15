/* ==========================================================================
   AISHWAR YADAV - PORTFOLIO INTERACTIVE SCRIPTS
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initNavigation();
  initTerminal();
  initCopyActions();
  initStatsCounter();
  initContactForm();
  initBackToTop();
});

/* --------------------------------------------------------------------------
   Theme Switcher (Dark / Light)
   -------------------------------------------------------------------------- */
function initTheme() {
  const themeToggle = document.getElementById('theme-toggle');
  const storedTheme = localStorage.getItem('ay-theme') || 'dark';

  document.documentElement.setAttribute('data-theme', storedTheme);
  updateThemeIcon(storedTheme);

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const currentTheme = document.documentElement.getAttribute('data-theme');
      const newTheme = currentTheme === 'light' ? 'dark' : 'light';
      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('ay-theme', newTheme);
      updateThemeIcon(newTheme);
    });
  }
}

function updateThemeIcon(theme) {
  const themeToggle = document.getElementById('theme-toggle');
  if (!themeToggle) return;
  if (theme === 'light') {
    themeToggle.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
      </svg>`;
    themeToggle.setAttribute('aria-label', 'Switch to dark theme');
  } else {
    themeToggle.innerHTML = `
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="5"></circle>
        <line x1="12" y1="1" x2="12" y2="3"></line>
        <line x1="12" y1="21" x2="12" y2="23"></line>
        <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
        <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
        <line x1="1" y1="12" x2="3" y2="12"></line>
        <line x1="21" y1="12" x2="23" y2="12"></line>
        <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
        <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
      </svg>`;
    themeToggle.setAttribute('aria-label', 'Switch to light theme');
  }
}

/* --------------------------------------------------------------------------
   Mobile Navigation & Scroll Spy
   -------------------------------------------------------------------------- */
function initNavigation() {
  const menuBtn = document.getElementById('mobile-menu-btn');
  const navLinks = document.getElementById('nav-links');
  const links = document.querySelectorAll('.nav-link');

  if (menuBtn && navLinks) {
    menuBtn.addEventListener('click', () => {
      navLinks.classList.toggle('mobile-active');
    });

    links.forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('mobile-active');
      });
    });
  }

  // Active section scroll highlighting
  const sections = document.querySelectorAll('section[id]');
  window.addEventListener('scroll', () => {
    const scrollY = window.pageYOffset;
    sections.forEach(current => {
      const sectionHeight = current.offsetHeight;
      const sectionTop = current.offsetTop - 120;
      const sectionId = current.getAttribute('id');
      const navItem = document.querySelector(`.nav-links a[href*="${sectionId}"]`);
      if (navItem) {
        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
          navItem.classList.add('active');
        } else {
          navItem.classList.remove('active');
        }
      }
    });
  });
}

/* --------------------------------------------------------------------------
   Interactive Sysadmin Terminal
   -------------------------------------------------------------------------- */
const terminalResponses = {
  uptime: ` 20:05:00 up 6+ years, 250+ enterprise nodes active
 Status: 100% operational | Incidents: 0 unhandled
 SLA Compliance: 99.99% across financial trading platforms`,

  onload: `[onload_stackdump] Solarflare Onload Kernel Bypass v8.1
 Multi-cast market feeds: Jitter 0.00ms, Dropped packets: 0
 CPU Core Pinning: Isolated cores 2-15 on NUMA Node 0 & 1
 Network Ring Buffers: RX 4096 / TX 4096 [Maximized]`,

  mysql: `[mysqladmin -u root -p ping]
 mysqld is alive! (MySQL 8.4 -> 9.7 fleet)
 Source-Replica Replication: GTID Synchronized | Lag: 0s
 Backup Status: Percona XtraBackup daily PITR verified
 Active DB Fleet: 25+ production databases operating normal`,

  rhel: `[leapp upgrade --target 8.10 --status]
 Migration Status: Completed across 250+ RHEL instances
 Strategy: Leapp in-place utility with Red Hat Satellite orchestration
 Unplanned Downtime: 0 minutes | Rollback occurrences: 0`,

  dr: `[dr-benchmark --verify-failover]
 Benchmark Target: < 60 mins SLA
 Current Validated Failover: 45 minutes DC to DR
 Storage: LVM volume groups & SAN snapshot sync verified`,

  skills: `[cat /etc/sysconfig/competencies]
 LINUX   : RHEL (7.x/8.x/9.x), Ubuntu, Leapp, Satellite, Onload, Kernel sysctl
 DB      : MySQL 8.4/9.7, Replication, GTID, EXPLAIN Tuning, XtraBackup
 CLOUD   : AWS (EC2, S3, IAM, VPC, CloudWatch, SSM), VMware, Nutanix
 AUTOMATE: Bash scripting, Ansible, Ansible Vault, Cron, Git
 TRIAGE  : Nagios Core/XI, systemd, journalctl, grep/awk/sed, RCA`,

  contact: `[cat /etc/motd/contact_info]
 Name    : Aishwar Yadav
 Title   : Application Support Engineer – Linux & MySQL
 Email   : aishwar253@outlook.com
 Phone   : +91 8691 805492
 LinkedIn: linkedin.com/in/aishwar-yadav
 GitHub  : github.com/aishwar2
 Location: Thane, Maharashtra, India`
};

function initTerminal() {
  const terminalBody = document.getElementById('terminal-body');
  const chips = document.querySelectorAll('.terminal-chip');
  if (!terminalBody) return;

  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      const cmdKey = chip.getAttribute('data-cmd');
      executeCommand(cmdKey, terminalBody);
    });
  });
}

function executeCommand(key, terminalBody) {
  if (key === 'clear') {
    terminalBody.innerHTML = `
      <div class="terminal-line">
        <span class="terminal-prompt">aishwar@prod-fleet-01:~$</span> <span class="terminal-cmd"># Screen cleared. Click a quick command below or explore skills.</span>
      </div>
    `;
    return;
  }

  const promptCmds = {
    uptime: 'uptime',
    onload: 'onload_stackdump --status',
    mysql: 'mysqladmin -u aishwar -p ping && check_repl',
    rhel: 'satellite-installer --check-rhel-fleet',
    dr: 'run-dr-failover-benchmark.sh',
    skills: 'cat /etc/sysconfig/competencies',
    contact: 'cat /etc/motd/contact_info'
  };

  const cmdText = promptCmds[key] || key;
  const responseText = terminalResponses[key] || 'Command not found. Try one of the quick chips below.';

  const lineDiv = document.createElement('div');
  lineDiv.className = 'terminal-line';
  lineDiv.innerHTML = `
    <div>
      <span class="terminal-prompt">aishwar@prod-fleet-01:~$</span> <span class="terminal-cmd">${cmdText}</span>
    </div>
    <div class="terminal-output highlight">${escapeHtml(responseText)}</div>
  `;

  terminalBody.appendChild(lineDiv);
  terminalBody.scrollTop = terminalBody.scrollHeight;
}

function escapeHtml(text) {
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  };
  return text.replace(/[&<>"']/g, m => map[m]);
}

/* --------------------------------------------------------------------------
   Copy to Clipboard & Toast
   -------------------------------------------------------------------------- */
function initCopyActions() {
  const copyButtons = document.querySelectorAll('[data-copy]');
  copyButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const textToCopy = btn.getAttribute('data-copy');
      navigator.clipboard.writeText(textToCopy).then(() => {
        showToast(`Copied to clipboard: ${textToCopy}`);
      }).catch(() => {
        showToast('Failed to copy to clipboard');
      });
    });
  });
}

function showToast(message) {
  let toast = document.getElementById('toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'toast';
    toast.className = 'toast';
    document.body.appendChild(toast);
  }
  toast.innerHTML = `
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="20 6 9 17 4 12"></polyline>
    </svg>
    <span>${message}</span>
  `;
  toast.classList.add('show');
  setTimeout(() => {
    toast.classList.remove('show');
  }, 3000);
}

/* --------------------------------------------------------------------------
   Metrics Counter Animation
   -------------------------------------------------------------------------- */
function initStatsCounter() {
  const statsElements = document.querySelectorAll('.stat-number');
  if (!statsElements.length) return;

  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const target = parseFloat(el.getAttribute('data-target'));
        const suffix = el.getAttribute('data-suffix') || '';
        const prefix = el.getAttribute('data-prefix') || '';
        animateValue(el, 0, target, 1600, prefix, suffix);
        obs.unobserve(el);
      }
    });
  }, { threshold: 0.5 });

  statsElements.forEach(el => observer.observe(el));
}

function animateValue(obj, start, end, duration, prefix, suffix) {
  let startTimestamp = null;
  const isFloat = end % 1 !== 0;

  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp;
    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
    const easeOutQuad = 1 - (1 - progress) * (1 - progress);
    const current = easeOutQuad * (end - start) + start;
    obj.innerHTML = prefix + (isFloat ? current.toFixed(1) : Math.floor(current)) + suffix;
    if (progress < 1) {
      window.requestAnimationFrame(step);
    } else {
      obj.innerHTML = prefix + end + suffix;
    }
  };
  window.requestAnimationFrame(step);
}

/* --------------------------------------------------------------------------
   Contact Form Handling
   -------------------------------------------------------------------------- */
function initContactForm() {
  const form = document.getElementById('contact-form');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = document.getElementById('sender-name')?.value || 'Recruiter/Manager';
    const email = document.getElementById('sender-email')?.value || '';
    const subject = document.getElementById('sender-subject')?.value || 'Job Opportunity / Technical Inquiry';
    const message = document.getElementById('sender-message')?.value || '';

    const mailtoLink = `mailto:aishwar253@outlook.com?subject=${encodeURIComponent(subject + ' - via Portfolio from ' + name)}&body=${encodeURIComponent('From: ' + name + ' (' + email + ')\n\n' + message)}`;

    window.location.href = mailtoLink;
    showToast('Launching email client to message Aishwar...');
  });
}

/* --------------------------------------------------------------------------
   Back to Top Button
   -------------------------------------------------------------------------- */
function initBackToTop() {
  const btn = document.getElementById('back-to-top');
  if (!btn) return;

  window.addEventListener('scroll', () => {
    if (window.pageYOffset > 400) {
      btn.classList.add('visible');
    } else {
      btn.classList.remove('visible');
    }
  });

  btn.addEventListener('click', () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });
}
