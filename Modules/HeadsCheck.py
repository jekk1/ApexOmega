import requests

# * HeadsCheck v5.8 (Advanced Security Header Auditor)
class HeadsCheck:
    """
    HeadsCheck itu kayak inspektur safety buat header keamanan website.
    
    Header HTTP itu kayak surat keterangan dari server:
    - "Ini lho website saya, pake HTTPS ya!"
    - "Jangan coba-coba inject script di sini!"
    - "Data user gak boleh di-share ke domain lain!"
    
    Tool ini cek 6 header keamanan utama:
    
    1. HSTS (Strict-Transport-Security) - Paksa HTTPS
       - Tanpa ini: User bisa akses via HTTP (gak aman)
       - Dengan ini: Browser maksa pake HTTPS
    
    2. CSP (Content-Security-Policy) - Anti XSS
       - Batasi dari mana script bisa dimuat
       - Kalo ada hacker inject script dari domain lain → diblokir
    
    3. X-Frame-Options - Anti Clickjacking
       - Mencegah website di-embed di iframe hacker
       - Tanpa ini: Hacker bisa bikin website lu 'dipake' buat phishing
    
    4. X-Content-Type-Options - Anti MIME Sniffing
       - Browser jangan nebak-nebak tipe file
       - File .jpg ya .jpg, bukan .exe yang disamarkan
    
    5. Referrer-Policy - Kontrol Privacy
       - Batasi info yang dikirim ke website lain
       - Jangan sampe URL yang sensitif kebocoran
    
    6. Permissions-Policy - Kontrol Fitur Browser
       - Matikan fitur yang gak dipake (camera, mic, location)
       - Kurangi attack surface
    
    HASIL SCAN:
    - ✓ FOUND = Header ada, website aman
    - ✗ MISSING = Header gak ada, POTENSI BAHAYA!
    
    Website tanpa header keamanan itu kayak rumah tanpa kunci!
    """
    def __init__(self, core):
        self.core = core
        self.target = core.active_target
        
    # * Jalankan scan security headers
    def scan(self):
        if not self.target:
            self.core.gui.log_to_terminal("[!] Error: No active target set.\n", "error")
            return
            
        url = self.target if self.target.startswith("http") else f"https://{self.target}"
        self.core.gui.log_to_terminal(f"[*] Analyzing Headers for: {url}\n", "info")
        
        try:
            response = requests.get(url, timeout=10, verify=False)
            headers = response.headers
            
            # -- Daftar Header Keamanan Primer --
            security_headers = {
                "Strict-Transport-Security": "Proteksi HTTPS (HSTS)",
                "Content-Security-Policy": "Proteksi XSS/Injection (CSP)",
                "X-Frame-Options": "Proteksi Clickjacking (XFO)",
                "X-Content-Type-Options": "Proteksi MIME Sniffing",
                "Referrer-Policy": "Kontrol Referrer Privacy",
                "Permissions-Policy": "Kontrol API Browser (Features)"
            }
            
            found_count = 0
            missing_count = 0
            
            self.core.gui.log_to_terminal("\n--- AUDIT RESULTS ---\n", "cyanText")
            for header, desc in security_headers.items():
                if header in headers:
                    val = headers[header]
                    self.core.gui.log_to_terminal(f"[+] {header}: FOUND\n", "success")
                    self.core.gui.log_to_terminal(f"    Value: {val[:50]}...\n", "sysText")
                    found_count += 1
                else:
                    self.core.gui.log_to_terminal(f"[-] {header}: MISSING\n", "warning")
                    self.core.gui.log_to_terminal(f"    Desc: {desc}\n", "dimText")
                    # * Log to Found Tab as vulnerability
                    self.core.gui.log_to_found(f"[HEADER MISSING] {self.target} - {header} is not set.")
                    missing_count += 1
            
            # -- Info Server Header --
            server = headers.get("Server", "Unknown")
            self.core.gui.log_to_terminal(f"\n[*] Server Identity: {server}\n", "info")
            if server != "Unknown":
                self.core.gui.log_to_found(f"[INFO] Server Header Disclosure: {server} on {self.target}")

            self.core.gui.log_to_terminal(f"\n[!] Audit Complete: {found_count} OK, {missing_count} Missing.\n", "cyanText")
            
        except Exception as e:
            self.core.gui.log_to_terminal(f"[!] Connection Error: {str(e)}\n", "error")
