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
            
            # -- Web Audit Tools --
            "webaudit": "Mesin audit web internal Apex (Zaqi Brutal Engine). CARA PAKAI: Ketik !webaudit.",
            "wordpress": "Spesialis audit situs berbasis WordPress. CARA PAKAI: Ketik !wordpress.",
            "wp": "Alias untuk wordpress scanner modul.",
            "sqlmap": "Otomatisasi deteksi dan eksploitasi celah SQL Injection di database.",
            
            # -- Exploitation & Chaos --
            "chaos": "Nitro Chaos Engine: Alat stress testing untuk menguji keandalan server. CARA PAKAI: Ketik !chaos.",
            "nitro": "Alias untuk Chaos Engine (Destroyer Profile).",
            "metasploit": "Framework eksploitasi paling lengkap untuk pengujian penetrasi sistem.",
            
            # -- System Commands --
            "exit": "Keluar dari modul aktif atau aplikasi. CARA PAKAI: Ketik !exit.",
            "clear": "Membersihkan layar terminal console.",
            "help": "Membuka panduan penggunaan alat di tab How to Use. CARA PAKAI: Ketik !help."
        }
        
        # * Roadmap Sejarah Sistem
        self.roadmap = [
            "v1.0-v3.x: Desktop UI Dasar.",
            "v4.0: Console Edition.",
            "v4.5: Interactive Shell Edition (Mode !tool & !exit)."
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
