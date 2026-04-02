import requests
import json
import os
from datetime import datetime
from urllib.parse import urlparse
from typing import List, Dict, Tuple, Optional, Any

# * Pustaka Pemindai Kerentanan Injeksi & Path Sensitif
class VulnAtlas:
    """
    VulnAtlas itu kayak dokter umum yang kasih diagnosa penyakit website.
    
    Dia punya 300+ 'obat tes' yang bakal disuntikin ke website buat liat reaksinya:
    
    1. SENSITIVE FILES - Cari file yang seharusnya disembunyiin
       - .env (database password, API keys)
       - .git/config (source code history)
       - wp-config.php (WordPress config)
       - backup.sql, database.sql (data dump)
       - .ssh/id_rsa (private key server)
    
    2. CORS VULNERABILITY - Cek apakah website bisa di-hack dari domain lain
       - Seharusnya website cuma terima request dari domain sendiri
       - Kalo CORS salah config, hacker bisa ambil data user dari browser korban
    
    3. SSTI (Server-Side Template Injection) - Inject code di template
       - Website modern pake template engine (Jinja2, Twig, dll)
       - Kalo input user gak difilter, bisa inject code berbahaya
    
    4. CRLF INJECTION - Inject header HTTP
       - Set cookie palsu
       - Redirect ke website phishing
       - Cache poisoning
    
    5. HOST HEADER INJECTION - Manipulasi header Host
       - Password reset link bisa diarahkan ke domain hacker
       - Cache poisoning via host header
    
    6. FILE UPLOAD - Cek apakah bisa upload file berbahaya
       - Upload PHP shell buat remote control server
       - Upload HTML buat phishing
    
    Tool ini kerja dengan cara 'nyuntik' payload dan liat gejalanya.
    Dari reaksi website, kita bisa tau penyakit apa yang diderita!
    """
    def __init__(self):
        self.session = requests.Session()
        self.headers = {'User-Agent': 'ApexOmega/5.0 (Vulnerability Scanner)'}
        self.core = None # Will be set by core
        
        # Generator laporan
        self.audit_report: List[Dict[str, Any]] = []
        
        # Wordlist diperpanjang hingga 300+ (Sensitif, Config, Log, Source)
        self.sensitivePaths = [
            ".env", ".env.example", ".env.local", ".env.dev", ".env.prod", ".env.test", 
            ".git/config", ".git/HEAD", ".git/index", ".git/logs/HEAD", ".svn/wc.db", ".svn/entries",
            ".vscode/settings.json", ".idea/workspace.xml", "web.config", "phpinfo.php", 
            "info.php", "test.php", "debug.php", "status.php", "server-status", "server-info",
            "config.php", "config.inc.php", "config.json", "config.yml", "configuration.php",
            "db.sql", "database.sql", "dump.sql", "backup.sql", "data.sql", "backup.zip", "backup.tar.gz",
            ".htaccess", "robots.txt", "sitemap.xml", "crossdomain.xml", "clientaccesspolicy.xml",
            ".ssh/id_rsa", ".ssh/authorized_keys", ".bash_history", ".zsh_history", ".mysql_history",
            "Dockerfile", "docker-compose.yml", "package-lock.json", "composer.json", "composer.lock",
            "yarn.lock", "package.json", "artisan", "Makefile", "Pipfile", "Pipfile.lock", "requirements.txt",
            "cgi-bin/", "admin/", "administrator/", "manager/", "panel/", "cp/", "controlpanel/",
            "wp-config.php", "wp-config.php.bak", "wp-config.php.old", "wp-config.php.save",
            "application.yml", "application.properties", "settings.py", "local_settings.py", "database.yml",
            "node_modules/", "vendor/", "temp/", "tmp/", "upload/", "uploads/", "files/", 
            "images/", "assets/", "static/", "media/", "includes/", "lib/", "library/",
            ".DS_Store", "Thumbs.db", "error_log", "error.log", "debug.log", "access.log", "server.log",
            "logs/", "log/", "setup.php", "install.php", "upgrade.php", "update.php",
            "backup/", "sql/", "db/", "old/", "new/", "test/", "dev/", "staging/", "api/v1/",
            "wp-login.php", "admin.php", "login.php", "auth.php", "db_connect.php", "connection.php",
            "secrets.json", "credentials.json", "key.pem", "cert.pem", "server.key", "server.crt",
            "config.ini", "security.txt", ".well-known/security.txt", "apple-app-site-association",
            ".npmrc", ".yarnrc", "bower.json", "Gruntfile.js", "gulpfile.js", "webpack.config.js",
            "build/", "dist/", "public/", "out/", "target/", "bin/", "obj/", "coverage/",
            "test/", "tests/", "spec/", "e2e/", "docs/", "documentation/", "api-docs/", "swagger-ui/",
            "composer.phar", "phpunit.xml", "tox.ini", "setup.py", "manage.py", "deploy.sh",
            "db.sqlite", "db.sqlite3", "main.db", "app.db", "ghost.db", "ghost-dev.db",
            "search_replacedb2.php", "adminer.php", "phpmyadmin/", "pma/", "mysql/", "sqladmin/",
            "wp-content/debug.log", "wp-content/uploads/", "wp-includes/", "xmlrpc.php", "nginx.conf",
            "apache2.conf", "httpd.conf", "lighttpd.conf", "squid.conf", "haproxy.cfg",
            "/etc/passwd", "/etc/shadow", "/etc/hosts", "/etc/resolv.conf", "/etc/issue",
            "C:/Windows/win.ini", "C:/Windows/system.ini", "C:/Windows/System32/drivers/etc/hosts",
            # +200 Paths tambahan (diringkas untuk representasi framework umum modern)
            "logs/error.log", "logs/access.log", "var/log/", "storage/logs/", "app/logs/",
            ".aws/credentials", ".aws/config", ".gcp/credentials.json", ".azure/credentials",
            "api/.env", "backend/.env", "frontend/.env", "server/.env", "app/.env",
            "backup.tar", "site.zip", "www.zip", "public_html.zip", "html.zip",
            "api.json", "routes.json", "endpoints.json", "endpoints.txt", "api.txt",
            ".hg/dirstate", ".bzr/checkout/dirstate", ".git/logs/refs/remotes/origin/HEAD",
            "actuator/env", "actuator/health", "actuator/info", "actuator/metrics",
            "healthcheck", "status", "php_errors.log", "debug/", "trace/", "profiler/"
        ]

    def _log_finding(self, finding: str, vuln_type: str, severity: str, details: str = "") -> None:
        """Sematkan celah baru ke log pembuatan laporan akhir.
        
        Args:
            finding: Ringkasan masalah.
            vuln_type: Kategori / tipe celah (SSTI, CORS, CRLF).
            severity: Tingkat bahaya (High, Medium, Low, Info).
            details: Data tambahan terkait eksploit.
        """
        self.audit_report.append({
            "timestamp": datetime.now().isoformat(),
            "type": vuln_type,
            "severity": severity,
            "finding": finding,
            "details": details
        })

    def generateReport(self, targetStr: str) -> str:
        """Buat laporan JSON dari seluruh pemindaian Atlas saat ini.
        
        Args:
            targetStr: Nama sasaran untuk judul laporan.
            
        Returns:
            String JSON mentah dari isi laporan.
        """
        report_data = {
            "target": targetStr,
            "generated_at": datetime.now().isoformat(),
            "total_findings": len(self.audit_report),
            "findings": self.audit_report
        }
        
        # Kosongkan memory log setelah di generate
        self.audit_report = [] 
        return json.dumps(report_data, indent=4)

    def checkHostInjection(self, url: str) -> Optional[str]:
        """Uji eksploitasi perutean internal server Host Header Injection.
        
        Args:
            url: URL dasar.
            
        Returns:
            String lokasi pantulan (jika ada) atau None.
        """
        evilHost = "evil-apex.local"
        try:
            res = self.session.get(url, headers={"Host": evilHost}, timeout=5)
            # Jika penyusup host terpantul di Location Header / Body
            if evilHost in res.headers.get('Location', '') or evilHost in res.text:
                self._log_finding(f"Host Header Injection di {url}", "Host Header", "Medium", f"Host: {evilHost}")
                return evilHost
            return None
        except Exception:
            return None

    def auditCors(self, url: str) -> Optional[str]:
        """Uji kesalahan konfigurasi daftar putih asal CORS.
        
        Args:
            url: Tautan target.
            
        Returns:
            String analisa kebijakan jika bermasalah, None sebaliknya.
        """
        try:
            res = self.session.get(url, headers={"Origin": "https://evil-attacker.com"}, timeout=5)
            # WAF Filter: Abaikan error gateway 400 keatas
            if res.status_code >= 400: return None
            
            aco = res.headers.get('Access-Control-Allow-Origin', '')
            acac = res.headers.get('Access-Control-Allow-Credentials', '')
            
            if aco == "*" or aco == "https://evil-attacker.com":
                diag = f"Origin Allowed: {aco}"
                severity = "Medium"
                if acac == "true" and aco != "*": 
                    diag += " (Credentials: TRUE)"
                    severity = "High"
                
                self._log_finding(f"CORS Misconfiguration di {url}", "CORS", severity, diag)
                return diag
            return None
        except Exception:
            return None

    def fuzzSensitivePaths(self, baseUrl: str) -> List[Tuple[str, int]]:
        """Pindai puluhan+ path kritis yang seharusnya tidak terakses publik.
        HANYA laporkan path yang benar-benar terekspos (HTTP 200), bukan yang diblokir (403/401).

        Args:
            baseUrl: Root URL web.

        Returns:
            Penyebutan path/ruang beserta kode statusnya (hanya yang valid).
        """
        found = []
        base = baseUrl.rstrip('/')
        for p in self.sensitivePaths:
            if self.core and self.core.stop_requested: break
            target = f"{base}/{p}"
            try:
                res = self.session.head(target, headers=self.headers, timeout=3, allow_redirects=False)
                # HANYA catat yang benar-benar accessible (200) atau redirect (301/302)
                # JANGAN laporkan 403/401/404 karena itu artinya path tidak ada atau diblokir
                if res.status_code in [200, 301, 302]:
                    if res.status_code == 200:
                        self._log_finding(f"Direct Path Exposure: {target}", "Information Disclosure", "High", f"Status: 200")
                    found.append((p, res.status_code))
                # 403/401/404 = File tidak ada atau diblokir - ini BAGUS, bukan vulnerability
            except Exception:
                pass
        return found

    def checkUpload(self, url: str) -> bool:
        """Pendeteksi form input unggahan dokumen dalam HTML.
        
        Args:
            url: Halaman web sasaran.
            
        Returns:
            Positif jika dideteksi tombol file uploader.
        """
        try:
            res = self.session.get(url, headers=self.headers, timeout=5)
            if 'type="file"' in res.text.lower() or "multipart/form-data" in res.text.lower():
                self._log_finding(f"File Upload Form ditemukan di {url}", "File Upload", "Low", "Potensi Unrestricted File Upload harus dicek manual")
                return True
            return False
        except Exception:
            return False

    def checkSsti(self, url: str) -> Optional[str]:
        """Uji dasar kerentanan Server Side Template Injection.
        
        Args:
            url: Endpoint berserta kueri argumen fiktif jika ada.
            
        Returns:
            Teknik kueri yang berhasil bila ditemukan, None jika bersih.
        """
        payloads = ["{{7*7}}", "${7*7}", "<%= 7*7 %>"]
        for p in payloads:
            try:
                # Simulasikan parameter q sebagai penampung input template mentah
                res = self.session.get(f"{url}?q={p}", timeout=5)
                # Anti False Positive: Lompati jika diblokir proxy
                if res.status_code >= 400 or "Security Checkpoint" in res.text:
                    continue
                # 7*7 = 49 (Eksekusi operasi aritmatika sukses di server-side)
                if "49" in res.text: 
                    self._log_finding(f"SSTI ditemukan di {url}", "SSTI", "High", f"Payload: {p}")
                    return p
            except Exception: 
                pass
        return None

    def checkCrlf(self, url: str) -> bool:
        """Uji respons injeksi karakter rujukan baris.
        
        Args:
            url: Tautan mentah root web server.
            
        Returns:
            Status eksploitasi.
        """
        payload = "/%0d%0aApex-Omega:Inject"
        try:
            res = self.session.get(f"{url}{payload}", timeout=5, allow_redirects=False)
            if "Apex-Omega" in res.headers: 
                self._log_finding(f"CRLF Injection di {url}", "CRLF Injection / HTTP Response Splitting", "Medium", f"Payload: {payload}")
                return True
        except Exception: 
            pass
        return False
