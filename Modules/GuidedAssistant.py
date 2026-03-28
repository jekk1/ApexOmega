# * Pustaka Tool Pentester (v4.5 Shell Edition)
class GuidedAssistant:
    def __init__(self):
        # * Database Bantuan & Cara Pakai (Interactive Syntax)
        self.helpDatabase = {
            # -- Network Tools --
            "nmap": "Network Mapper: Tool untuk pengintai network, scan port, dan deteksi OS. CARA PAKAI: Ketik !nmap setelah input target di shell.",
            "netdiscover": "Alat pengintai jaringan ARP (Layer 2) untuk menemukan host di LAN.",
            "wireshark": "Penganalisis protokol jaringan (packet sniffer) paling populer di dunia.",
            "recon": "Reconnaissance: Tahap awal pengumpulan informasi target. CARA PAKAI: Ketik !recon di shell.",
            
            # -- Web Audit Tools (WEB-NITRO) --
            "webaudit": "Nitro Web Audit v4.8: Pemindaian brutal SQLi, XSS, WAF detection, & JS scraper. CARA PAKAI: Ketik !webaudit.",
            "subdomain": "Subdomain Bruter: Mencari subdomain aktif dari domain target secara massal. CARA PAKAI: Ketik !subdomain.",
            "sub": "Alias untuk subdomain discovery engine.",
            "vhost": "Virtual Host Finder: Mencari konfigurasi vhost tersembunyi lewat modifikasi host header. CARA PAKAI: Ketik !vhost.",
            "webports": "Web Port Scanner: Scan port khusus layanan web (80, 443, 8080, dll). CARA PAKAI: Ketik !webports.",
            "vuln": "Vuln Atlas v4.9: Audit kerentanan tingkat lanjut (CORS, SSRF, Host Header Injection, & 50+ Sensitive Paths). CARA PAKAI: Ketik !vuln.",
            "api": "API Auditor: Mencari endpoint API tersembunyi dan melakukan pengetesan HTTP methods (IDOR check). CARA PAKAI: Ketik !api.",
            "cloud": "Cloud Hunter: Mencari public storage (S3 Buckets, Firebase, GCP) yang terekspos berdasarkan nama domain. CARA PAKAI: Ketik !cloud.",
            "wordpress": "Spesialis audit situs berbasis WordPress. CARA PAKAI: Ketik !wordpress.",
            "wp": "Alias untuk wordpress scanner modul.",
            "sqlmap": "Otomatisasi deteksi dan eksploitasi celah SQL Injection di database.",
            
            # -- Exploitation & Chaos --
            "chaos": "Nitro Chaos Engine: Alat stress testing untuk menguji keandalan server. CARA PAKAI: Ketik !chaos.",
            "nitro": "Alias untuk Chaos Engine (Destroyer Profile).",
            "metasploit": "Framework eksploitasi paling lengkap untuk pengujian penetrasi sistem.",
            
            "payload": "Payload Generator: Tool untuk membuat encoding (Base64, Hex, URL) buat bypass filter dasar. CARA PAKAI: Ketik !payload.",
            
            # -- System Commands --
            "exit": "Keluar dari modul aktif atau aplikasi. CARA PAKAI: Ketik !exit.",
            "clear": "Membersihkan layar terminal console.",
            "help": "Membuka panduan penggunaan alat di tab How to Use. CARA PAKAI: Ketik !help."
        }
        
        # * Roadmap Sejarah Sistem
        self.roadmap = [
            "v1.0-v3.x: Desktop UI Dasar.",
            "v4.0: Console Edition.",
            "v4.5: Interactive Shell Edition (Mode !tool & !exit).",
            "v4.7: Zero-to-Hero Edition (Beginner Roadmap & Color Aesthetics).",
            "v4.8: Web-Nitro Edition (Advanced Web Discovery & Pentesting Powerhouse).",
            "v4.9: Web-Nitro Ultra Edition (Vuln Atlas, API Auditor, Cloud Hunter, & Sidebar UI Categories)."
        ]

    def getSteps(self):
        return []

    def getRoadmap(self):
        return self.roadmap

    def searchHelp(self, query):
        query = query.lower()
        results = {}
        for k, v in self.helpDatabase.items():
            if query in k or query in v.lower():
                results[k] = v
        return results
