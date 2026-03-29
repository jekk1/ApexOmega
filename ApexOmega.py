import os
import sys

# --- DLL PATH FALLBACK v5.8.6 (ABSOLUTE) ---
# Harus paling atas sebelum import UI yang pake Tkinter
try:
    python_dir = os.path.dirname(sys.executable)
    # Deteksi folder DLLs & Tcl di Python 3.13
    dll_dir = os.path.join(python_dir, 'DLLs')
    tcl_dir = os.path.join(python_dir, 'tcl')
    
    if os.path.exists(dll_dir):
        if hasattr(os, 'add_dll_directory'):
            os.add_dll_directory(dll_dir)
        os.environ['PATH'] = dll_dir + os.pathsep + os.environ['PATH']
    
    if os.path.exists(tcl_dir):
        os.environ['TCL_LIBRARY'] = os.path.join(tcl_dir, 'tcl8.6')
        os.environ['TK_LIBRARY'] = os.path.join(tcl_dir, 'tk8.6')
except Exception:
    pass

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
from Modules.HeadsCheck import HeadsCheck

from UI.InterfaceDesktop import InterfaceDesktop
import threading

from Modules.GuidedAssistant import GuidedAssistant
from Modules.WordPressScanner import WordPressScanner
from Modules.PayloadGen import PayloadGen
from Modules.WebDiscovery import WebDiscovery
from Modules.VulnAtlas import VulnAtlas
from Modules.ApiAuditor import ApiAuditor
from Modules.CloudAudit import CloudAudit
from Modules.ScriptLibrary import ScriptLibrary
import requests
import socket
from tkinter import messagebox
from urllib.parse import urljoin

# --- CONFIGURATION (v5.9.8) ---
VERSION_URL = "https://raw.githubusercontent.com/jekk1/ApexOmega/main/version.txt"
REPO_ZIP_URL = "https://github.com/jekk1/ApexOmega/archive/refs/heads/main.zip"

