import requests
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import concurrent.futures

# * Mesin pemindai kerentanan aplikasi web
class WebScanner:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {'User-Agent': 'ApexOmega/4.8 (X11; Linux x86_64)'} # Kali Linux Style UA
        self.discovered = set()
        self.waf_signatures = {
            "Cloudflare": ["cf-ray", "__cfduid", "cloudflare"],
            "Akamai": ["akamai-ghost", "akamai-edge"],
            "Imperva": ["incap_ses", "visid_incap"],
            "ModSecurity": ["mod_security", "noisiest"],
            "Nginx Generic": ["nginx"]
        }

    # * Jelajahi endpoint yang tersedia pada domain target
    def crawlEndpoint(self, baseUrl, maxDepth=3, currentDepth=0):
        if currentDepth >= maxDepth or baseUrl in self.discovered:
            return
        
        try:
            response = self.session.get(baseUrl, headers=self.headers, timeout=5)
            self.discovered.add(baseUrl)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                fullUrl = urljoin(baseUrl, link['href'])
                if urlparse(fullUrl).netloc == urlparse(baseUrl).netloc:
                    self.crawlEndpoint(fullUrl, maxDepth, currentDepth + 1)
        except Exception:
            pass

    # * Lakukan brute force direktori menggunakan wordlist internal v5.3
    def bruteDir(self, baseUrl, customList=None):
        commonDirs = ["admin", "login", "config", "api", "v1", "v2", "backup", ".env", "phpinfo.php", ".git", "wp-admin", "administrator", "dev", "test", "private", "shell.php", "cmd.php"]
        if customList: commonDirs += customList
        
        found = []
        for d in commonDirs:
            target = urljoin(baseUrl, d)
            try:
                # * Kita pake HEAD biar kenceng (v5.3 Optimize)
                response = self.session.head(target, headers=self.headers, timeout=3, allow_redirects=False)
                if response.status_code in [200, 301, 302, 403]:
                    found.append((d, response.status_code))
            except Exception:
                pass
        return found

    # * Audit HTTP Security Headers (v5.3 New)
    def auditSecurityHeaders(self, url):
        required = ["Content-Security-Policy", "X-Frame-Options", "X-Content-Type-Options", "Strict-Transport-Security", "Referrer-Policy"]
        findings = []
        try:
            response = self.session.get(url, headers=self.headers, timeout=5)
            headers = response.headers
            for h in required:
                if h not in headers:
                    findings.append(f"MISSING: {h}")
                else:
                    findings.append(f"PRESENT: {h} ({headers[h][:30]}...)")
            return findings
        except Exception:
            return ["Error fetching headers."]

    # * Audit Form Parameters (v5.3 New)
    def auditForms(self, url):
        findings = []
        try:
            response = self.session.get(url, headers=self.headers, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            forms = soup.find_all('form')
            for i, f in enumerate(forms):
                method = f.get('method', 'GET').upper()
                action = f.get('action', '')
                inputs = [inp.get('name') for inp in f.find_all(['input', 'textarea']) if inp.get('name')]
                findings.append({
                    "id": i+1,
                    "method": method,
                    "action": action,
                    "inputs": inputs
                })
            return findings
        except Exception:
            return []

    # * Cek apakah folder .git terbuka ke publik (v5.3 New)
    def checkGitExposed(self, baseUrl):
        critical_files = [".git/config", ".git/HEAD", ".git/index"]
        leaks = []
        for f in critical_files:
            target = urljoin(baseUrl, f)
            try:
                res = self.session.get(target, headers=self.headers, timeout=4)
                if res.status_code == 200 and ("[core]" in res.text or "ref: refs/" in res.text or len(res.content) > 10):
                    leaks.append(f)
            except Exception:
                pass
        return leaks

    # * Deteksi teknologi detail (JS Frameworks, Analytics, WAF)
    def detectTech(self, url):
        tech_stack = {"framework": [], "cms": [], "analytics": [], "server": [], "waf": []}
        try:
            response = self.session.get(url, headers=self.headers, timeout=5)
            html = response.text.lower()
            headers = response.headers
            
            # -- WAF Detection --
            for waf, sigs in self.waf_signatures.items():
                for sig in sigs:
                    if sig in str(headers).lower() or sig in html:
                        if waf not in tech_stack["waf"]: tech_stack["waf"].append(waf)
            
            # -- Server --
            if 'Server' in headers: tech_stack["server"].append(headers['Server'])
            
            # -- Frameworks --
            if "react" in html: tech_stack["framework"].append("React.js")
            if "vue" in html: tech_stack["framework"].append("Vue.js")
            if "angular" in html: tech_stack["framework"].append("Angular")
            
            # -- Deep CMS Detection --
            if "wp-content" in html or "wordpress" in html: tech_stack["cms"].append("WordPress")
            if "laravel" in html: tech_stack["cms"].append("Laravel")
            if "joomla" in html or "option=com_" in html: tech_stack["cms"].append("Joomla")
            if "drupal" in html or "sites/all" in html: tech_stack["cms"].append("Drupal")
            if "magento" in html or "mage-cache" in html: tech_stack["cms"].append("Magento")
            if "prestashop" in html: tech_stack["cms"].append("PrestaShop")
            if "shopify" in html or "cdn.shopify.com" in html: tech_stack["cms"].append("Shopify")
            
            # -- Analytics ID --
            ua_match = re.search(r"ua-\d+-\d+", html)
            if ua_match: tech_stack["analytics"].append(f"Google Analytics ({ua_match.group(0).upper()})")
            
            return tech_stack
        except Exception:
            return tech_stack

    # * SQL Injection Brutal Mode (Threaded)
    def runBrutalSqlScan(self, url):
        payloads = self.getPayloadList("sqli") + ["' OR SLEEP(5)--", "' AND 1=1--", "admin'--"]
        found = []
        def check(p):
            try:
                testUrl = f"{url}?id={p}"
                res = self.session.get(testUrl, timeout=7)
                if "sql syntax" in res.text.lower() or "mysql" in res.text.lower():
                    return (p, "Error-based")
                return None
            except Exception:
                pass
            return None

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(check, payloads)
            found = [r for r in results if r]
        return found

    # * XSS Brutal Mode (Threaded with Reflection Check)
    def runBrutalXssScan(self, url):
        payloads = self.getPayloadList("xss") + ["<svg/onload=alert(1)>", "\"><script>alert(1)</script>"]
        found = []
        def check(p):
            try:
                testUrl = f"{url}?q={p}"
                res = self.session.get(testUrl, timeout=5)
                # * Kita cek apakah payload terpantul (reflected) dan tidak ter-escape
                if p in res.text and "&lt;script&gt;" not in res.text:
                    return (p, "Reflected")
                return None
            except Exception:
                pass
            return None

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(check, payloads)
            found = [r for r in results if r]
        return found

    # * Cari halaman login admin dengan pola umum
    def findAdminPanel(self, baseUrl):
        adminPaths = ["/wp-admin", "/admin", "/administrator", "/login", "/wp-login.php", "/user/login", "/cp", "/panel"]
        found = []
        for path in adminPaths:
            target = urljoin(baseUrl, path)
            try:
                # * Kita cari yang beneran ada form login (200 OK)
                response = self.session.get(target, headers=self.headers, timeout=3)
                if response.status_code == 200:
                    found.append(target)
            except Exception:
                pass
        return found

    # * Cek kerentanan Clickjacking (X-Frame-Options)
    def checkClickjacking(self, baseUrl):
        try:
            response = self.session.get(baseUrl, headers=self.headers, timeout=5)
            xfo = response.headers.get('X-Frame-Options', '').upper()
            csp = response.headers.get('Content-Security-Policy', '').lower()
            
            if 'DENY' in xfo or 'SAMEORIGIN' in xfo or 'frame-ancestors' in csp:
                return False # Aman
            return True # VULNERABLE
        except Exception:
            return False

    # * Audit keamanan cookie (Flags: HttpOnly, Secure)
    def auditCookies(self, baseUrl):
        try:
            response = self.session.get(baseUrl, headers=self.headers, timeout=5)
            cookies = response.cookies
            results = []
            for cookie in cookies:
                results.append({
                    "name": cookie.name,
                    "httpOnly": cookie.has_nonstandard_attr('httponly') or 'httponly' in str(cookie).lower(),
                    "secure": cookie.secure
                })
            return results
        except Exception:
            return []

    # * Deteksi celah Local File Inclusion (LFI) pada parameter
    def detectLfi(self, url, payload="../../../etc/passwd"):
        # * Untuk windows, kita pake win.ini sebagai payload alternatif
        targets = [payload, "../../../../../../../../windows/win.ini"]
        try:
            for p in targets:
                testUrl = f"{url}?file={p}"
                response = self.session.get(testUrl, headers=self.headers, timeout=5)
                if "root:x:0:0:" in response.text or "[extensions]" in response.text:
                    return True, p
            return False, ""
        except Exception:
            return False, ""

    # * Cek apakah redirect pada URL bisa dieksploitasi (Open Redirect)
    def checkOpenRedirect(self, url):
        payload = "https://evil.local"
        testParams = ["url", "redirect", "next", "redir", "dest"]
        try:
            for param in testParams:
                testUrl = f"{url}?{param}={payload}"
                # * Kita gak izinkan internal redirect biar keliatan kalo keluar
                response = self.session.get(testUrl, headers=self.headers, timeout=5, allow_redirects=False)
                if response.status_code in [301, 302, 307]:
                    location = response.headers.get('Location', '')
                    if location.startswith(payload):
                        return True, param
            return False, ""
        except Exception:
            return False, ""

    # * Cari parameter tersembunyi pada URL (Parameter Miner)
    def mineParameters(self, url):
        commonParams = ["debug", "admin", "test", "dev", "config", "cmd", "exec", "source", "view", "edit", "root"]
        found = []
        try:
            for p in commonParams:
                testUrl = f"{url}?{p}=1"
                response = self.session.get(testUrl, headers=self.headers, timeout=3)
                # * Kalo response berubah (size/content) kemungkinan parameter valid
                if response.status_code == 200:
                    found.append(p)
            return found
        except Exception:
            return []

    # * Perluasan pencarian file sensitif (Extended Miner)
    def mineSensitiveFiles(self, baseUrl):
        criticalFiles = [
            ".env", ".git/config", "web.config", "phpinfo.php", "config.php",
            "db.sql", "backup.zip", ".htaccess", "robots.txt", ".ssh/id_rsa",
            "server-status", "server-info", "Dockerfile", "docker-compose.yml"
        ]
        found = []
        for f in criticalFiles:
            target = urljoin(baseUrl, f)
            try:
                response = self.session.get(target, headers=self.headers, timeout=3)
                if response.status_code == 200:
                    found.append((f, len(response.content)))
            except Exception:
                pass
        return found

    # * Audit Header Keamanan Lanjutan (CSP, HSTS, Referrer)
    def auditSecurityHeaders(self, baseUrl):
        try:
            response = self.session.get(baseUrl, headers=self.headers, timeout=5)
            headers = response.headers
            audit = {
                "HSTS": headers.get("Strict-Transport-Security", "MISSING"),
                "CSP": headers.get("Content-Security-Policy", "MISSING"),
                "Referrer-Policy": headers.get("Referrer-Policy", "MISSING"),
                "Permissions-Policy": headers.get("Permissions-Policy", "MISSING")
            }
            return audit
        except Exception:
            return {}

    # * EKSTRA PENTESTING WEB: Scrape JS Endpoint & Secrets
    def scrapeJsInfo(self, baseUrl, html_content):
        # * Cari semua file .js di HTML
        js_files = re.findall(r'src=["\']([^"\']+\.js)', html_content)
        endpoints = set()
        secrets = []
        
        for js in js_files[:5]: # Batasi 5 file biar gak hang
            js_url = urljoin(baseUrl, js)
            try:
                res = self.session.get(js_url, timeout=3)
                # * Cari URL (Endpoint)
                found_urls = re.findall(r'https?://[a-zA-Z0-9./?=_-]+', res.text)
                endpoints.update(found_urls)
                # * Cari API Keys (Simple Regex)
                if "key" in res.text.lower() or "secret" in res.text.lower():
                    matches = re.findall(r'[a-zA-Z0-9]{32,}', res.text)
                    if matches: secrets.extend(matches)
            except Exception:
                pass
        return list(endpoints)[:10], secrets[:3]

    # * ANALISA FILE SENSITIF WEB: Robots & Sitemap
    def analyzeWebConfig(self, baseUrl):
        configs = {"robots": [], "sitemap": []}
        try:
            # -- Robots.txt --
            r_res = self.session.get(urljoin(baseUrl, "/robots.txt"), timeout=3)
            if r_res.status_code == 200:
                disallow = re.findall(r'Disallow: (.+)', r_res.text)
                configs["robots"].extend(disallow)
            
            # -- Sitemap.xml --
            s_res = self.session.get(urljoin(baseUrl, "/sitemap.xml"), timeout=3)
            if s_res.status_code == 200:
                locs = re.findall(r'<loc>(.+)</loc>', s_res.text)
                configs["sitemap"].extend(locs[:5])
        except Exception:
            pass
        return configs

    # * Generator Payload XSS/SQLi Dasar buat Pemula
    def getPayloadList(self, vulnType="xss"):
        payloads = {
            "xss": [
                "<script>alert(1)</script>",
                "'\"><script>alert(1)</script>",
                "<img src=x onerror=alert(1)>",
                "javascript:alert(1)"
            ],
            "sqli": [
                "' OR 1=1--",
                "\" OR 1=1--",
                "admin' --",
                "' UNION SELECT 1,2,3--"
            ]
        }
        return payloads.get(vulnType, [])
