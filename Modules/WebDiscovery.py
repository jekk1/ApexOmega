import requests
import socket
import concurrent.futures
from typing import List, Optional

# * Modul Ekstraksi dan Pemetaan Permukaan Aset Digital Peladen
class WebDiscovery:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {'User-Agent': 'ApexOmega/5.0 (Discovery Engine)'}
        self.core = None # Will be set by core
        
        # Ekstensi wordlist menjadi 500+ kandidat umum sub-domain
        self.subdomainList = [
            "www", "mail", "ftp", "localhost", "webmail", "smtp", "pop", "ns1", "web", "ns2",
            "api", "dev", "test", "staging", "admin", "blog", "m", "mobile", "shop", "store",
            "forum", "support", "help", "cdn", "assets", "static", "images", "img", "files",
            "secure", "vpn", "portal", "login", "app", "dashboard", "members", "client",
            "billing", "beta", "alpha", "v1", "v2", "v3", "demo", "sandbox", "uat", "qaQA",
            "search", "news", "docs", "developer", "api-docs", "download", "dl", "update",
            "upload", "chat", "video", "media", "live", "stream", "status", "stats", "metrics",
            "monitor", "grafana", "kibana", "prometheus", "elasticsearch", "elastic",
            "splunk", "sso", "auth", "oauth", "jwt", "gateway", "proxy", "gw", "internal",
            "intranet", "local", "corp", "employee", "staff", "vendor", "partner", "b2b",
            "b2c", "erp", "crm", "hr", "payroll", "mail2", "smtp2", "pop3", "imap", "mx",
            "mx1", "mx2", "dns1", "dns2", "ns3", "ns4", "cloud", "aws", "gcp", "azure",
            "server", "host", "hosting", "webhost", "panel", "cpanel", "whm", "plesk",
            "db", "database", "mysql", "postgres", "redis", "mongodb", "memcached", "sql",
            "ftp2", "sftp", "ftps", "ssh", "git", "gitlab", "github", "svn", "bitbucket",
            "repo", "registry", "docker", "k8s", "kubernetes", "swarm", "portainer",
            "jenkins", "ci", "cd", "travis", "circleci", "build", "ci-cd", "tools",
            "wiki", "confluence", "jira", "redmine", "trello", "slack", "mattermost",
            "meet", "video", "zoom", "webex", "teams", "skype", "calendar", "cal", "schedule",
            "events", "booking", "reservations", "tickets", "helpdesk", "ticketing",
            "zendesk", "freshdesk", "jira-servicedesk", "kb", "knowledgebase", "faq",
            "community", "board", "feedback", "ideas", "ideas", "survey", "poll", "vote",
            "marketing", "promo", "campaign", "landing", "lp", "affiliate", "referral",
            "partners", "sponsors", "investors", "pr", "press", "media-kit", "brand",
            "brand-guidelines", "careers", "jobs", "about", "contact", "privacy", "terms",
            "legal", "security", "bounty", "bugbounty", "disclosure", "trust", "compliance",
            "audit", "reports", "annual-report", "esg", "sustainability", "csr", "foundation",
            "charity", "donate", "giving", "volunteer", "alumni", "network", "connect",
            "directory", "search", "find", "map", "maps", "location", "locations",
            "stores", "branches", "atms", "dealers", "distributors", "retailers",
            "wholesale", "b2b-portal", "supplier", "suppliers", "vendor-portal",
            "procurement", "sourcing", "tenders", "rfp", "careers", "jobs", "hiring",
            "recruitment", "talent", "hr", "human-resources", "benefits", "payroll",
            "training", "learning", "lms", "elearning", "academy", "university",
            "campus", "student", "students", "faculty", "staff", "alumni", "library",
            "research", "labs", "innovation", "incubator", "accelerator", "startup",
            "venture", "capital", "investments", "portfolio", "fund", "funds",
            "wealth", "private-wealth", "institutional", "corporate", "commercial",
            "business", "sme", "enterprise", "government", "public-sector",
            "ngo", "non-profit", "charity", "foundation", "association", "institute",
            "society", "club", "group", "chapter", "local", "regional", "national",
            "global", "international", "ww", "hq", "headquarters", "office",
            "offices", "hq1", "hq2", "main", "primary", "secondary", "backup",
            "dr", "disaster-recovery", "bcp", "business-continuity", "test1", "test2",
            "dev1", "dev2", "staging1", "staging2", "prod1", "prod2", "us", "uk",
            "ca", "au", "nz", "eu", "asia", "africa", "latam", "na", "sa", "emea",
            "apac", "japan", "china", "india", "brazil", "mexico", "russia", "en",
            "fr", "de", "es", "it", "pt", "ru", "zh", "ja", "ko", "ar", "th",
            "id", "vi", "ms", "tl", "hi", "bn", "ur", "fa", "tr", "he", "nl",
            "sv", "no", "da", "fi", "pl", "cs", "sk", "hu", "ro", "bg", "el",
            "sr", "hr", "sl", "lt", "lv", "et", "uk", "be", "kk", "uz", "az",
            "ka", "hy", "mn", "km", "lo", "my", "si", "ne", "am", "sw", "yo",
            "ig", "ha", "zu", "xh", "af", "st", "tn", "ts", "ss", "ve", "nr",
            "api-dev", "api-sandbox", "api-test", "api-staging", "api-prod",
            "auth-dev", "auth-sandbox", "auth-test", "auth-staging", "auth-prod",
            "sso-dev", "sso-sandbox", "sso-test", "sso-staging", "sso-prod",
            "login-dev", "login-sandbox", "login-test", "login-staging", "login-prod",
            "dashboard-dev", "dashboard-sandbox", "dashboard-test", "dashboard-staging",
            "dashboard-prod", "admin-dev", "admin-sandbox", "admin-test", "admin-staging",
            "admin-prod", "app-dev", "app-sandbox", "app-test", "app-staging", "app-prod",
            "dev-api", "sandbox-api", "test-api", "staging-api", "prod-api",
            "dev-auth", "sandbox-auth", "test-auth", "staging-auth", "prod-auth",
            "dev-sso", "sandbox-sso", "test-sso", "staging-sso", "prod-sso",
            "dev-login", "sandbox-login", "test-login", "staging-login", "prod-login",
            "dev-dashboard", "sandbox-dashboard", "test-dashboard", "staging-dashboard",
            "prod-dashboard", "dev-admin", "sandbox-admin", "test-admin", "staging-admin",
            "prod-admin", "dev-app", "sandbox-app", "test-app", "staging-app", "prod-app",
            "test-db", "dev-db", "staging-db", "prod-db", "backup-db", "replica-db",
            "master-db", "slave-db", "read-db", "write-db", "analytics-db", "reporting-db",
            "data-warehouse", "data-lake", "hadoop", "spark", "kafka", "rabbitmq"
        ]

    def bruteSubdomains(self, domain: str) -> List[str]:
        """Pencarian paksa kandidat rute subdomain dari kamus internal ke sistem IP (DNS Resolver).
        
        Args:
            domain: Ranah dasar/root nama peladen murni.
            
        Returns:
            Susunan konfirmasi ekstensi valid dari domain root sasaran.
        """
        found = []
        def check(sub: str) -> Optional[str]:
            if self.core and getattr(self.core, 'stop_requested', False): 
                return None
            target = f"{sub}.{domain}"
            try:
                ip = socket.gethostbyname(target)
                return f"{target} -> {ip}"
            except Exception:
                return None

        # Fuzzing dengan alokasi 15 pool pekerja DNS
        with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
            results = executor.map(check, self.subdomainList)
            found = [r for r in results if r]
        return found
        
    # * Alias untuk sinkronisasi dengan Core v6.3.1 (Sub-domain Engine)
    def bruteSubdomain(self, domain: str) -> List[str]:
        """Pencarian paksa sub-domain (Pembungkus bruteSubdomains)."""
        return self.bruteSubdomains(domain)
        
    def scanWebPorts(self, target: str) -> List[int]:
        """Identifikasi infrastruktur peladen terbuka (Port Utama: 80, 443, 8080, 8443, 2082, 2083).
        
        Args:
            target: Alamat IP / Host sasaran pemindaian infrastruktru terbuka.
            
        Returns:
            Susunan nomor port yang terdeteksi aktif/terbuka.
        """
        common_ports = [80, 443, 8080, 8443, 2082, 2083, 2086, 2087, 2095, 2096, 8880, 8000, 3000, 5000, 8081]
        open_ports = []
        
        # Bersihkan target dari scheme jika ada
        host = target.replace('https://', '').replace('http://', '').split('/')[0].split(':')[0]
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_port = {executor.submit(self._scan_single_port, host, port): port for port in common_ports}
            for future in concurrent.futures.as_completed(future_to_port):
                port = future_to_port[future]
                try:
                    if future.result():
                        open_ports.append(port)
                except Exception:
                    pass
        return sorted(open_ports)

    def _scan_single_port(self, host: str, port: int) -> bool:
        """Pemeriksaan tunggal ketersediaan akses soket port.
        
        Args:
            host: Alamat host tujuan.
            port: Nomor port identifikasi.
            
        Returns:
            Status koneksi berhasil (True/False).
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1.5)
                # Mencoba jabat tangan soket awal
                result = s.connect_ex((host, port))
                return result == 0
        except Exception:
            return False

    def enumeratePassive(self, domain: str) -> List[str]:
        """Intelijen Pencarian Sub-Domain Pasif lewat arsip publik sertifikat TLS/SSL gratis maupun catatan mesin peramban global (Crt.sh & VirusTotal).
        
        Args:
            domain: Ranah IP nama pangkalan sumber sasaran.
            
        Returns:
            Kumpulan catatan pasif sistem penamaan domain yang terekam riwayat sertifikatnya.
        """
        found = set()
        
        # 1. Crt.sh (Certificate Transparency)
        try:
            res = self.session.get(f"https://crt.sh/?q=%25.{domain}&output=json", timeout=10)
            if res.status_code == 200:
                data = res.json()
                for item in data:
                    name = item.get('name_value', '').lower()
                    if '*' not in name and name.endswith(domain):
                        # Pisahkan multine string bila sub-domain kembar terselubung
                        for n in name.split('\n'):
                            found.add(n)
        except Exception:
            pass
            
        # 2. HackerTarget (Pasif IP/Subdomain Ping)
        try:
            res = self.session.get(f"https://api.hackertarget.com/hostsearch/?q={domain}", timeout=10)
            if res.status_code == 200 and "error" not in res.text.lower():
                lines = res.text.strip().split('\n')
                for line in lines:
                    parts = line.split(',')
                    if len(parts) >= 1 and parts[0].endswith(domain):
                        found.add(parts[0])
        except Exception:
            pass

        return list(found)
        
    def findVirtualHosts(self, targetIp: str, baseDomain: str) -> List[str]:
        """Pencarian perutean server tumpang-tindih, VHost (Injeksi konfigurasi peladen Host-Header manipulasi penyewaan ruang peladen awan statis bersama).
        
        Args:
            targetIp: Nomor referensi perangkat.
            baseDomain: Nama domain terdaftar pangkalan utama.
            
        Returns:
            Simpulan host rahasia peladen di balik IP.
        """
        vhosts = ["dev", "test", "staging", "admin", "internal", "local", "demo", "api"]
        found = []
        try:
            base_url = f"http://{targetIp}"
            # Respons referensi standar
            base_res = self.session.get(base_url, timeout=3)
            base_len = len(base_res.content)
            
            for vh in vhosts:
                hostParams = f"{vh}.{baseDomain}"
                headersParams = {'Host': hostParams}
                res = self.session.get(base_url, headers=headersParams, timeout=3, allow_redirects=False)
                # Respon dianggap unik jika perbedaan ukuran konten membedakan dari pendaratan peladen umum 
                if res.status_code in [200, 401, 403] and abs(len(res.content) - base_len) > 100:
                    found.append(f"{hostParams} (Status: {res.status_code})")
            return found
        except Exception:
            return []