class ApexOmega:
    def __init__(self, mode="gui"):
        self.VERSION = self._load_version()
        socket.setdefaulttimeout(3) # * Anti-Stuck Globally
        self.stop_requested = False
        self.ui_mode = mode
        self.isRunning = True
        self.active_target = None
        self.current_module = None
        self.update_check_in_progress = False
        
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
        self.script_lib = ScriptLibrary()
        
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

    # ? Load versi secara dinamis dari file (v5.9.4)
    def _load_version(self):
        try:
            rootDir = os.path.dirname(os.path.abspath(__file__))
            vPath = os.path.join(rootDir, "version.txt")
            if os.path.exists(vPath):
                with open(vPath, "r") as f:
                    return f.read().strip()
            return "6.1.0"
        except:
            return "6.1.0"

    # * Jalankan banner awal dan verifikasi sistem
    def startup(self):
        if self.ui_mode == "cli":
            console.clear()
            self.ui.showBanner()
            self.ui.logStatus("Memeriksa mesin Apex v5.9...", "info")
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

    # * Set Target Utama (IP/Domain) - Auto-sanitize
    def set_active_target(self, target):
        if not target: return None
        from urllib.parse import urlparse
        # * Contoh: https://google.com/test/ -> google.com
        clean = urlparse(target).netloc if "://" in target else target.split('/')[0]
        # * Strip port and spaces
        self.active_target = clean.split(':')[0].strip()
        return self.active_target

    # * Interactive Shell Command Handler (Terminal Logic v5.9)
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
                    self.gui.log_to_terminal(f"Exiting module: {self.current_module}\n", "[info] ")
                    self.current_module = None
                
                if self.active_target:
                    self.gui.log_to_terminal("Returning to global root session...\n", "[warning] ")
                    self.active_target = None
                    self.gui.reset_roadmap()
                else:
                    self.gui.log_to_terminal("Already at root. Use standard exit to close apps.\n", "[info] ")
                
                # Paksa reset target dan kembalikan ke root prompt
                self.gui.show_prompt()
                return

            # * Unified Dispatch v6.1.0 (Secret Mode Support)
            userInput_trimmed = userInput.strip()
            if userInput_trimmed == "!testalltools!":
                self.gui.start_hacker_mode()
                return

            tool_name = userInput_trimmed.lower().replace("!", "").split()[0]
            args = userInput_trimmed.split()[1:]
            
            try:
                self._dispatch_module(tool_name, args)
            except Exception as e:
                self.gui.log_to_terminal(f"Error executing {tool_name}: {e}\n", "error")
            finally:
                if self.gui:
                    self.gui.show_prompt()

        threading.Thread(target=thread_task, daemon=True).start()

    # -- Module Dispatcher & Runners --

    def _dispatch_module(self, tool_name, args=[]):
        mapping = {
            "nmap": self._run_nmap_module,
            "recon": self._run_recon_module,
            "vuln": self._run_vuln_module,
            "atlas": self._run_vuln_module,
            "api": self._run_api_module,
            "cloud": self._run_cloud_module,
            "dirb": self._run_dirb_module,
            "directory": self._run_dirb_module,
            "headers": self._run_headers_module,
            "security": self._run_headers_module,
            "form": self._run_form_module,
            "cookie": self._run_cookie_module,
            "cookies": self._run_cookie_module,
            "git": self._run_git_module,
            "wp": self._run_wp_module,
            "wordpress": self._run_wp_module,
            "chaos": self._run_chaos_module,
            "nitro": self._run_stress_module,
            "stress": self._run_stress_module,
            "payload": self._run_payload_module,
            "webaudit": self._run_web_module,
            "subdomain": self._run_subdomain_module,
            "vhost": self._run_vhost_module,
            "webport": self._run_webports_module,
            "webports": self._run_webports_module,
            "sqlmap": self._run_web_module,
            "aoi": self._run_web_module,
            "testalltools": self._run_testalltools_module,
            "help": self._run_help_module,
            "script": self._run_script_module
        }
        
        if tool_name in mapping:
            self.current_module = tool_name
            mapping[tool_name](args)
        else:
            self.gui.log_to_terminal(f"[!] Unknown tool: {tool_name}. Type !help for manual.\n", "error")

    # -- Module Automated Runners (v5.9 Child Command Support) --

    # * Vuln Atlas Scanner dengan mode spesifik
    def _run_vuln_module(self, args=[]):
        if not self.active_target:
            self.gui.log_to_terminal("Vuln: No target set.\n", "[error] ")
            return
        target = f"https://{self.active_target}"
        
        mode = args[0].lower() if args else "full"
        self.gui.log_to_terminal(f"Starting VULN ATLAS ({mode}) on: {target}\n", "[init] ")
        
        runAll = (mode == "full")
        
        # 1. Host Injection
        if runAll or mode == "host":
            self.gui.log_to_terminal("  [*] Testing Host Header Injection...\n")
            host_vuln = self.atlas.checkHostInjection(target)
            if host_vuln: 
                self.gui.log_to_terminal(f"  [!] HOST INJECTION VULNERABLE: {host_vuln}\n", "[danger] ")
                self.gui.log_to_found(f"[VULN] Host Header Injection at {target} (Host: {host_vuln})")
        
        # 2. CORS Audit
        if runAll or mode == "cors":
            self.gui.log_to_terminal("  [*] Auditing CORS configuration...\n")
            cors = self.atlas.auditCors(target)
            if cors: 
                self.gui.log_to_terminal(f"  [!] CORS MISCONFIGURED: {cors}\n", "[warning] ")
                self.gui.log_to_found(f"[VULN] CORS Misconfig at {target} ({cors})")
        
        # 3. SSTI Check
        if runAll or mode == "ssti":
            self.gui.log_to_terminal("  [*] Testing Server-Side Template Injection (SSTI)...\n")
            ssti = self.atlas.checkSsti(target)
            if ssti: 
                self.gui.log_to_terminal(f"  [!!!] SSTI VULNERABLE: Found echo with payload {ssti}\n", "[danger] ")
                self.gui.log_to_found(f"[VULN] SSTI Detected at {target} (Payload: {ssti})")

        # 4. File Upload Detection
        if runAll or mode == "upload":
            self.gui.log_to_terminal("  [*] Searching for File Upload vectors...\n")
            if self.atlas.checkUpload(target):
                self.gui.log_to_terminal("  [!] FILE UPLOAD DETECTED: Found upload form on page\n", "[warning] ")
                self.gui.log_to_found(f"[INTERESTING] File Upload Form Found at {target}")

        # 5. CRLF Injection
        if runAll or mode == "crlf":
            self.gui.log_to_terminal("  [*] Testing CRLF Injection (HTTP Splitting)...\n")
            if self.atlas.checkCrlf(target):
                self.gui.log_to_terminal("  [!] CRLF INJECTION VULNERABLE: Header injection possible\n", "[danger] ")
                self.gui.log_to_found(f"[VULN] CRLF Injection Vulnerability at {target}")

        # 6. Path Fuzzing
        if runAll or mode == "paths":
            self.gui.log_to_terminal("  [*] Fuzzing 100+ Sensitive Paths (config, backup, dev, git)...\n")
            paths = self.atlas.fuzzSensitivePaths(target)
            for p, code in paths:
                self.gui.log_to_terminal(f"  [+] FOUND PATH: {p:25} (HTTP {code})\n", "[success] ")
        
        self.gui.log_to_terminal("Vuln Scan Complete. Type !exit to switch.\n")

    # * API Auditor dengan mode fuzz/methods/all
    def _run_api_module(self, args=[]):
        if not self.active_target:
            self.gui.log_to_terminal("API: No target set.\n", "[error] ")
            return
        target = f"https://{self.active_target}"
        
        mode = args[0].lower() if args else "all"
        self.gui.log_to_terminal(f"API AUDITOR ({mode}): Scanning {target}...\n", "[init] ")
        
        # 1. API Fuzz
        if mode in ["fuzz", "all"]:
            self.gui.log_to_terminal("  [*] Fuzzing API Endpoints (v1, v2, graphql, rest)...\n")
            res = self.api_auditor.fuzzEndpoints(target)
            for e in res:
                self.gui.log_to_terminal(f"  [+] API ENDPOINT: {e}\n", "[success] ")
            
        # 2. Method Check
        if mode in ["methods", "all"]:
            self.gui.log_to_terminal("  [*] Testing HTTP Methods (PUT, DELETE, PATCH)...\n")
            m_res = self.api_auditor.checkAllowedMethods(target)
            self.gui.log_to_terminal(f"  [+] ALLOWED: {', '.join(m_res)}\n")
        
        self.gui.log_to_terminal("API Audit Complete.\n")

    # * Stress Engine (format: !stress <threads> <duration>)
    def _run_stress_module(self, args=[]):
        if not self.active_target:
            self.gui.log_to_terminal("Stress: No target set.\n", "[error] ")
            return
            
        if len(args) < 2:
            self.gui.log_to_terminal("Usage: !stress <threads/workers> <duration_seconds>\n", "[warning] ")
            self.gui.log_to_terminal("Example: !stress 200 30\n", "[info] ")
            return
            
        try:
            threads = int(args[0])
            duration = int(args[1])
        except ValueError:
            self.gui.log_to_terminal("[!] Invalid input. Harus angka: !stress <threads> <duration>\n", "[error] ")
            return
        
        self.gui.log_to_terminal(f"[*] STRESS ENGINE: Launching {threads} workers for {duration}s to {self.active_target}\n", "[init] ")
        res = self.special.runNitroStress(self.active_target, duration=duration, threads=threads)
        
        if duration > 0:
            self.gui.log_to_terminal(f"  [!] Attack running... (Wait {duration}s or press ESC to stop)\n", "[danger] ")
            start_wait = time.time()
            while time.time() - start_wait < duration:
                if self.stop_requested or not self.isRunning:
                    break
                # * Live Status v5.8.14 (Overwrite)
                s = self.special.stats
                curr_status = f"\r  [*] PROGRESS: [success .{s['success']}x] [blocked .{s['blocked']}x] [redirect .{s['redirect']}x] [error .{s['error']}x]"
                self.gui.log_to_terminal(curr_status, "[info] ")
                time.sleep(1.0)
            self.gui.log_to_terminal("\n[*] Attack Duration Finished.\n", "[info] ")
        else:
            self.gui.log_to_terminal(f"  [!] Infinite Attack Running (Press ESC or !stop to terminate)\n", "[danger] ")
            while not self.stop_requested and self.isRunning:
                s = self.special.stats
                curr_status = f"\r  [*] PROGRESS: [success .{s['success']}x] [blocked .{s['blocked']}x] [redirect .{s['redirect']}x] [error .{s['error']}x]"
                self.gui.log_to_terminal(curr_status, "[info] ")
                time.sleep(1.0)
        
        self.gui.update_roadmap_check(7)

    # * Directory Brute Force (mode: common/deep)
    def _run_dirb_module(self, args=[]):
        if not self.active_target:
            self.gui.log_to_terminal("Dirb: No target set.\n", "[error] ")
            return
        baseUrl = f"https://{self.active_target}"
        
        mode = args[0].lower() if args else "common"
        self.gui.log_to_terminal(f"[*] DIRB ({mode}): Brute-forcing directories on {baseUrl}\n", "[init] ")
        
        if mode == "deep":
            commonDirs = ["admin", "config", "backup", "dev", "login", "wp-admin", "api", "v1", "v2",
                          "test", "private", "shell.php", "cmd.php", ".env", "phpinfo.php", ".git", "administrator"]
        else:
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

    # * Headers Audit
    def _run_headers_module(self, args=[]):
        self.gui.log_to_terminal(f"\n[*] INITIATING HEADS-CHECK (SECURITY HEADERS AUDIT)...\n", "cyanText")
        scanner = HeadsCheck(self)
        scanner.scan()

    # * Form Auditor
    def _run_form_module(self, args=[]):
        if not self.active_target:
            self.gui.log_to_terminal("Forms: No target set.\n", "[error] ")
            return
        target = f"https://{self.active_target}"
        self.gui.log_to_terminal(f"[*] FORMS: Auditing HTML Forms on {target}\n", "[init] ")
        res = self.web.auditForms(target)
        for f in res:
            self.gui.log_to_terminal(f"  [!] Form #{f['id']} | Action: {f['action']} | Method: {f['method']}\n", "[warning] ")
            if f['inputs']: self.gui.log_to_terminal(f"      Inputs: {', '.join(f['inputs'])}\n")
        if not res: self.gui.log_to_terminal("  [-] No forms found on landing page.\n")

    # * Cookie Auditor
    def _run_cookie_module(self, args=[]):
        if not self.active_target:
            self.gui.log_to_terminal("Cookie: No target set.\n", "[error] ")
            return
        target = f"https://{self.active_target}"
        self.gui.log_to_terminal(f"[*] COOKIE: Auditing Session Cookies on {target}\n", "[init] ")
        res = self.web.auditCookies(target)
        for c in res:
            self.gui.log_to_terminal(f"  [!] Cookie: {c['name']}\n", "[success] ")
            h_tag = "[success]" if c['httpOnly'] else "[error]"
            s_tag = "[success]" if c['secure'] else "[error]"
            self.gui.log_to_terminal(f"      HttpOnly: {c['httpOnly']}\n", h_tag)
            self.gui.log_to_terminal(f"      Secure:   {c['secure']}\n", s_tag)
        if not res: self.gui.log_to_terminal("  [-] No cookies received from target.\n")

    # * Git Exposure Scanner (mode: check/deep)
    def _run_git_module(self, args=[]):
        if not self.active_target:
            self.gui.log_to_terminal("Git: No target set.\n", "[error] ")
            return
        target = f"https://{self.active_target}"
        mode = args[0].lower() if args else "check"
        self.gui.log_to_terminal(f"[*] GIT ({mode}): Searching for exposed .git directory on {target}\n", "[init] ")
        res = self.web.checkGitExposed(target)
        for f in res:
            self.gui.log_to_terminal(f"  [!!!] CRITICAL EXPOSURE: {f}\n", "[danger] ")
        if not res: self.gui.log_to_terminal("  [-] No public .git repository found.\n")
        
        # Deep mode: coba download content yang terexpose
        if mode == "deep" and res:
            self.gui.log_to_terminal("  [*] Attempting to read exposed content...\n")
            for f in res:
                try:
                    url = urljoin(target, f)
                    r = requests.get(url, timeout=5)
                    if r.status_code == 200:
                        preview = r.text[:200].replace('\n', ' ')
                        self.gui.log_to_terminal(f"  [+] Content ({f}): {preview}...\n", "[success] ")
                        self.gui.log_to_found(f"[GIT LEAK] {f} content readable at {target}")
                except Exception:
                    pass

    # * Cloud Bucket Scanner (mode: s3/firebase/gcs/all)
    def _run_cloud_module(self, args=[]):
        if not self.active_target:
            self.gui.log_to_terminal("Cloud: No target set.\n", "[error] ")
            return
        
        mode = args[0].lower() if args else "all"
        self.gui.log_to_terminal(f"CLOUD HUNTER ({mode}): Searching for Buckets for {self.active_target}...\n", "[init] ")
        
        # Filter suffix berdasarkan mode
        suffixMap = {
            "s3": [".s3.amazonaws.com"],
            "firebase": [".firebaseio.com"],
            "gcs": [".storage.googleapis.com"],
            "all": [".s3.amazonaws.com", ".firebaseio.com", ".storage.googleapis.com"]
        }
        
        suffixes = suffixMap.get(mode, suffixMap["all"])
        originalSuffixes = self.cloud_audit.cloudSuffixes
        self.cloud_audit.cloudSuffixes = suffixes
        
        res = self.cloud_audit.findCloudBuckets(self.active_target)
        for b in res:
            self.gui.log_to_terminal(f"  [!] PUBLIC BUCKET FOUND: {b}\n", "[danger] ")
        if not res:
            self.gui.log_to_terminal("  [-] No public buckets found.\n")
        self.gui.log_to_terminal("Cloud Hunt complete.\n")
        
        # Restore
        self.cloud_audit.cloudSuffixes = originalSuffixes

    # * Payload Generator (mode: encode/decode)
    def _run_payload_module(self, args=[]):
        mode = args[0].lower() if args else "encode"
        
        if mode == "decode" and len(args) >= 3:
            fmt = args[1].lower()
            text = " ".join(args[2:])
            self.gui.log_to_terminal(f"Decoding ({fmt}): {text}\n", "[gen] ")
            result = self.payload_gen.decode(text, fmt)
            self.gui.log_to_terminal(f"  Result: {result}\n", "[success] ")
        else:
            # Encode mode (default)
            text = " ".join(args[1:]) if len(args) > 1 else (self.active_target if self.active_target else "alert('ApexOmega')")
            res = self.payload_gen.generate(text)
            
            self.gui.log_to_terminal(f"Generating Payloads for: {text}\n", "[gen] ")
            if res:
                for fmt, val in res.items():
                    self.gui.log_to_terminal(f"  {fmt}: {val}\n", "[+] ")
        self.gui.log_to_terminal("Payloads ready. Type !exit to switch.\n")

    # * Subdomain Scanner (mode: brute/passive)
    def _run_subdomain_module(self, args=[]):
        if not self.active_target:
            self.gui.log_to_terminal("Discovery: No target set.\n", "[error] ")
            return
        
        mode = args[0].lower() if args else "brute"
        
        if mode == "passive":
            self.gui.log_to_terminal(f"Passive Subdomain Discovery (crt.sh) for: {self.active_target}\n", "[info] ")
            res = self.net.findSubdomains(self.active_target)
            for host in res:
                self.gui.log_to_terminal(f"  [+] {host}\n", "[success] ")
                self.gui.log_to_found(f"[SUBDOMAIN] Certificate found: {host}")
            self.gui.log_to_terminal(f"Scan complete. Found {len(res)} subdomains (passive).\n")
        else:
            self.gui.log_to_terminal(f"Bruteforcing Subdomains for: {self.active_target}\n", "[info] ")
            res = self.discovery.bruteSubdomain(self.active_target)
            for host, ip in res:
                self.gui.log_to_terminal(f"  [+] {host:20} -> {ip}\n", "[success] ")
                self.gui.log_to_found(f"[SUBDOMAIN] Found host: {host} ({ip})")
            self.gui.log_to_terminal(f"Scan complete. Found {len(res)} subdomains.\n")

    # * VHost Scanner
    def _run_vhost_module(self, args=[]):
        if not self.active_target:
            self.gui.log_to_terminal("Discovery: No target set.\n", "[error] ")
            return
        try:
            ip = socket.gethostbyname(self.active_target)
            self.gui.log_to_terminal(f"Hunting VHosts on {ip} for {self.active_target}...\n", "[info] ")
            res = self.discovery.findVHosts(ip, self.active_target)
            for v, code in res:
                self.gui.log_to_terminal(f"  [+] {v:25} (HTTP {code})\n", "[success] ")
            self.gui.log_to_terminal("VHost scan complete.\n")
        except:
            self.gui.log_to_terminal("Error: Could not resolve target IP for VHost scan.\n")

    # * Web Ports Scanner (mode: common/full)
    def _run_webports_module(self, args=[]):
        if not self.active_target:
            self.gui.log_to_terminal("Discovery: No target set.\n", "[error] ")
            return
        
        mode = args[0].lower() if args else "common"
        
        if mode == "full":
            self.discovery.webPorts = [80, 443, 3000, 3001, 4000, 4200, 4443, 5000, 5001, 5555,
                                       8000, 8008, 8080, 8081, 8443, 8888, 9000, 9090, 9200, 9443]
        
        self.gui.log_to_terminal(f"Scanning Web Ports ({mode}) for: {self.active_target}\n", "[info] ")
        res = self.discovery.scanWebPorts(self.active_target)
        for p in res:
            self.gui.log_to_terminal(f"  [+] Port {p} is OPEN\n", "[success] ")
        self.gui.log_to_terminal("Port scan complete.\n")
        
        # Restore default
        if mode == "full":
            self.discovery.webPorts = [80, 443, 8000, 8008, 8080, 8081, 8443, 8888, 9000, 9443]

    # * Recon Module (mode: quick/deep/full)
    def _run_recon_module(self, args=[]):
        if not self.active_target:
            self.gui.log_to_terminal("Recon: Target not set.\n", "[error] ")
            return
        
        mode = args[0].lower() if args else "quick"
        self.gui.log_to_terminal(f"[*] INITIATING {mode.upper()} RECON: {self.active_target}\n", "[init] ")
        
        try:
            # 1. IP & DNS Info (semua mode)
            self.gui.log_to_terminal("  [*] Fetching DNS & IP Records...\n")
            records = self.net.getDnsInfo(self.active_target)
            for k, v in records.items():
                self.gui.log_to_terminal(f"  [+] {k:10}: {v}\n", "[success] ")
            
            # 2. Tech Detection (semua mode)
            self.gui.log_to_terminal("  [*] Detecting Web Technologies...\n")
            target_url = f"https://{self.active_target}"
            tech = self.web.detectTech(target_url)
            server_list = tech.get('server', [])
            server_info = server_list[0] if server_list else "Unknown"
            self.gui.log_to_terminal(f"  [+] Server: {server_info}\n", "[success] ")
            
            # 3. Deep mode: WHOIS + All DNS Records
            if mode in ["deep", "full"]:
                self.gui.log_to_terminal("  [*] Fetching WHOIS Data...\n")
                whois = self.net.whoisLookup(self.active_target)
                if "error" not in whois:
                    name = whois.get("name", "Unknown")
                    self.gui.log_to_terminal(f"  [+] WHOIS Name: {name}\n", "[success] ")
                else:
                    self.gui.log_to_terminal(f"  [-] WHOIS: {whois.get('error', 'Not found')}\n", "[warning] ")
                
                self.gui.log_to_terminal("  [*] Fetching All DNS Records (A, AAAA, MX, TXT, NS)...\n")
                allDns = self.net.getAllDnsRecords(self.active_target)
                for rType, rData in allDns.items():
                    preview = rData[:80] if isinstance(rData, str) else str(rData)[:80]
                    self.gui.log_to_terminal(f"  [+] {rType:5}: {preview}\n", "[success] ")
            
            # 4. Full mode: Tech detail + Certificate Subdomains
            if mode == "full":
                if tech.get("framework"):
                    self.gui.log_to_terminal(f"  [+] Frameworks: {', '.join(tech['framework'])}\n", "[success] ")
                if tech.get("cms"):
                    self.gui.log_to_terminal(f"  [+] CMS: {', '.join(tech['cms'])}\n", "[success] ")
                if tech.get("waf"):
                    self.gui.log_to_terminal(f"  [!] WAF Detected: {', '.join(tech['waf'])}\n", "[warning] ")
                
                self.gui.log_to_terminal("  [*] Searching Certificate Subdomains (crt.sh)...\n")
                certSubs = self.net.findSubdomains(self.active_target)
                for sub in certSubs[:10]:
                    self.gui.log_to_terminal(f"  [+] CertSub: {sub}\n", "[success] ")
                if len(certSubs) > 10:
                    self.gui.log_to_terminal(f"  [*] ... and {len(certSubs)-10} more subdomains\n", "[info] ")
            
            self.gui.log_to_terminal("Recon Complete. Step 1 Finished.\n", "[info] ")
            self.gui.update_roadmap_check(0)
        except Exception as e:
            self.gui.log_to_terminal(f"Recon Error: {str(e)}\n", "[error] ")

    # * Nmap Port Scanner (custom ports support)
    def _run_nmap_module(self, args=[]):
        if not self.active_target:
            self.gui.log_to_terminal("Nmap: Target not set.\n", "[error] ")
            return
            
        custom_ports = args[0].split(",") if args else None
        port_msg = f"Ports: {args[0]}" if custom_ports else "Common Web Ports"
        
        self.gui.log_to_terminal(f"[*] NMAP INFRA SCAN ({port_msg}): {self.active_target}\n", "[init] ")
        
        try:
            if custom_ports:
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
            self.gui.update_roadmap_check(1)
        except Exception as e:
            self.gui.log_to_terminal(f"Nmap Error: {str(e)}\n", "[error] ")

    # * Web Audit Module (mode: tech/sqli/full)
    def _run_web_module(self, args=[]):
        if not self.active_target:
            self.gui.log_to_terminal("ERROR: Target not set.\n", "[error] ")
            return
        
        mode = args[0].lower() if args else "full"
        target = f"https://{self.active_target}"
        self.gui.log_to_terminal(f"Modul Web Audit ({mode}) Aktif on {target}...\n", "[init] ")
        
        if mode in ["tech", "full"]:
            tech = self.web.detectTech(target)
            if tech["framework"]: self.gui.log_to_terminal(f"Framework: {', '.join(tech['framework'])}\n", "[success] ")
            if tech["cms"]: self.gui.log_to_terminal(f"CMS: {', '.join(tech['cms'])}\n", "[success] ")
            if tech["server"]: self.gui.log_to_terminal(f"Server: {', '.join(tech['server'])}\n", "[success] ")
        
        if mode in ["sqli", "full"]:
            sqli = self.web.runBrutalSqlScan(target)
            if sqli: self.gui.log_to_terminal(f"SQLi Found: {len(sqli)} targets!\n", "[danger] ")
        
        self.gui.log_to_terminal("Web Audit Complete. Type !exit to switch.\n")

    # * WordPress Scanner (mode: version/plugins/users/files/all)
    def _run_wp_module(self, args=[]):
        if not self.active_target:
            self.gui.log_to_terminal("ERROR: Target not set.\n", "[error] ")
            return
        
        target = f"https://{self.active_target}"
        mode = args[0].lower() if args else "all"
        self.gui.log_to_terminal(f"WP Scanner ({mode}): Checking {target}...\n", "[init] ")
        
        runAll = (mode == "all")
        
        if runAll or mode == "version":
            ver = self.wp.detectVersion(target)
            self.gui.log_to_terminal(f"WP Version Detected: {ver}\n", "[success] " if ver != "Unknown" else "[warning] ")
        
        if runAll or mode == "plugins":
            plugins = self.wp.scanPlugins(target)
            if plugins:
                for p in plugins:
                    self.gui.log_to_terminal(f"  [+] Plugin Found: {p}\n", "[success] ")
                    self.gui.log_to_found(f"[WP] Plugin: {p} at {target}")
            else:
                self.gui.log_to_terminal("  [-] No common plugins detected.\n")
        
        if runAll or mode == "users":
            users = self.wp.enumerateUsers(target)
            if users:
                for u in users:
                    self.gui.log_to_terminal(f"  [+] User Found: {u}\n", "[success] ")
                    self.gui.log_to_found(f"[WP] User: {u} at {target}")
            else:
                self.gui.log_to_terminal("  [-] User enumeration blocked or no users found.\n")
        
        if runAll or mode == "files":
            files = self.wp.checkVulnFiles(target)
            if files:
                for f in files:
                    self.gui.log_to_terminal(f"  [!!!] VULN FILE EXPOSED: {f}\n", "[danger] ")
                    self.gui.log_to_found(f"[WP CRITICAL] Exposed file: {f} at {target}")
            else:
                self.gui.log_to_terminal("  [-] No vulnerable files found.\n")

    def _run_chaos_module(self, args=[]):
        if not self.active_target:
            self.gui.log_to_terminal("ERROR: Target not set.\n", "[error] ")
            return
        self.gui.log_to_terminal(f"NITRO ATTACK Active on {self.active_target}...\n")
        res = self.special.runNitroStress(self.active_target, duration=5, threads=20)
        self.gui.log_to_terminal(res)
        self.gui.log_to_terminal("Attack cycle finished.\n")

    # * Functional Test All Tools v6.1.0 (Sequential Diagnostic Scan)
    def _run_testalltools_module(self, args=[]):
        if not self.active_target:
            self.gui.log_to_terminal("[!] TEST ALL: Target belum diset. Ketik target dulu.\n", "[error] ")
            return
        
        target = self.active_target
        self.gui.log_to_terminal("\n" + "="*60 + "\n", "[info] ")
        self.gui.log_to_terminal("  APEXOMEGA FUNCTIONAL DIAGNOSTIC SCAN v6.1.0\n", "[init] ")
        self.gui.log_to_terminal(f"  Target: {target}\n", "[info] ")
        self.gui.log_to_terminal("="*60 + "\n\n", "[info] ")
        
        # * Daftar tool yang akan diuji secara berurutan
        toolSequence = [
            ("recon",    "Reconnaissance",       ["quick"]),
            ("nmap",     "Infrastructure Scan",   []),
            ("headers",  "Security Headers",      []),
            ("cookie",   "Cookie Audit",          []),
            ("form",     "Form Audit",            []),
            ("git",      "Git Exposure",          []),
            ("dirb",     "Directory Bruteforce",  ["common"]),
            ("vuln",     "Vulnerability Scan",    ["full"]),
            ("api",      "API Audit",             ["all"]),
            ("cloud",    "Cloud Bucket Hunt",     ["all"]),
            ("wp",       "WordPress Scan",        ["all"]),
            ("subdomain","Subdomain Discovery",   ["brute"]),
            ("vhost",    "Virtual Host Scan",     []),
            ("webports", "Web Port Scan",         ["common"]),
            ("payload",  "Payload Generator",     []),
            ("webaudit", "Full Web Audit",        ["full"]),
        ]
        
        totalTools = len(toolSequence)
        results = []
        scanStart = time.time()
        
        for idx, (toolName, toolLabel, toolArgs) in enumerate(toolSequence):
            if self.stop_requested:
                self.gui.log_to_terminal("\n[!] DIAGNOSTIC SCAN ABORTED oleh user (ESC/Ctrl+C).\n", "[warning] ")
                remaining = totalTools - idx
                for r in range(remaining):
                    results.append((toolSequence[idx + r][1], "SKIPPED", 0))
                break
            
            progress = f"[{idx+1}/{totalTools}]"
            self.gui.log_to_terminal(f"\n{'─'*50}\n", "[info] ")
            self.gui.log_to_terminal(f"  {progress} {toolLabel.upper()} ({toolName})\n", "[init] ")
            self.gui.log_to_terminal(f"{'─'*50}\n", "[info] ")
            
            toolStart = time.time()
            status = "PASS"
            
            try:
                self._dispatch_module(toolName, toolArgs)
            except Exception as e:
                status = "FAIL"
                self.gui.log_to_terminal(f"  [X] Error: {e}\n", "[error] ")
            
            elapsed = time.time() - toolStart
            results.append((toolLabel, status, elapsed))
            
            # * Status output per tool
            statusTag = "[success] " if status == "PASS" else "[error] "
            self.gui.log_to_terminal(f"  >> {toolLabel}: {status} ({elapsed:.1f}s)\n", statusTag)
            
            # * Jeda antar tool biar output ga numpuk
            time.sleep(0.3)
        
        # * Summary Report
        totalTime = time.time() - scanStart
        passCount = sum(1 for _, s, _ in results if s == "PASS")
        failCount = sum(1 for _, s, _ in results if s == "FAIL")
        skipCount = sum(1 for _, s, _ in results if s == "SKIPPED")
        
        self.gui.log_to_terminal("\n\n" + "="*60 + "\n", "[info] ")
        self.gui.log_to_terminal("  DIAGNOSTIC SCAN REPORT\n", "[init] ")
        self.gui.log_to_terminal("="*60 + "\n\n", "[info] ")
        
        for toolLabel, status, elapsed in results:
            if status == "PASS":
                tag = "[success] "
                icon = "[+]"
            elif status == "FAIL":
                tag = "[error] "
                icon = "[X]"
            else:
                tag = "[warning] "
                icon = "[-]"
            self.gui.log_to_terminal(f"  {icon} {toolLabel:30} {status:8} ({elapsed:.1f}s)\n", tag)
        
        self.gui.log_to_terminal(f"\n  Total: {passCount} PASS / {failCount} FAIL / {skipCount} SKIPPED\n", "[info] ")
        self.gui.log_to_terminal(f"  Duration: {totalTime:.1f}s\n", "[info] ")
        self.gui.log_to_terminal("="*60 + "\n", "[info] ")

    # * Help Command (terminal-side)
    def _run_help_module(self, args=[]):
        if args:
            tool = args[0].lower()
            usage = self.guided.getUsage(tool)
            info = self.guided.helpDatabase.get(tool, None)
            
            if usage:
                self.gui.log_to_terminal(f"\n=== HELP: {tool.upper()} ===\n", "cyanText")
                self.gui.log_to_terminal(f"Syntax: {usage['syntax']}\n\n", "[success] ")
                self.gui.log_to_terminal("Modes:\n", "[info] ")
                for m, desc in usage['modes'].items():
                    self.gui.log_to_terminal(f"  {m:20} - {desc}\n")
                self.gui.log_to_terminal("\nExamples:\n", "[info] ")
                for ex in usage['examples']:
                    self.gui.log_to_terminal(f"  {ex}\n", "[success] ")
                if info:
                    self.gui.log_to_terminal(f"\nInfo: {info}\n", "[init] ")
            else:
                self.gui.log_to_terminal(f"[!] No help data for: {tool}\n", "[error] ")
        else:
            self.gui.log_to_terminal("\n=== APEXOMEGA v5.9 - COMMAND REFERENCE ===\n", "cyanText")
            self.gui.log_to_terminal("Type !help <tool> for detailed usage.\n\n", "[info] ")
            
            cmdList = [
                ("!recon [quick|deep|full]", "Reconnaissance & intel gathering"),
                ("!nmap [ports]", "Infrastructure port scanning"),
                ("!vuln [full|cors|ssti|...]", "Vulnerability scanning"),
                ("!testalltools", "Functional Diagnostic Scan"),
                ("!testalltools!", "Secret Hacker Mode"),
                ("!api [fuzz|methods|all]", "API endpoint auditing"),
                ("!cloud [s3|firebase|gcs|all]", "Cloud bucket hunting"),
                ("!dirb [common|deep]", "Directory brute force"),
                ("!headers", "Security headers audit"),
                ("!form", "HTML form auditing"),
                ("!cookie", "Cookie security audit"),
                ("!git [check|deep]", "Git exposure scanning"),
                ("!wp [version|plugins|users|files|all]", "WordPress scanning"),
                ("!payload [encode|decode] [text]", "Payload encoding/decoding"),
                ("!subdomain [brute|passive]", "Subdomain discovery"),
                ("!vhost", "Virtual host discovery"),
                ("!webports [common|full]", "Web port scanning"),
                ("!webaudit [tech|sqli|full]", "Full web audit"),
                ("!stress <threads> <duration>", "Stress testing"),
                ("!script [category]", "Script/payload library"),
                ("!exit", "Exit module or reset target"),
            ]
            
            for cmd, desc in cmdList:
                self.gui.log_to_terminal(f"  {cmd:40} {desc}\n")

    # * Script Library Command (terminal-side)
    def _run_script_module(self, args=[]):
        if args:
            category = " ".join(args).lower()
            scripts = self.script_lib.searchScripts(category)
            if scripts:
                self.gui.log_to_terminal(f"\n=== SCRIPTS: {category.upper()} ({len(scripts)} found) ===\n", "cyanText")
                for i, s in enumerate(scripts):
                    risk_tag = "[danger] " if s["risk"] == "Critical" else "[warning] " if s["risk"] == "High" else "[info] "
                    self.gui.log_to_terminal(f"  [{i+1}] {s['name']} [{s['risk']}]\n", risk_tag)
                    self.gui.log_to_terminal(f"      {s['description']}\n", "[init] ")
                self.gui.log_to_terminal("\nUse the Scripts tab to preview & drag payloads to terminal.\n", "[info] ")
            else:
                self.gui.log_to_terminal(f"[!] No scripts found for: {category}\n", "[error] ")
        else:
            cats = self.script_lib.getCategories()
            self.gui.log_to_terminal("\n=== SCRIPT LIBRARY v5.9 ===\n", "cyanText")
            self.gui.log_to_terminal("Type !script <category> to list scripts.\n\n", "[info] ")
            for cat in cats:
                count = len(self.script_lib.getScripts(cat))
                self.gui.log_to_terminal(f"  {cat:25} ({count} scripts)\n", "[success] ")
            self.gui.log_to_terminal("\nOr open the Scripts tab for drag-and-drop.\n", "[info] ")

