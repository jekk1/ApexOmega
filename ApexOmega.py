import sys
import os
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
import requests
from tkinter import messagebox

# * Inisialisasi framework Apex Omega Shell v4.6 (Zaqi Interactive Edition)
class ApexOmega:
    VERSION = "4.6"
    def __init__(self, mode="gui"):
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
            self.ui.logStatus("Memeriksa mesin Apex v4.5...", "info")
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

    # * Set Target Utama (IP/Domain)
    def set_active_target(self, target):
        self.active_target = target
        return target

    # * Interactive Shell Command Handler (Zaqi Shell Logic)
    def execute_shell_command(self, cmd):
        def thread_task():
            # * Format: !nmap atau !exit
            command = cmd.strip().lower()
            
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
                
                # -- Verifikasi Tool --
                if tool_name in ["nmap", "nethub", "recon"]:
                    self.current_module = "nmap"
                    self._run_nmap_module()
                elif tool_name in ["webaudit", "web", "scan"]:
                    self.current_module = "webaudit"
                    self._run_web_module()
                elif tool_name in ["wordpress", "wp"]:
                    self.current_module = "wordpress"
                    self._run_wp_module()
                elif tool_name in ["chaos", "nitro"]:
                    self.current_module = "chaos"
                    self._run_chaos_module()
                elif tool_name == "help":
                    self.gui.tabview.set("How to Use")
                else:
                    self.gui.log_to_terminal(f"Error: Unknown tool '{tool_name}'.")

        threading.Thread(target=thread_task, daemon=True).start()

    # -- Module Automated Runners --

    def _run_nmap_module(self):
        if not self.active_target:
            self.gui.log_to_terminal("ERROR: Target not set. Please type target first.")
            return
        self.gui.log_to_terminal(f"Modul Nmap Aktif. Scanning {self.active_target}...")
        records = self.net.getAllDnsRecords(self.active_target)
        for k, v in records.items():
            self.gui.log_to_terminal(f"{k}: {v}")
        self.gui.log_to_terminal("Nmap Scan Complete. Type !exit to switch.")

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
            self.gui.log_to_terminal("Checking GitHub for updates (jekk1/ApexOmega)...")
            try:
                versionUrl = "https://raw.githubusercontent.com/jekk1/ApexOmega/main/version.txt"
                response = requests.get(versionUrl, timeout=5)
                if response.status_code != 200:
                    self.gui.log_to_terminal(f"Failed to check updates (HTTP {response.status_code})")
                    return
                
                remoteVer = response.text.strip()
                if remoteVer <= self.VERSION:
                    self.gui.log_to_terminal(f"System is up-to-date (v{self.VERSION}).")
                    return
                
                self.gui.log_to_terminal(f"UPDATE AVAILABLE: v{remoteVer} (current: v{self.VERSION})")
                confirm = messagebox.askyesno("Update Available", f"Version {remoteVer} tersedia.\nDownload dan install sekarang?")
                if not confirm:
                    self.gui.log_to_terminal("Update skipped by user.")
                    return
                
                self._performUpdate(remoteVer)
            except Exception as e:
                self.gui.log_to_terminal(f"Update Error: {str(e)}")
        
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
            
            projectDir = os.path.dirname(os.path.abspath(__file__))
            tempDir = os.path.join(projectDir, "_update_temp")
            zipPath = os.path.join(projectDir, "_update.zip")
            
            # * Simpan ZIP ke disk
            with open(zipPath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            self.gui.log_to_terminal("Extracting update...")
            
            # * Extract ZIP
            if os.path.exists(tempDir):
                shutil.rmtree(tempDir)
            
            with zipfile.ZipFile(zipPath, "r") as zf:
                zf.extractall(tempDir)
            
            # * Cari folder hasil extract (biasanya ApexOmega-main/)
            extractedFolders = os.listdir(tempDir)
            if not extractedFolders:
                self.gui.log_to_terminal("ERROR: Empty archive.")
                return
            
            sourceDir = os.path.join(tempDir, extractedFolders[0])
            
            # * Replace files dari source ke project directory
            updatedCount = 0
            skippedItems = {"_update_temp", "_update.zip", ".git", "__pycache__", "Software"}
            
            for item in os.listdir(sourceDir):
                if item in skippedItems:
                    continue
                
                srcPath = os.path.join(sourceDir, item)
                dstPath = os.path.join(projectDir, item)
                
                if os.path.isdir(srcPath):
                    if os.path.exists(dstPath):
                        shutil.rmtree(dstPath)
                    shutil.copytree(srcPath, dstPath)
                else:
                    shutil.copy2(srcPath, dstPath)
                updatedCount += 1
                self.gui.log_to_terminal(f"  Updated: {item}")
            
            # * Bersihkan temp files
            shutil.rmtree(tempDir, ignore_errors=True)
            if os.path.exists(zipPath):
                os.remove(zipPath)
            
            self.gui.log_to_terminal(f"Update complete! {updatedCount} items updated to v{remoteVer}.")
            self.gui.log_to_terminal("Please restart the application to apply changes.")
            messagebox.showinfo("Update Complete", f"Updated to v{remoteVer}.\nPlease restart the application.")
            
        except Exception as e:
            self.gui.log_to_terminal(f"Update Error: {str(e)}")
            # * Cleanup on failure
            tempDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_update_temp")
            zipPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_update.zip")
            shutil.rmtree(tempDir, ignore_errors=True)
            if os.path.exists(zipPath):
                os.remove(zipPath)

    # * Bersihkan sesi
    def exitFramework(self):
        self.bridge.stopNativeSession()
        self.isRunning = False
        if self.ui_mode == "cli":
            sys.exit(0)

if __name__ == "__main__":
    app = ApexOmega(mode="gui")
    app.startup()
