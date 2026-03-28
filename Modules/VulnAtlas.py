import requests
from urllib.parse import urlparse

# * Atlas Kerentanan Web (CORS, SSRF, Host Injection, Sensitive Paths)
class VulnAtlas:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {'User-Agent': 'ApexOmega/4.9 (X11; Linux x86_64)'}
        
        # * Daftar 100+ path sensitif v5.4 (Industrial Grade Pentest Wordlist)
        self.sensitivePaths = [
            ".env", ".git/config", ".vscode/settings.json", "web.config", "phpinfo.php",
            "config.php", "db.sql", "backup.zip", ".htaccess", "robots.txt", ".ssh/id_rsa",
            "server-status", "server-info", "Dockerfile", "docker-compose.yml", "package-lock.json",
            "composer.json", "artisan", "cgi-bin/", "admin/", "administrator/", "wp-config.php",
            "wp-config.php.bak", "wp-config.php.old", "config.yml", "application.yml", "settings.py",
            "local_settings.py", "database.yml", "node_modules/", "vendor/", "sql.zip", "data.sql",
            "temp/", "tmp/", "upload/", "uploads/", "files/", "images/", "assets/", "static/",
            "media/", ".DS_Store", "Thumbs.db", ".bash_history", ".mysql_history", "error_log",
            "logs/", "test.php", "info.php", "dev.php", "setup.php", "install.php",
            "backup/", "sql/", "db/", "old/", "new/", "test/", "dev/", "staging/", "api/v1/",
            ".env.example", ".env.local", ".env.dev", ".env.prod", "config.json", "settings.json",
            "wp-login.php", "admin.php", "login.php", "auth.php", "db_connect.php", "connection.php",
            "secrets.json", "credentials.json", "key.pem", "cert.pem", "id_rsa", "config.ini",
            "sitemap.xml", "crossdomain.xml", "clientaccesspolicy.xml", "security.txt",
            ".well-known/", "server.key", "server.crt", ".npmrc", ".yarnrc", "yarn.lock",
            "package.json", "bower.json", "Gruntfile.js", "gulpfile.js", "webpack.config.js"
        ]
        self.core = None # Will be set by core

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
            # * Ignore Vercel WAF/403 challenges
            if res.status_code >= 400: return None
            
            aco = res.headers.get('Access-Control-Allow-Origin', '')
            acac = res.headers.get('Access-Control-Allow-Credentials', '')
            
            if aco == "*" or aco == "https://evil-attacker.com":
                diag = f"Origin Allowed: {aco}"
                if acac == "true": diag += " (Credentials: TRUE - HIGH RISK)"
                return diag
            return None
        except Exception:
            return None

    # * Cek apakah path tertentu ada (v5.4 Helper)
    def checkPath(self, url):
        try:
            res = self.session.head(url, headers=self.headers, timeout=3, allow_redirects=False)
            return res.status_code if res.status_code in [200, 301, 302, 403] else None
        except: return None

    # * Fuzzing 100+ path sensitif secara otomatis v5.4
    def fuzzSensitivePaths(self, baseUrl):
        found = []
        base = baseUrl.rstrip('/')
        for p in self.sensitivePaths:
            if self.core and self.core.stop_requested: break
            target = f"{base}/{p}"
            try:
                res = self.session.head(target, headers=self.headers, timeout=3, allow_redirects=False)
                if res.status_code == 200:
                    found.append((p, res.status_code))
            except Exception: pass
        return found

    # * Cek apakah ada form upload di page v5.4
    def checkUpload(self, url):
        try:
            res = self.session.get(url, headers=self.headers, timeout=5)
            if 'type="file"' in res.text or "multipart/form-data" in res.text:
                return True
            return False
        except Exception: return False

    # * Cek potensi Server-Side Template Injection (SSTI) v5.4
    def checkSsti(self, url):
        payloads = ["{{7*7}}", "${7*7}", "<%= 7*7 %>"]
        for p in payloads:
            try:
                res = self.session.get(f"{url}?q={p}", timeout=5)
                # * Anti False Positive: Abaikan WAF/Vercel Cloudflare pages
                if res.status_code >= 400 or "Vercel Security Checkpoint" in res.text:
                    continue
                if "49" in res.text: return p
            except: pass
        return None

    # * Cek potensi CRLF Injection (HTTP Response Splitting) v5.4
    def checkCrlf(self, url):
        payload = "/%0d%0aApex-Omega:Inject"
        try:
            res = self.session.get(f"{url}{payload}", timeout=5, allow_redirects=False)
            if "Apex-Omega" in res.headers: return True
        except: pass
        return False
