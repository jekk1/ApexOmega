import requests

# * HeadsCheck v5.8 (Advanced Security Header Auditor)
class HeadsCheck:
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