# -- Update Core --

    # * Cek dan download update otomatis dari GitHub
    def check_updates(self):
        if self.update_check_in_progress:
            return
            
        def task():
            self.update_check_in_progress = True
            self.gui.log_to_terminal("[root@shell] Checking GitHub for updates (jekk1/ApexOmega)...\n", "[inspect] ")
            try:
                # * Fetch remote version with Cache Buster & Headers (v6.0.0)
                try:
                    cache_buster = f"?t={int(time.time())}"
                    headers = {
                        "Cache-Control": "no-cache",
                        "Pragma": "no-cache",
                        "Expires": "0"
                    }
                    response = requests.get(VERSION_URL + cache_buster, headers=headers, timeout=5)
                    if response.status_code != 200:
                        self.gui.log_to_terminal(f"Failed to check updates (HTTP {response.status_code})\n")
                        self.show_prompt()
                        return
                    remoteVer = response.text.strip()
                except Exception as e:
                    self.gui.log_to_terminal(f"Connection Error: {str(e)}\n")
                    self.show_prompt()
                    return
                
                # * Parsing versi numerik biar kaku (Semver Parsing Fix)
                def parse_v(v): 
                    try: return [int(x) for x in v.split('.')]
                    except: return [0,0,0]
                
                curr_v = parse_v(self.VERSION)
                rem_v = parse_v(remoteVer)
                
                if rem_v > curr_v:
                    # Upgrade logic
                    self.gui.log_to_terminal(f"New version found: v{remoteVer} (Local: v{self.VERSION})\n", "[warning] ")
                    
                    confirm = messagebox.askyesno("ApexOmega Update", f"Ada versi baru v{remoteVer}. Mau download & restart otomatis?")
                    if not confirm: 
                        self.gui.log_to_terminal("Update dibatalkan oleh user.\n")
                        self.gui.show_prompt()
                        return

                    self.gui.log_to_terminal("[*] Downloading updates from GitHub (Auto-Sync)...\n", "[info] ")
                    try:
                        # Cek git dulu
                        git_check = subprocess.run(["git", "--version"], capture_output=True, text=True)
                        if git_check.returncode == 0:
                            result = subprocess.run(["git", "pull", "origin", "main"], capture_output=True, text=True, timeout=30)
                            if result.returncode == 0:
                                self.gui.log_to_terminal("[+] Update downloaded successfully via Git!\n", "[success] ")
                                self.gui.log_to_terminal("[*] Restarting application in 3s...\n", "[info] ")
                                time.sleep(3)
                                self.restart_app()
                            else:
                                raise Exception(f"Git Pull failed: {result.stderr}")
                        else:
                            raise FileNotFoundError
                    except (FileNotFoundError, Exception):
                        self.gui.log_to_terminal("[!] Git not detected or failed. Falling back to Direct Download (ZIP)...\n", "[warning] ")
                        self._performUpdate(remoteVer)
                elif rem_v < curr_v:
                    self.gui.log_to_terminal(f"Warning: Remote version (v{remoteVer}) is older than local (v{self.VERSION}).\n", "[warning] ")
                    self.gui.show_prompt()
                else:
                    self.gui.log_to_terminal(f"System is up-to-date (v{self.VERSION}).\n", "[success] ")
                    self.gui.show_prompt()
                    
            except Exception as e:
                self.gui.log_to_terminal(f"Update Error: {str(e)}\n")
                self.gui.show_prompt()
            finally:
                self.update_check_in_progress = False
        
        threading.Thread(target=task, daemon=True).start()

    # * Download ZIP dari GitHub dan replace file project
    def _performUpdate(self, remoteVer):
        try:
            zipUrl = "https://github.com/jekk1/ApexOmega/archive/refs/heads/main.zip"
            self.gui.log_to_terminal("Downloading update package...")
            
            response = requests.get(zipUrl, timeout=30, stream=True)
            if response.status_code != 200:
                self.gui.log_to_terminal(f"Download failed (HTTP {response.status_code})")
                return
            
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
                # * Defensive extraction: Hindari replace folder sistem yang bisa hijack EXE (v6.0.6)
                for member in zf.infolist():
                    # Check if file is in a forbidden library folder
                    if "customtkinter" in member.filename.lower() or "darkdetect" in member.filename.lower():
                        continue
                    zf.extract(member, tempDir)
            
            extractedFolders = os.listdir(tempDir)
            if not extractedFolders:
                self.gui.log_to_terminal("ERROR: Empty archive.")
                return
            
            sourceRepoRoot = os.path.join(tempDir, extractedFolders[0])
            sourceSoftwareDir = sourceRepoRoot
            
            if not os.path.exists(os.path.join(sourceSoftwareDir, "ApexOmega.py")):
                self.gui.log_to_terminal("ERROR: Main script not found in update.")
                return

            self.gui.log_to_terminal("Replacing files...")
            updatedCount = 0
            
            for item in os.listdir(sourceSoftwareDir):
                if item in {".git", "__pycache__", "_update_temp", "_update.zip"}:
                    continue
                
                srcPath = os.path.join(sourceSoftwareDir, item)
                dstPath = os.path.join(softwareDir, item)
                
                try:
                    # * Safe File Replacement v5.9.3 (Rename-Move trick for Windows)
                    if os.path.exists(dstPath):
                        if os.path.isfile(srcPath):
                            # Jika file (seperti .exe), rename dulu baru timpa
                            oldPath = dstPath + ".old"
                            if os.path.exists(oldPath): os.remove(oldPath)
                            os.rename(dstPath, oldPath)
                            shutil.copy2(srcPath, dstPath)
                            try: os.remove(oldPath)
                            except: pass
                        else:
                            # Jika folder, hapus dan copy
                            shutil.rmtree(dstPath, ignore_errors=True)
                            shutil.copytree(srcPath, dstPath)
                    else:
                        if os.path.isdir(srcPath):
                            shutil.copytree(srcPath, dstPath)
                        else:
                            shutil.copy2(srcPath, dstPath)
                    updatedCount += 1
                except:
                    self.gui.log_to_terminal(f"  [!] Skipped: {item} (File in use?)")
            
            shutil.rmtree(tempDir, ignore_errors=True)
            if os.path.exists(zipPath):
                os.remove(zipPath)
            
            self.gui.log_to_terminal(f"Update complete! {updatedCount} items updated to v{remoteVer}.\n")
            self.gui.log_to_terminal("[!] AUTO-RESTARTING SYSTEM TO APPLY CHANGES...\n", "[danger] ")
            
            time.sleep(2)
            self.restart_app()
            
        except Exception as e:
            self.gui.log_to_terminal(f"Update Error: {str(e)}")
            rootDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            tempDir = os.path.join(rootDir, "_update_temp")
            zipPath = os.path.join(rootDir, "_update.zip")
            shutil.rmtree(tempDir, ignore_errors=True)
            if os.path.exists(zipPath):
                os.remove(zipPath)

    # * Restart aplikasi otomatis (v5.9.3 Fix DLL)
    def restart_app(self):
        self.gui.log_to_terminal("\n[!] RESTARTING APEXOMEGA v5.9.3...\n", "[init] ")
        self.bridge.stopNativeSession()
        
        try:
            # * Clear TCL/TK environment variables (v5.9.3 DLL Fix)
            # Menghindari error 'DLL load failed while importing _tkinter' 
            # karena folder temp lama masih nyangkut di environment.
            for env_var in ["TCL_LIBRARY", "TK_LIBRARY"]:
                if env_var in os.environ:
                    del os.environ[env_var]
            
            # * Gunakan Popen + exit (lebih stabil daripada execl di Windows)
            subprocess.Popen([sys.executable] + sys.argv, 
                             creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS if os.name == 'nt' else 0,
                             close_fds=True)
            os._exit(0)
        except Exception as e:
            # Fallback jika gagal
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
