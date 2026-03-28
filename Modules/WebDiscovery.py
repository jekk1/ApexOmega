import socket
import requests
from urllib.parse import urlparse
import concurrent.futures

# * Mesin penemu aset website (Subdomains, VHosts, WebPorts)
class WebDiscovery:
    def __init__(self):
        # * Wordlist internal 100+ subdomain populer buat pemula
        self.commonSubdomains = [
            "www", "mail", "ftp", "localhost", "webmail", "smtp", "pop3", "dev", "test", "stage",
            "api", "blog", "admin", "portal", "secure", "vpn", "remote", "support", "help", "app",
            "assets", "static", "cdn", "cloud", "shop", "m", "mobile", "dev-api", "test-api", "stg",
            "v1", "v2", "beta", "alpha", "demo", "docs", "git", "svn", "jira", "wiki", "svn", "bit",
            "gitlab", "github", "jenkins", "docker", "k8s", "prod", "uat", "qa", "debug", "mysql",
            "db", "database", "redis", "elastic", "mailman", "lists", "news", "forum", "chat",
            "media", "img", "images", "js", "css", "video", "sh", "download", "files", "share",
            "backup", "old", "archive", "private", "corp", "internal", "intranet", "extranet",
            "partner", "reseller", "billing", "account", "client", "customer", "member", "staff",
            "hr", "ops", "monitoring", "status", "zabbix", "grafana", "prometheus", "nagios",
            "elk", "graylog", "splunk", "api-docs", "developer", "sandbox", "stg-api", "ws"
        ]
        
        # * Port khusus layanan web (Ops standard)
        self.webPorts = [80, 443, 8000, 8008, 8080, 8081, 8443, 8888, 9000, 9443]

    # * Brute-force subdomain (Zero-to-Hero Style)
    def bruteSubdomain(self, target):
        domain = urlparse(target).netloc if target.startswith('http') else target
        if not domain: domain = target
        
        found = []
        def check(sub):
            host = f"{sub}.{domain}"
            try:
                ip = socket.gethostbyname(host)
                return (host, ip)
            except socket.gaierror:
                return None

        # * Pake threading biar selevel Kali Linux (Brutal mode)
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            results = list(executor.map(check, self.commonSubdomains))
            found = [r for r in results if r]
        
        return found

    # * Cari Virtual Host tersembunyi lewat modifikasi Host Header
    def findVHosts(self, ip, domain):
        found = []
        try:
            for sub in self.commonSubdomains[:30]: # Limit biar gak kena rate limit parah
                vhost = f"{sub}.{domain}"
                headers = {"Host": vhost, "User-Agent": "ApexOmega/4.8"}
                response = requests.get(f"http://{ip}", headers=headers, timeout=3, allow_redirects=False)
                # * Kalo size-nya beda sama default IP, kemungkinan ada VHost
                if response.status_code == 200:
                    found.append((vhost, response.status_code))
        except Exception:
            pass
        return found

    # * Scan port layanan web yang aktif
    def scanWebPorts(self, host):
        active = []
        domain = urlparse(host).netloc if host.startswith('http') else host
        domain = domain.split(':')[0].strip('/')
        if not domain: domain = host
        
        for port in self.webPorts:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                try:
                    if s.connect_ex((domain, port)) == 0:
                        active.append(port)
                except Exception:
                    pass
        return active

    # * Cek port spesifik (v5.8.6 new alias)
    def _scan_single_port(self, host, port):
        domain = urlparse(host).netloc if host.startswith('http') else host
        domain = domain.split(':')[0].strip('/')
        if not domain: domain = host
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            try:
                return s.connect_ex((domain, port)) == 0
            except Exception:
                return False
