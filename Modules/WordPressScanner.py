import requests
import re
from urllib.parse import urljoin
import concurrent.futures

# * Spesialisasi pemindaian keamanan khusus WordPress
class WordPressScanner:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {'User-Agent': 'ApexOmega/3.6.0 (Zaqi Ultimate)'}
        self.commonPlugins = ["wp-forms", "elementor", "contact-form-7", "woocommerce", "jetpack"]
        self.commonThemes = ["astra", "oceanwp", "divi", "generatepress"]

    # * Deteksi versi WordPress dari meta generator atau readme
    def detectVersion(self, url):
        try:
            response = self.session.get(url, headers=self.headers, timeout=5)
            # * Cara 1: Meta Generator
            match = re.search(r'name="generator" content="WordPress ([\d.]+)"', response.text)
            if match: return match.group(1)
            
            # * Cara 2: Readme file
            readmeUrl = urljoin(url, "readme.html")
            res = self.session.get(readmeUrl, timeout=3)
            if res.status_code == 200:
                match = re.search(r'<br /> Version ([\d.]+)', res.text)
                if match: return match.group(1)
            return "Unknown"
        except Exception:
            return "Unknown"

    # * Enumerasi User via WP-JSON API (Celah umum WP)
    def enumerateUsers(self, url):
        users = []
        try:
            apiUrl = urljoin(url, "wp-json/wp/v2/users")
            res = self.session.get(apiUrl, timeout=5)
            if res.status_code == 200:
                data = res.json()
                for user in data:
                    users.append(user.get('slug', ''))
        except Exception:
            pass
        return users

    # * Cek apakah target beneran situs WordPress (Anti-False Positive)
    def isWordPress(self, url):
        signatures = ["wp-login.php", "wp-content/", "wp-includes/", "xmlrpc.php"]
        found_count = 0
        for s in signatures:
            try:
                target = urljoin(url, s)
                res = self.session.head(target, timeout=3, allow_redirects=True)
                # * Kita cari status 200/403/405 (Method Not Allowed buat xmlrpc)
                if res.status_code in [200, 403, 405]:
                    found_count += 1
            except Exception:
                pass
        # * Minimal nemu 2 signature buat konfirmasi ini WP
        return found_count >= 2

    # * Pindai plugin yang aktif pada situs target
    def scanPlugins(self, url):
        if not self.isWordPress(url):
            return []
            
        found = []
        def check(p):
            target = urljoin(url, f"wp-content/plugins/{p}/")
            try:
                # * Tambahin check detail: plugin directory biasanya 403 kalo directory listing off,
                # * tapi kita cari index.php atau readme.txt di dalemnya buat validasi 200.
                res = self.session.head(target, timeout=2)
                if res.status_code in [200, 403]:
                    # Double check file readme/license buat anti-WAF false positive
                    chk_file = urljoin(target, "readme.txt")
                    res2 = self.session.head(chk_file, timeout=2)
                    if res2.status_code == 200:
                        return p
            except Exception:
                pass
            return None

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(check, self.commonPlugins)
            found = [r for r in results if r]
        return found

    # * Cek file sensitif WordPress yang sering terekspos
    def checkVulnFiles(self, url):
        files = ["xmlrpc.php", "wp-config.php.bak", ".env", "wp-content/debug.log"]
        findings = []
        for f in files:
            target = urljoin(url, f)
            try:
                res = self.session.head(target, timeout=3)
                if res.status_code == 200:
                    findings.append(f)
            except Exception:
                pass
        return findings
