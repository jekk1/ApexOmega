import requests
from urllib.parse import urlparse

# * Atlas Kerentanan Web (CORS, SSRF, Host Injection, Sensitive Paths)
class VulnAtlas:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {'User-Agent': 'ApexOmega/4.9 (X11; Linux x86_64)'}
        
        # * Daftar 50+ path sensitif selevel Kali Linux (wordlist internal)
        self.sensitivePaths = [
            ".env", ".git/config", ".vscode/settings.json", "web.config", "phpinfo.php",
            "config.php", "db.sql", "backup.zip", ".htaccess", "robots.txt", ".ssh/id_rsa",
            "server-status", "server-info", "Dockerfile", "docker-compose.yml", "package-lock.json",
            "composer.json", "artisan", "cgi-bin/", "admin/", "administrator/", "wp-config.php",
            "wp-config.php.bak", "wp-config.php.old", "config.yml", "application.yml", "settings.py",
            "local_settings.py", "database.yml", "node_modules/", "vendor/", "sql.zip", "data.sql",
            "temp/", "tmp/", "upload/", "uploads/", "files/", "images/", "assets/", "static/",
            "media/", ".DS_Store", "Thumbs.db", ".bash_history", ".mysql_history", "error_log",
            "logs/", "test.php", "info.php", "dev.php", "setup.php", "install.php"
        ]

    # * Cek Host Header Injection (Bypass internal routing)
    def checkHostInjection(self, url):
        evilHost = "evil-apex.local"
        try:
            res = self.session.get(url, headers={"Host": evilHost}, timeout=5)
            # * Jika evilHost terpantul di Location atau Link, ada indikasi vuln
            if evilHost in res.headers.get('Location', '') or evilHost in res.text:
                return evilHost
            return None
        except Exception:
            return None

    # * Audit CORS Misconfiguration (Wildcard Check)
    def auditCors(self, url):
        try:
            res = self.session.get(url, headers={"Origin": "https://evil-attacker.com"}, timeout=5)
            aco = res.headers.get('Access-Control-Allow-Origin', '')
            acac = res.headers.get('Access-Control-Allow-Credentials', '')
            
            if aco == "*" or aco == "https://evil-attacker.com":
                diag = f"Origin Allowed: {aco}"
                if acac == "true": diag += " (Credentials: TRUE - HIGH RISK)"
                return diag
            return None
        except Exception:
            return None

    # * Fuzzing 50+ path sensitif secara otomatis
    def fuzzSensitivePaths(self, baseUrl):
        found = []
        base = baseUrl.rstrip('/')
        for p in self.sensitivePaths:
            target = f"{base}/{p}"
            try:
                # * Kita cuma cari yang 200 OK (Beneran ada)
                res = self.session.get(target, headers=self.headers, timeout=3, allow_redirects=False)
                if res.status_code == 200:
                    found.append((p, res.status_code))
            except Exception:
                pass
        return found
