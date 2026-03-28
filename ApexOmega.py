import sys
import os
import subprocess
import time
import zipfile
import shutil
import tempfile
from UI.InterfaceManager import InterfaceManager, console
from Core.NativeBridge import NativeBridge
from Modules.WebScanner import WebScanner
from Modules.NetworkScanner import NetworkScanner
from Modules.CryptoTools import CryptoTools
from Modules.SpecialTools import SpecialTools
from Modules.EduModule import EduModule

from UI.InterfaceDesktop import InterfaceDesktop
import threading

from Modules.GuidedAssistant import GuidedAssistant
from Modules.WordPressScanner import WordPressScanner
from Modules.PayloadGen import PayloadGen
from Modules.WebDiscovery import WebDiscovery
from Modules.VulnAtlas import VulnAtlas
from Modules.ApiAuditor import ApiAuditor
from Modules.CloudAudit import CloudAudit
import requests
from tkinter import messagebox

# * Inisialisasi framework Apex Omega Shell v5.1 (Auto-Pilot Edition)
class ApexOmega:
    VERSION = "5.7"
    def __init__(self, mode="gui"):
        self.stop_requested = False
        self.ui_mode = mode
        self.isRunning = True
        self.active_target = None
        self.current_module = None
        
        # * Inisialisasi Core & Modules
        self.ui = InterfaceManager()
        self.bridge = NativeBridge()
        self.web = WebScanner()
        self.wp = WordPressScanner()
        self.net = NetworkScanner(self.bridge)
        self.crypto = CryptoTools()
        self.special = SpecialTools()
        self.edu = EduModule()
        self.guided = GuidedAssistant()
        self.payload_gen = PayloadGen()
        self.discovery = WebDiscovery()
        self.atlas = VulnAtlas()
        self.api_auditor = ApiAuditor()
        self.cloud_audit = CloudAudit()
        
        # * Link Core for Global Events (v5.4)
        self.web.core = self
        self.atlas.core = self
        self.net.core = self
        self.discovery.core = self
        self.api_auditor.core = self
        self.wp.core = self
        self.special.core = self
        self.payload_gen.core = self
        self.cloud_audit.core = self
        
        # * GUI Handle
        if self.ui_mode == "gui":
            self.gui = InterfaceDesktop(self)
        else:
            self.gui = None

    # * Jalankan banner awal dan verifikasi sistem
    def startup(self):
        if self.ui_mode == "cli":
            console.clear()
            self.ui.showBanner()
            self.ui.logStatus("Memeriksa mesin Apex v5.5...", "info")
            time.sleep(0.5)
            
            if self.bridge.startNativeSession():
                self.ui.logStatus("WinSock Native Bridge: ONLINE", "success")
            else:
                self.ui.logStatus("Native Bridge: FALLBACK (Python Mode)", "warning")
            self.mainLoop()
        else:
            # * Jalankan GUI Shell
            self.bridge.startNativeSession()
            self.gui.mainloop()

    # * Berhenti paksa tool yang sedang jalan (v5.4 Control-c)
    def stop_running_tool(self):
        self.stop_requested = True
        self.gui.log_to_terminal("\n[!] PANIC STOP INITIATED (Ctrl+C). Terminating current process...\n", "[error] ")
        self.gui.show_prompt()

    # * Set Target Utama (IP/Domain)
    def set_active_target(self, target):
        self.active_target = target
        return target

    # * Interactive Shell Command Handler (Terminal Logic v5.4)
    def execute_shell_command(self, userInput):
        parts = userInput.split()
        if not parts: return
        
        # * Reset flag stop tiap kali command baru dieksekusi v5.4
        self.stop_requested = False
        
        def thread_task():
            # * Format: !nmap atau !exit
            command = parts[0].strip().lower()
            
            if command == "!exit":
                if self.current_module:
                    self.gui.log_to_terminal(f"Exiting module: {self.current_module}")
                    self.current_module = None
                else:
                    self.gui.log_to_terminal("Already at root. Use standard exit to close apps.")
                return

            # * Pilih Modul (Format !tool)
            if command.startswith("!"):
                tool_name = command[1:] # Hapus tanda seru
                
                # -- Verifikasi Tool v5.4 (Args Support) --
                args = parts[1:]
                
                if tool_name in ["recon", "info"]:
                    self.current_module = "recon"
                    self._run_recon_module(args)
                elif tool_name in ["nmap", "scan"]:
                    self.current_module = "nmap"
                    self._run_nmap_module(args)
                elif tool_name in ["webaudit", "web"]:
                    self.current_module = "webaudit"
                    self._run_web_module(args)
                elif tool_name in ["wordpress", "wp"]:
                    self.current_module = "wordpress"
                    self._run_wp_module(args)
                elif tool_name in ["chaos", "nitro"]:
                    self.current_module = "chaos"
                    self._run_chaos_module(args)
                elif tool_name in ["payload"]:
                    self.current_module = "payload"
                    self._run_payload_module(args)
                elif tool_name in ["subdomain", "sub"]:
                    self.current_module = "discovery"
                    self._run_subdomain_module(args)
                elif tool_name in ["vhost"]:
                    self.current_module = "discovery"
                    self._run_vhost_module(args)
                elif tool_name in ["webports", "ports"]:
                    self.current_module = "discovery"
                    self._run_webports_module(args)
                elif tool_name in ["vuln", "atlas"]:
                    self.current_module = "vulnerability"
                    self._run_vuln_module(args)
                elif tool_name in ["api"]:
                    self.current_module = "api"
                    self._run_api_module(args)
                elif tool_name in ["cloud"]:
                    self.current_module = "cloud"
                    self._run_cloud_module(args)
                elif tool_name in ["dirb", "directory"]:
                    self.current_module = "webaudit"
                    self._run_dirb_module(args)
                elif tool_name in ["headers", "security"]:
                    self.current_module = "webaudit"
                    self._run_headers_module(args)
                elif tool_name in ["form", "auditform"]:
                    self.current_module = "webaudit"
                    self._run_form_module(args)
                elif tool_name in ["cookie", "cookies"]:
                    self.current_module = "webaudit"
                    self._run_cookie_module(args)
                elif tool_name in ["git"]:
                    self.current_module = "webaudit"
                    self._run_git_module(args)
                elif tool_name == "help":
                    self.gui.tabview.set("How to Use")
                else:
                    self.gui.log_to_terminal(f"Error: Unknown tool '{tool_name}'.\n")
            
            # * Auto-show prompt after process completion v5.2
            self.gui.show_prompt()

        threading.Thread(target=thread_task, daemon=True).start()

    # -- Module Automated Runners --

    def _run_vuln_module(self, args=[]):
        if not self.active_target:
            self.gui.log_to_terminal("Vuln: No target set.\n", "[error] ")
            return
        target = self.active_target
        if not target.startswith('http'): target = f"http://{target}"
        
        mode = args[0] if args else "Full"
        self.gui.log_to_terminal(f"Starting VULN ATLAS ({mode}) on: {target}\n", "[init] ")
        
        # 1. Host Injection
        self.gui.log_to_terminal("  [*] Testing Host Header Injection...\n")
        host_vuln = self.atlas.checkHostInjection(target)
        if host_vuln: 
            self.gui.log_to_terminal(f"  [!] HOST INJECTION VULNERABLE: {host_vuln}\n", "[danger] ")
            self.gui.log_to_found(f"[VULN] Host Header Injection at {target} (Host: {host_vuln})")
        
        # 2. CORS Audit
        self.gui.log_to_terminal("  [*] Auditing CORS configuration...\n")
        cors = self.atlas.auditCors(target)
        if cors: 
            self.gui.log_to_terminal(f"  [!] CORS MISCONFIGURED: {cors}\n", "[warning] ")
            self.gui.log_to_found(f"[VULN] CORS Misconfig at {target} ({cors})")
        
        # 4. SSTI Check (v5.4 New)
        self.gui.log_to_terminal("  [*] Testing Server-Side Template Injection (SSTI)...\n")
        ssti = self.atlas.checkSsti(target)
        if ssti: 
            self.gui.log_to_terminal(f"  [!!!] SSTI VULNERABLE: Found echo with payload {ssti}\n", "[danger] ")
            self.gui.log_to_found(f"[VULN] SSTI Detected at {target} (Payload: {ssti})")

        # 5. File Upload Detection (v5.4 New)
        self.gui.log_to_terminal("  [*] Searching for File Upload vectors...\n")
        if self.atlas.checkUpload(target):
            self.gui.log_to_terminal("  [!] FILE UPLOAD DETECTED: Found upload form on page\n", "[warning] ")
            self.gui.log_to_found(f"[INTERESTING] File Upload Form Found at {target}")

        # 6. CRLF Injection (v5.4 New)
        self.gui.log_to_terminal("  [*] Testing CRLF Injection (HTTP Splitting)...\n")
        if self.atlas.checkCrlf(target):
            self.gui.log_to_terminal("  [!] CRLF INJECTION VULNERABLE: Header injection possible\n", "[danger] ")
            self.gui.log_to_found(f"[VULN] CRLF Injection Vulnerability at {target}")

        # 7. Path Fuzzing (Extreme 100+ Paths)
        self.gui.log_to_terminal("  [*] Fuzzing 100+ Sensitive Paths (config, backup, dev, git)...\n")
        paths = self.atlas.fuzzSensitivePaths(target)
        for p, code in paths:
            self.gui.log_to_terminal(f"  [+] FOUND PATH: {p:25} (HTTP {code})\n", "[success] ")
        
        self.gui.log_to_terminal("Vuln Scan Complete. Type !exit to switch.\n")

    def _run_api_module(self):
        if not self.active_target:
            self.gui.log_to_terminal("API: No target set.\n", "[error] ")
            return
        target = self.active_target
        if not target.startswith('http'): target = f"http://{target}"
        
        self.gui.log_to_terminal(f"API AUDITOR: Scanning {target}...\n", "[init] ")
        
        # 1. API Fuzz
        self.gui.log_to_terminal("  [*] Fuzzing API Endpoints (v1, v2, graphql, rest)...\n")
        res = self.api_auditor.fuzzEndpoints(target)
        for e in res:
            self.gui.log_to_terminal(f"  [+] API ENDPOINT: {e}\n", "[success] ")
            
        # 2. Method Check
        self.gui.log_to_terminal("  [*] Testing HTTP Methods (PUT, DELETE, PATCH)...\n")
        m_res = self.api_auditor.checkAllowedMethods(target)
        self.gui.log_to_terminal(f"  [+] ALLOWED: {', '.join(m_res)}\n")
        
        self.gui.log_to_terminal("API Audit Complete.\n")

    def _run_stress_module(self, args=[]):
        if not self.active_target:
            self.gui.log_to_terminal("Stress: No target set.\n", "[error] ")
            return
        
        threads = int(args[0]) if args else 50
        self.gui.log_to_terminal(f"[*] STRESS ENGINE: Launching {threads} threads to {self.active_target} (Nitro-Flood)\n", "[init] ")
        
        # Simulasi serangan asinkron dengan support stop flag v5.4
        self.special.runNitroStress(self.active_target, threads=threads)
        self.gui.log_to_terminal("  [!] Attack Running (Check target status manually)\n", "[danger] ")
        
        self.gui.log_to_terminal("Stress complete. Check server health.\n", "[info] ")
        self.gui.update_roadmap_check(6)

    def _run_dirb_module(self, args=[]):
        if not self.active_target:
            self.gui.log_to_terminal("Dirb: No target set.\n", "[error] ")
            return
        baseUrl = f"http://{self.active_target}" if not self.active_target.startswith("http") else self.active_target
        self.gui.log_to_terminal(f"[*] DIRB: Brute-forcing directories on {baseUrl}\n", "[init] ")
        
        commonDirs = ["admin", "config", "backup", "dev", "login", "wp-admin"]
        for d in commonDirs:
            if self.stop_requested: break
            target = urljoin(baseUrl, d)
            code = self.web.checkPath(target)
            if code:
                tag = "[success]" if code == 200 else "[warning]"
                self.gui.log_to_terminal(f"  [+] /{d:20} (HTTP {code})\n", tag)
                self.gui.log_to_found(f"[DIR] Found path: {baseUrl}/{d} (HTTP {code})")
        self.gui.log_to_terminal("Dirb complete.\n", "[info] ")

    def _run_headers_module(self, args=[]):
        if not self.active_target:
            self.gui.log_to_terminal("Headers: No target set.\n", "[error] ")
            return
        target = f"http://{self.active_target}" if not self.active_target.startswith("http") else self.active_target
        self.gui.log_to_terminal(f"[*] HEADERS: Auditing Security Headers on {target}\n", "[init] ")
        res = self.web.auditSecurityHeaders(target)
        for line in res:
            tag = "[success]" if "PRESENT" in line else "[error]"
            self.gui.log_to_terminal(f"  {line}\n", tag)

    def _run_form_module(self, args=[]):
        if not self.active_target:
            self.gui.log_to_terminal("Forms: No target set.\n", "[error] ")
            return
        target = f"http://{self.active_target}" if not self.active_target.startswith("http") else self.active_target
        self.gui.log_to_terminal(f"[*] FORMS: Auditing HTML Forms on {target}\n", "[init] ")
        res = self.web.auditForms(target)
        for f in res:
            self.gui.log_to_terminal(f"  [!] Form #{f['id']} | Action: {f['action']} | Method: {f['method']}\n", "[warning] ")
            if f['inputs']: self.gui.log_to_terminal(f"      Inputs: {', '.join(f['inputs'])}\n")
        if not res: self.gui.log_to_terminal("  [-] No forms found on landing page.\n")

    def _run_cookie_module(self, args=[]):
        if not self.active_target:
            self.gui.log_to_terminal("Cookie: No target set.\n", "[error] ")
            return
        target = f"http://{self.active_target}" if not self.active_target.startswith("http") else self.active_target
        self.gui.log_to_terminal(f"[*] COOKIE: Auditing Session Cookies on {target}\n", "[init] ")
        res = self.web.auditCookies(target)
        for c in res:
            self.gui.log_to_terminal(f"  [!] Cookie: {c['name']}\n", "[success] ")
            h_tag = "[success]" if c['httpOnly'] else "[error]"
            s_tag = "[success]" if c['secure'] else "[error]"
            self.gui.log_to_terminal(f"      HttpOnly: {c['httpOnly']}\n", h_tag)
            self.gui.log_to_terminal(f"      Secure:   {c['secure']}\n", s_tag)
        if not res: self.gui.log_to_terminal("  [-] No cookies received from target.\n")

    def _run_git_module(self, args=[]):
        if not self.active_target:
            self.gui.log_to_terminal("Git: No target set.\n", "[error] ")
            return
        target = f"http://{self.active_target}" if not self.active_target.startswith("http") else self.active_target
        self.gui.log_to_terminal(f"[*] GIT: Searching for exposed .git directory on {target}\n", "[init] ")
        res = self.web.checkGitExposed(target)
        for f in res:
            self.gui.log_to_terminal(f"  [!!!] CRITICAL EXPOSURE: {f}\n", "[danger] ")
        if not res: self.gui.log_to_terminal("  [-] No public .git repository found.\n")

    def _run_cloud_module(self):
        if not self.active_target:
            self.gui.log_to_terminal("Cloud: No target set.\n", "[error] ")
            return
        self.gui.log_to_terminal(f"CLOUD HUNTER: Searching for Buckets for {self.active_target}...\n", "[init] ")
        res = self.cloud_audit.findCloudBuckets(self.active_target)
        for b in res:
            self.gui.log_to_terminal(f"  [!] PUBLIC BUCKET FOUND: {b}\n", "[danger] ")
        if not res:
            self.gui.log_to_terminal("  [-] No public buckets found.\n")
        self.gui.log_to_terminal("Cloud Hunt complete.\n")

    def _run_payload_module(self):
        if not self.active_target:
            self.gui.log_to_terminal("Payload Gen: No target set, using generic payload.\n", "[info] ")
        
        # Contoh payload sederhana (bypass/xss)
        text = self.active_target if self.active_target else "alert('ApexOmega')"
        res = self.payload_gen.generate(text)
        
        self.gui.log_to_terminal(f"Generating Payloads for: {text}\n", "[gen] ")
        for fmt, val in res.items():
            self.gui.log_to_terminal(f"  {fmt}: {val}\n", "[+] ")
        self.gui.log_to_terminal("Payloads ready. Type !exit to switch.\n")

    def _run_subdomain_module(self):
        if not self.active_target:
            self.gui.log_to_terminal("Discovery: No target set.\n", "[error] ")
            return
        self.gui.log_to_terminal(f"Bruteforcing Subdomains for: {self.active_target}\n", "[info] ")
        res = self.discovery.bruteSubdomain(self.active_target)
        for host, ip in res:
            self.gui.log_to_terminal(f"  [+] {host:20} -> {ip}\n", "[success] ")
            self.gui.log_to_found(f"[SUBDOMAIN] Found host: {host} ({ip})")
        self.gui.log_to_terminal(f"Scan complete. Found {len(res)} subdomains.\n")

    def _run_vhost_module(self):
        if not self.active_target:
            self.gui.log_to_terminal("Discovery: No target set.\n", "[error] ")
            return
        # * VHost butuh IP aslinya kalau targetnya domain
        try:
            ip = socket.gethostbyname(self.active_target)
            self.gui.log_to_terminal(f"Hunting VHosts on {ip} for {self.active_target}...\n", "[info] ")
            res = self.discovery.findVHosts(ip, self.active_target)
            for v, code in res:
                self.gui.log_to_terminal(f"  [+] {v:25} (HTTP {code})\n", "[success] ")
            self.gui.log_to_terminal("VHost scan complete.\n")
        except:
            self.gui.log_to_terminal("Error: Could not resolve target IP for VHost scan.\n")

    def _run_webports_module(self):
        if not self.active_target:
            self.gui.log_to_terminal("Discovery: No target set.\n", "[error] ")
            return
        self.gui.log_to_terminal(f"Scanning Web Ports for: {self.active_target}\n", "[info] ")
        res = self.discovery.scanWebPorts(self.active_target)
        for p in res:
            self.gui.log_to_terminal(f"  [+] Port {p} is OPEN\n", "[success] ")
        self.gui.log_to_terminal("Port scan complete.\n")

    def _run_recon_module(self, args=[]):
        if not self.active_target:
            self.gui.log_to_terminal("Recon: Target not set.\n", "[error] ")
            return
        
        mode = args[0] if args else "quick"
        self.gui.log_to_terminal(f"[*] INITIATING {mode.upper()} RECON: {self.active_target}\n", "[init] ")
        
        try:
            # 1. IP & DNS Info
            self.gui.log_to_terminal("  [*] Fetching DNS & IP Records...\n")
            records = self.net.getDnsInfo(self.active_target)
            for k, v in records.items():
                self.gui.log_to_terminal(f"  [+] {k:10}: {v}\n", "[success] ")
            
            # 2. Tech Detection
            self.gui.log_to_terminal("  [*] Detecting Web Technologies...\n")
            target_url = f"http://{self.active_target}" if not self.active_target.startswith("http") else self.active_target
            tech = self.web.detectTech(target_url)
            self.gui.log_to_terminal(f"  [+] Server: {tech.get('server', ['Unknown'])[0]}\n", "[success] ")
            
            self.gui.log_to_terminal("Recon Complete. Step 1 Finished.\n", "[info] ")
            self.gui.update_roadmap_check(1)
        except Exception as e:
            self.gui.log_to_terminal(f"Recon Error: {str(e)}\n", "[error] ")

    def _run_nmap_module(self, args=[]):
        if not self.active_target:
            self.gui.log_to_terminal("Nmap: Target not set.\n", "[error] ")
            return
            
        custom_ports = args[0].split(",") if args else None
        port_msg = f"Ports: {args[0]}" if custom_ports else "Common Web Ports"
        
        self.gui.log_to_terminal(f"[*] NMAP INFRA SCAN ({port_msg}): {self.active_target}\n", "[init] ")
        
        try:
            if custom_ports:
                # * Logic for custom ports
                res = []
                for p in custom_ports:
                    if self.discovery._scan_single_port(self.active_target, int(p)):
                        res.append(p)
            else:
                res = self.discovery.scanWebPorts(self.active_target)
                
            if res:
                for p in res:
                    self.gui.log_to_terminal(f"  [!] PORT {p} is OPEN\n", "[success] ")
            else:
                self.gui.log_to_terminal("  [-] No target ports open.\n", "[warning] ")
                
            self.gui.log_to_terminal("Nmap Infrastructure Scan Complete.\n", "[info] ")
            self.gui.update_roadmap_check(2)
        except Exception as e:
            self.gui.log_to_terminal(f"Nmap Error: {str(e)}\n", "[error] ")

    def _run_web_module(self):
        if not self.active_target:
            self.gui.log_to_terminal("ERROR: Target not set.")
            return
        self.gui.log_to_terminal(f"Modul Web Audit Aktif on {self.active_target}...")
        tech = self.web.detectTech(self.active_target)
        if tech["framework"]: self.gui.log_to_terminal(f"Framework: {', '.join(tech['framework'])}")
        sqli = self.web.runBrutalSqlScan(self.active_target)
        if sqli: self.gui.log_to_terminal(f"SQLi Found: {len(sqli)} targets!")
        self.gui.log_to_terminal("Web Audit Complete. Type !exit to switch.")

    def _run_wp_module(self):
        if not self.active_target:
            self.gui.log_to_terminal("ERROR: Target not set.")
            return
        self.gui.log_to_terminal(f"WP Specialized Module: Checking {self.active_target}...")
        ver = self.wp.detectVersion(self.active_target)
        self.gui.log_to_terminal(f"Version: {ver}")
        self.gui.log_to_terminal("WP Scan Complete.")

    def _run_chaos_module(self):
        if not self.active_target:
            self.gui.log_to_terminal("ERROR: Target not set.")
            return
        self.gui.log_to_terminal(f"NITRO ATTACK Active on {self.active_target}...")
        res = self.special.runNitroStress(self.active_target, duration=5, threads=20)
        self.gui.log_to_terminal(res)
        self.gui.log_to_terminal("Attack cycle finished.")

