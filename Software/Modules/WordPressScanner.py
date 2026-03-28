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

    # * Pindai plugin yang aktif pada situs target
    def scanPlugins(self, url):
        found = []
        def check(p):
            target = urljoin(url, f"wp-content/plugins/{p}/")
            try:
                res = self.session.head(target, timeout=2)
                if res.status_code in [200, 403]:
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
