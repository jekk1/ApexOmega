import socket
import requests
import json
from typing import List, Dict

# * Modul pemindaian infrastruktur jaringan
class NetworkScanner:
    """
    NetworkScanner itu kayak Google Maps buat jaringan komputer.
    
    Fungsinya:
    - Nyari tau IP address asli dari sebuah domain (misal: google.com itu IP-nya berapa)
    - Nyari subdomain tersembunyi (dev.google.com, admin.google.com, dll)
    - Ngecek DNS record buat liat email server, name server, dll
    - Mapping semua 'ruangan' di jaringan target
    
    Cara kerjanya kayak detektif yang ngumpulin info dari berbagai sumber:
    1. Sertifikat SSL - Setiap website punya sertifikat, dari situ kita bisa liat subdomain lain
    2. DNS Records - Kayak buku telepon internet, nyimpen info IP, email server, dll
    3. Port Scanning - Ngetok satu-satu pintu (port) buat liat ada yang jawab gak
    
    Hasil scan bisa kasih tau kita:
    - Berapa banyak 'pintu masuk' ke server target
    - Layanan apa aja yang jalan (web, email, database, dll)
    - Subdomain yang lupa diproteksi atau terlupakan
    """
    def __init__(self, bridge=None):
        self.bridge = bridge
        self.timeout = 2
        self.headers = {'User-Agent': 'ApexOmega/3.0.0'}

    # * Helper buat bersihin target dari protocol/path (URL -> Domain)
    def _clean_domain(self, domain: str) -> str:
        if not domain: return ""
        from urllib.parse import urlparse
        # * Contoh: https://google.com/test -> google.com
        res = urlparse(domain).netloc if "://" in domain else domain
        # * Handle cases like google.com:8080
        return res.split(":")[0].strip("/")

    # * Cari subdomain menggunakan database sertifikat (Passive)
    def findSubdomains(self, domain: str) -> List[str]:
        domain = self._clean_domain(domain)
        subdomains = set()
        try:
            url = f"https://crt.sh/?q=%25.{domain}&output=json"
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for entry in data:
                    name = entry['name_value'].lower()
                    if "\n" in name:
                        for n in name.split("\n"):
                            subdomains.add(n)
                    else:
                        subdomains.add(name)
        except Exception:
            pass
        return sorted(list(subdomains))

    # * Ambil informasi DNS record (A, MX, NS)
    def getDnsInfo(self, domain: str) -> Dict:
        results = {}
        clean_domain = self._clean_domain(domain)
        
        try:
            results['IP'] = socket.gethostbyname(clean_domain)
            # * Dapatkan hostname tambahan jika ada
            results['Aliases'] = socket.gethostbyname_ex(clean_domain)[1]
        except Exception as e:
            results['Error'] = str(e)
        return results

    # * Lakukan pencarian Whois dasar via API publik
    def whoisLookup(self, domain: str) -> Dict:
        domain = self._clean_domain(domain)
        try:
            # * Menggunakan API rdap (standard modern whois)
            url = f"https://rdap.org/domain/{domain}"
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception:
            pass
        return {"error": "Data Whois tidak ditemukan"}

    # * Scan port menggunakan bridge atau native socket
    def scanPort(self, target: str, port: int) -> bool:
        if self.bridge:
            return self.bridge.scanPort(target, port)
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                return s.connect_ex((target, port)) == 0
        except Exception:
            return False

    # * Deteksi potensi Subdomain Takeover (Cek CNAME pointing)
    def checkSubdomainTakeover(self, subdomain: str) -> Dict:
        services = {
            "github.io": "GitHub Pages",
            "heroku.com": "Heroku App",
            "cloudfront.net": "Amazon CloudFront",
            "s3.amazonaws.com": "Amazon S3 Bucket",
            "azurewebsites.net": "Azure Website"
        }
        try:
            # * Dapatkan CNAME target
            # * Note: Tanpa library dns, kita simulasi deteksi via hostname
            import subprocess
            cmd = f"nslookup -type=CNAME {subdomain}"
            output = subprocess.check_output(cmd, shell=True).decode()
            for pattern, name in services.items():
                if pattern in output.lower():
                    return {"vulnerable": True, "service": name, "cname": pattern}
        except Exception:
            pass
        return {"vulnerable": False}

    # * Ambil semua Record DNS (A, AAAA, MX, TXT)
    def getAllDnsRecords(self, domain: str) -> Dict:
        domain = self._clean_domain(domain)
        records = {}
        types = ["A", "AAAA", "MX", "TXT", "NS"]
        import subprocess
        for t in types:
            try:
                cmd = f"nslookup -type={t} {domain}"
                output = subprocess.check_output(cmd, shell=True).decode()
                records[t] = output.split("Non-authoritative answer:")[-1].strip()
            except Exception:
                records[t] = "Not found"
        return records