# -- Update Core --

    # * Cek dan download update otomatis dari GitHub
    def check_updates(self):
        def task():
            self.gui.log_to_terminal("[root@shell] Checking GitHub for updates (jekk1/ApexOmega)...\n", "[inspect] ")
            try:
                # * Cache Buster: Tambahkan timestamp ke URL biar gak kena cache GitHub
                versionUrl = f"https://raw.githubusercontent.com/jekk1/ApexOmega/main/version.txt?t={int(time.time())}"
                response = requests.get(versionUrl, timeout=5)
                if response.status_code != 200:
                    self.gui.log_to_terminal(f"Failed to check updates (HTTP {response.status_code})")
                    self.gui.show_prompt()
                    return
                
                remoteVer = response.text.strip()
                
                # -- Logika Small Update v5.7.1 --
                if remoteVer < self.VERSION:
                    self.gui.log_to_terminal(f"Warning: Remote version (v{remoteVer}) is older than local (v{self.VERSION}).\n", "[warning] ")
                    self.gui.show_prompt()
                    return
                
                isSmallUpdate = False
                if remoteVer == self.VERSION:
                    confirm = messagebox.askyesno("ApexOmega: Small Update", f"System sudah v{self.VERSION}. Mau lakuin 'Small Update' (Force Sync) dari GitHub?")
                    if not confirm:
                        self.gui.log_to_terminal(f"System is up-to-date (v{self.VERSION}).\n", "[info] ")
                        self.gui.show_prompt()
                        return
                    isSmallUpdate = True
                
                # -- Proceed with Update (Large or Small) --
                msg = f"\n[!] New version found: v{remoteVer}\n" if not isSmallUpdate else "\n[*] Initiating Small Update (Force Sync)...\n"
                self.gui.log_to_terminal(msg, "[warning] " if not isSmallUpdate else "[info] ")
                
                if not isSmallUpdate:
                    confirm = messagebox.askyesno("ApexOmega Update", f"Ada versi baru v{remoteVer}. Mau download & restart otomatis?")
                    if not confirm: 
                        self.gui.log_to_terminal("Update dibatalkan oleh user.")
                        return

                self.gui.log_to_terminal("[*] Downloading updates from GitHub (Git Pull)...\n", "[info] ")
                try:
                    result = subprocess.run(["git", "pull", "origin", "main"], capture_output=True, text=True, timeout=30)
                    if result.returncode == 0:
                        self.gui.log_to_terminal("[+] Update downloaded successfully!\n", "[success] ")
                        self.gui.log_to_terminal("[*] Restarting application in 3s...\n", "[info] ")
                        time.sleep(3)
                        self.restart_app()
                    else:
                        self.gui.log_to_terminal(f"[-] Git Pull Error: {result.stderr}\n", "[error] ")
                except Exception as e:
                    self.gui.log_to_terminal(f"[-] Update Failed: {str(e)}\n", "[error] ")
                    
            except Exception as e:
                self.gui.log_to_terminal(f"Update Error: {str(e)}")
        
        threading.Thread(target=task, daemon=True).start()

    # * Seamless Restart v5.1
    def restart_app(self):
        try:
            # * Launch instance baru dan exit yang lama secara seamless
            subprocess.Popen([sys.executable] + sys.argv)
            os._exit(0)
        except Exception as e:
            print(f"Failed to restart: {e}")
            sys.exit(0)

    # * Download ZIP dari GitHub dan replace file project
    def _performUpdate(self, remoteVer):
        try:
            zipUrl = "https://github.com/jekk1/ApexOmega/archive/refs/heads/main.zip"
            self.gui.log_to_terminal("Downloading update package...")
            
            response = requests.get(zipUrl, timeout=30, stream=True)
            if response.status_code != 200:
                self.gui.log_to_terminal(f"Download failed (HTTP {response.status_code})")
                return
            
            # * Lokasi Software/ saat ini
            softwareDir = os.path.dirname(os.path.abspath(__file__))
            rootDir = os.path.dirname(softwareDir)
            tempDir = os.path.join(rootDir, "_update_temp")
            zipPath = os.path.join(rootDir, "_update.zip")
            
            with open(zipPath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            self.gui.log_to_terminal("Extracting update...")
            if os.path.exists(tempDir):
                shutil.rmtree(tempDir)
            
            with zipfile.ZipFile(zipPath, "r") as zf:
                zf.extractall(tempDir)
            
            extractedFolders = os.listdir(tempDir)
            if not extractedFolders:
                self.gui.log_to_terminal("ERROR: Empty archive.")
                return
            
            # * Repo root di ZIP: ApexOmega-main/ (Sekarang isinya langsung data Software)
            sourceRepoRoot = os.path.join(tempDir, extractedFolders[0])
            sourceSoftwareDir = sourceRepoRoot
            
            if not os.path.exists(os.path.join(sourceSoftwareDir, "ApexOmega.py")):
                self.gui.log_to_terminal("ERROR: Main script not found in update.")
                return

            self.gui.log_to_terminal("Replacing files...")
            updatedCount = 0
            
            # * Update isi Software/
            for item in os.listdir(sourceSoftwareDir):
                if item in {".git", "__pycache__", "_update_temp", "_update.zip"}:
                    continue
                
                srcPath = os.path.join(sourceSoftwareDir, item)
                dstPath = os.path.join(softwareDir, item)
                
                try:
                    if os.path.isdir(srcPath):
                        if os.path.exists(dstPath):
                            shutil.rmtree(dstPath, ignore_errors=True)
                        shutil.copytree(srcPath, dstPath)
                    else:
                        shutil.copy2(srcPath, dstPath)
                    updatedCount += 1
                except Exception as e:
                    self.gui.log_to_terminal(f"  [!] Skipped: {item} (File in use?)")
            
            # * Cleanup
            shutil.rmtree(tempDir, ignore_errors=True)
            if os.path.exists(zipPath):
                os.remove(zipPath)
            
            self.gui.log_to_terminal(f"Update complete! {updatedCount} items updated to v{remoteVer}.\n")
            self.gui.log_to_terminal("[!] AUTO-RESTARTING SYSTEM TO APPLY CHANGES...\n", "[danger] ")
            
            # * Kasih jeda dikit biar user sempet baca log
            time.sleep(2)
            self.restart_app()
            
        except Exception as e:
            self.gui.log_to_terminal(f"Update Error: {str(e)}")
            # * Final cleanup
            rootDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            tempDir = os.path.join(rootDir, "_update_temp")
            zipPath = os.path.join(rootDir, "_update.zip")
            shutil.rmtree(tempDir, ignore_errors=True)
            if os.path.exists(zipPath):
                os.remove(zipPath)

    # * Restart aplikasi otomatis (v5.5)
    def restart_app(self):
        self.gui.log_to_terminal("\n[!] RESTARTING APEXOMEGA v5.5...\n", "[init] ")
        self.bridge.stopNativeSession()
        
        # * Restart process pake executable python yang sama
        python = sys.executable
        os.execl(python, python, *sys.argv)

    # * Bersihkan sesi
    def exitFramework(self):
        self.bridge.stopNativeSession()
        self.isRunning = False
        if self.ui_mode == "cli":
            sys.exit(0)

if __name__ == "__main__":
    app = ApexOmega(mode="gui")
    app.startup()
