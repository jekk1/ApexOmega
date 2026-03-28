import customtkinter as ctk
import threading
from tkinter import messagebox

# * Tema Shell Mode (Zaqi Interactive Edition v4.6)
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class InterfaceDesktop(ctk.CTk):
    def __init__(self, app_core):
        super().__init__()
        self.core = app_core
        self.title("ApexOmega Shell v5.7 (Ultra-Stable Edition)")
        self.geometry("1100x700")
        
        # * Standard Resizable Window
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.98)
        
        self.tools_visible = True # * Auto-Open Sidebar v5.0
        self.waitingTarget = True
        self._setup_ui()
        
        # * Auto-Prompt Target on Startup
        self.after(500, self._initial_prompt)
        # * Auto-Open Tools Sidebar on Startup
        self._populate_tools()
        self.tools_frame.pack(fill="both", expand=True, padx=5, pady=5)

    def _setup_ui(self):
        # * --- Main Container ---
        self.main_container = ctk.CTkFrame(self, fg_color="#0a0a0a", corner_radius=0)
        self.main_container.pack(fill="both", expand=True)
        
        # * --- Sidebar (Dynamic Tools) ---
        self.sidebar = ctk.CTkFrame(self.main_container, width=220, fg_color="#121212", corner_radius=0)
        self.sidebar.pack(side="left", fill="y", padx=2, pady=2)
        
        self.btn_tools_root = ctk.CTkButton(self.sidebar, text="TOOLS", font=("Roboto", 16, "bold"), fg_color="transparent", text_color="cyan", hover_color="#1a1a1a", anchor="center", height=45, command=self._toggle_tools)
        self.btn_tools_root.pack(fill="x", pady=20)
        
        # -- Expanding Tools Frame --
        self.tools_frame = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent")
        
        self.btn_update = ctk.CTkButton(self.sidebar, text="CHECK FOR UPDATES", font=("Roboto", 11, "bold"), fg_color="#1a1a1a", text_color="#555555", hover_color="#222222", height=30, command=self.core.check_updates)
        self.btn_update.pack(side="bottom", pady=5)

        self.credit_label = ctk.CTkLabel(self.sidebar, text="Credits to Zaqi", font=("Roboto", 11, "italic"), text_color="dim gray")
        self.credit_label.pack(side="bottom", pady=(10, 20))

        # * --- Content Area (Full Shell) ---
        self.content_area = ctk.CTkFrame(self.main_container, fg_color="#0a0a0a")
        self.content_area.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.tabview = ctk.CTkTabview(self.content_area, border_width=1, border_color="#222222", fg_color="#050505")
        self.tabview.pack(fill="both", expand=True)
        
        self.tab_console = self.tabview.add("Terminal")
        self.tab_roadmap = self.tabview.add("Roadmap")
        self.tab_found = self.tabview.add("Found")
        self.tab_tutorial = self.tabview.add("How to Use")
        
        # * Populate Roadmap Tab
        self._setup_roadmap_tab()

        # * Akses internal textbox dari CTkTextbox buat kontrol granular
        self.terminal = ctk.CTkTextbox(self.tab_console, font=("Consolas", 13), text_color="#cccccc", border_width=0, border_spacing=20, fg_color="#050505")
        self.terminal.pack(fill="both", expand=True)
        self._tw = self.terminal._textbox
        
        # * Tag warna untuk output v5.2 (Hacker Colors)
        self._tw.tag_config("sysText", foreground="#666666")
        self._tw.tag_config("dimText", foreground="#333333")
        self._tw.tag_config("prompt", foreground="#555555")
        self._tw.tag_config("inspect", foreground="#888888")
        
        # * Pentest Colors (Success, Error, Info, Warning)
        self._tw.tag_config("success", foreground="#00ff00") # * Ijo Terang
        self._tw.tag_config("greenText", foreground="#00ff00")
        self._tw.tag_config("error", foreground="#ff3333")   # * Merah Terang
        self._tw.tag_config("danger", foreground="#ff3333")
        self._tw.tag_config("warning", foreground="#ffcc00") # * Kuning/Orange
        self._tw.tag_config("info", foreground="#5dade2")    # * Blueish
        self._tw.tag_config("cyanText", foreground="#00ffff")
        self._tw.tag_config("init", foreground="#aaaaaa")
        
        # * Bind event untuk proteksi
        self._tw.bind("<Control-c>", lambda e: self.core.stop_running_tool())
        
        # * Label Instruksi Bawah
        lbl_info = ctk.CTkLabel(self.tab_console, text="[!] CTRL+C TO STOP | !EXIT TO ROOT | !HELP FOR MANUAL", font=("Roboto", 10), text_color="#444444")
        lbl_info.pack(side="bottom", pady=5)
        self._tw.bind("<Key>", self._on_key)
        self._tw.bind("<BackSpace>", self._on_backspace)
        self._tw.bind("<Delete>", self._on_delete)
        self._tw.bind("<<Cut>>", self._block_cut)
        self._tw.bind("<Control-a>", self._block_select_all)
        
        self._tw.insert("end", "ApexOmega Console [Version: 5.7]\n", "dimText")
        self._tw.insert("end", "Ultra-Stable Edition (Thread-Safe Refresh)\n\n", "dimText")
        
        # * Mark posisi awal input (semua sebelumnya protected)
        self._tw.mark_set("inputStart", "end-1c")
        self._tw.mark_gravity("inputStart", "left")

        # * --- Setup Tab Found (Harta Karun) ---
        self.found_box = ctk.CTkTextbox(self.tab_found, font=("Consolas", 13), text_color="#00ff00", fg_color="#050505", border_width=0, border_spacing=20)
        self.found_box.pack(fill="both", expand=True)
        self.found_box.insert("end", "[*] HARTA KARUN SYSTEM (v5.6)\n", "success")
        self.found_box.insert("end", "[*] Hasil scouting penting bakal dicatet di sini otomatis.\n", "dimText")
        self.found_box.insert("end", "-"*50 + "\n\n")
        self.found_box.configure(state="disabled")

    # * Prompt awal minta target
    def _initial_prompt(self):
        self._append_system("[root@shell] ENTER TARGET IP/URL >> ", "prompt")
        self._set_input_mark()

    # * Tulis teks system yang terproteksi (Internal - No After)
    def _append_system(self, text, tag="sysText"):
        self._tw.insert("end", text, tag)
        self._tw.see("end")

    # * Set input mark setelah output baru (Internal - No After)
    def _set_input_mark(self):
        self._tw.mark_set("inputStart", "end-1c")
        self._tw.mark_gravity("inputStart", "left")
        self._tw.see("end")

    # * Blokir penghapusan teks sebelum inputStart
    def _on_backspace(self, event):
        cursorPos = self._tw.index("insert")
        markPos = self._tw.index("inputStart")
        if self._tw.compare(cursorPos, "<=", markPos):
            return "break"
        return None

    # * Blokir delete key di area protected
    def _on_delete(self, event):
        cursorPos = self._tw.index("insert")
        markPos = self._tw.index("inputStart")
        if self._tw.compare(cursorPos, "<", markPos):
            return "break"
        return None

    # * Blokir ketikan di area protected
    def _on_key(self, event):
        if event.keysym in ("Return", "BackSpace", "Delete", "Left", "Right", "Up", "Down", "Home", "End"):
            return None
        if event.state & 0x4:
            return None
        cursorPos = self._tw.index("insert")
        markPos = self._tw.index("inputStart")
        if self._tw.compare(cursorPos, "<", markPos):
            self._tw.mark_set("insert", "end-1c")
        return None

    # * Blokir cut di area protected
    def _block_cut(self, event):
        try:
            selStart = self._tw.index("sel.first")
            markPos = self._tw.index("inputStart")
            if self._tw.compare(selStart, "<", markPos):
                return "break"
        except Exception:
            pass
        return None

    # * Blokir select all (cuma select area input)
    def _block_select_all(self, event):
        markPos = self._tw.index("inputStart")
        self._tw.tag_remove("sel", "1.0", "end")
        self._tw.tag_add("sel", markPos, "end-1c")
        return "break"

    # * Handle Enter (submit command/target)
    def _on_enter(self, event):
        # * Ambil input dari mark inputStart sampe akhir
        markPos = self._tw.index("inputStart")
        userInput = self._tw.get(markPos, "end-1c").strip()
        
        # --- NUCLEAR SYNC RESET v5.7.5 ---
        # Kita lakukan update UI secara sinkron seketika biar gak ada race condition
        self._tw.insert("end", "\n")
        
        target_display = self.core.active_target or "none"
        prompt_text = f"\n[root@shell:{target_display}] >> "
        
        # Cetak prompt dan kunci kursor dalam satu nafas
        self._tw.insert("end", prompt_text, "prompt")
        self._tw.mark_set("inputStart", "end-1c")
        self._tw.mark_gravity("inputStart", "left")
        self._tw.see("end")

        if not userInput:
            return "break"
        
        # * Mode command
        if userInput.startswith("!"):
            self.core.execute_shell_command(userInput)
        else:
            # * Cek apakah user mau ganti target
            target = userInput
            self.core.set_active_target(target)
            
            self._append_system(f"\n[root@shell] [INITIATING AUTOMATED RECON ON: {target}]\n", "cyanText")
            
            # -- Quick real recon v5.7.3 (Full Background) --
            def quick_recon():
                try:
                    import socket
                    socket.setdefaulttimeout(5) # * Anti-Stuck DNS
                    self.core.set_active_target(target)
                    self._append_system(f"[*] Reconnaissance for {target} started in background...\n", "info")
                    
                    # * Resolve IP dasar (Silent)
                    pure_domain = target.replace("http://", "").replace("https://", "").split("/")[0]
                    ip = socket.gethostbyname(pure_domain)
                    self.log_to_terminal(f"  [+] TARGET IP DISCOVERED: {ip}\n", "success")
                except Exception:
                    pass
            
            threading.Thread(target=quick_recon, daemon=True).start()
        
        return "break"

    # * Tampilkan prompt baru (Thread-Safe untuk v5.7)
    def show_prompt(self):
        def _exec():
            target = self.core.active_target or "none"
            self._append_system(f"\n[root@shell:{target}] >> ", "prompt")
            self._set_input_mark()
        self.after(0, _exec)

    # * Log output ke terminal (v5.7 Tag-Supported Thread-Safe)
    def log_to_terminal(self, message, tag="sysText"):
        def _exec():
            clean_tag = tag.replace("[", "").replace("]", "").strip()
            self._tw.insert("end", f"{message}", clean_tag)
            self._tw.see("end")
            self._set_input_mark()
        self.after(0, _exec)

    # * Log ke tab Found (Harta Karun - Thread-Safe v5.7)
    def log_to_found(self, message):
        def _exec():
            # Check if widget exists (prevent error during closing)
            if self.found_box.winfo_exists():
                self.found_box.configure(state="normal")
                self.found_box.insert("end", f"{message}\n")
                self.found_box.see("end")
                self.found_box.configure(state="disabled")
        self.after(0, _exec)

    def _toggle_tools(self):
        if not self.tools_visible:
            self.tools_frame.pack(fill="both", expand=True, padx=5, pady=5)
            self._populate_tools()
            self.tools_visible = True
        else:
            self.tools_frame.pack_forget()
            self.tools_visible = False

    def _populate_tools(self):
        # * Clear existing
        for widget in self.tools_frame.winfo_children():
            widget.destroy()
        
        # * Categorized Tools Listing (Kali Linux Style)
        categories = {
            "RECON / INFO": ["nmap", "recon", "webaudit", "headers", "cookie"],
            "DISCOVERY": ["subdomain", "vhost", "webports", "dirb", "git"],
            "VULNERABILITY": ["vuln", "wordpress", "wp", "form"],
            "API / CLOUD": ["api", "cloud"],
            "EXPLOITATION": ["payload", "sqlmap", "stress"]
        }
        
        for cat, tools in categories.items():
            # -- Category Header --
            lbl = ctk.CTkLabel(self.tools_frame, text=cat, font=("Roboto", 11, "bold"), text_color="#444444", anchor="w")
            lbl.pack(fill="x", pady=(10, 2), padx=5)
            
            for t in sorted(tools):
                btn = ctk.CTkButton(self.tools_frame, text=t.upper(), anchor="w", fg_color="transparent", text_color="#777777", hover_color="#1a1a1a", height=28, command=lambda x=t: self._show_how_to(x))
                btn.pack(fill="x", pady=0)

    # * Setup Roadmap Tab: Menjadi Misi Penaklukan (Checklist)
    def _setup_roadmap_tab(self):
        # * Clear existing if reload
        for widget in self.tab_roadmap.winfo_children():
            widget.destroy()

        lbl_title = ctk.CTkLabel(self.tab_roadmap, text="MISI PENAKLUKAN WEBSITE", font=("Roboto", 24, "bold"), text_color="#00cc66")
        lbl_title.pack(pady=(30, 5))
        
        lbl_sub = ctk.CTkLabel(self.tab_roadmap, text="Langkah demi langkah menuju akses penuh (Beginner-Nitro Guide)", font=("Roboto", 13), text_color="#555555")
        lbl_sub.pack(pady=(0, 20))
        
        self.roadmap_checks = []
        roadmap_frame = ctk.CTkFrame(self.tab_roadmap, fg_color="#0a0a0a", border_width=1, border_color="#222222")
        roadmap_frame.pack(fill="both", expand=True, padx=80, pady=20)
        
        # * Daftar checklist (Berdasarkan GuidedAssistant v5.4)
        missions = [
            ("1. Information Gathering (!recon)", "Stalking IP, DNS, Whois, dan Server Info buat nyari titik lemah target."),
            ("2. Infrastructure Scan (!nmap)", "Cari pintu (Port) mana aja yang kebuka di server musuh biar bisa masuk."),
            ("3. Subdomain Discovery (!subdomain)", "Buru subdomain rahasia (dev, test, staging) yang sering dilupain admin."),
            ("4. Vulnerability Audit (!webaudit / !vuln)", "Audit celah SQLi, XSS, dan Host Injection di level aplikasi web."),
            ("5. API & Cloud Hunting (!api / !cloud)", "Bongkar urat nadi data di API endpoint dan storage awan (S3 Bucket)."),
            ("6. Stress Testing (!stress)", "Uji ketahanan akhir dengan tsunami request buat bikin server megap-megap.")
        ]
        
        for i, (m, desc) in enumerate(missions):
            cb = ctk.CTkCheckBox(roadmap_frame, text=m, font=("Roboto", 15, "bold"), text_color="#00ff00", fg_color="#00cc66", hover_color="#00aa55", border_color="#333333")
            cb.pack(anchor="w", padx=40, pady=(20, 2))
            
            lbl_desc = ctk.CTkLabel(roadmap_frame, text=desc, font=("Roboto", 12), text_color="#666666", wraplength=500, justify="left")
            lbl_desc.pack(anchor="w", padx=75, pady=(0, 10))
            
            self.roadmap_checks.append(cb)

    # * Tandai misi selesai dari luar (Auto-Checkbox v5.0)
    def update_roadmap_check(self, step_idx):
        if 0 <= step_idx < len(self.roadmap_checks):
            self.roadmap_checks[step_idx].select()

    # * Reset semua misi pas ganti target (!exit)
    def reset_roadmap(self):
        for cb in self.roadmap_checks:
            cb.deselect()


    def _show_how_to(self, tool_name):
        self.tabview.set("How to Use")
        for widget in self.tab_tutorial.winfo_children():
            widget.destroy()
            
        info = self.core.guided.helpDatabase.get(tool_name, "No data.")
        lbl_title = ctk.CTkLabel(self.tab_tutorial, text=f"DOCS: {tool_name.upper()}", font=("Roboto", 20, "bold"), text_color="cyan")
        lbl_title.pack(pady=20)
        
        txt_body = ctk.CTkTextbox(self.tab_tutorial, font=("Roboto", 13), wrap="word", fg_color="transparent")
        txt_body.pack(fill="both", expand=True, padx=40, pady=10)
        txt_body.insert("end", f"{info}\n\n")
        txt_body.insert("end", f"TO RUN:\nType '!{tool_name}' in the Terminal.\nType '!exit' to close the module.")
        txt_body.configure(state="disabled")

    def _on_close(self):
        self.core.exitFramework()
        self.destroy()
