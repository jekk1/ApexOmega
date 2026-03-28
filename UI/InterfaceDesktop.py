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
        self.title("ApexOmega Shell v4.6")
        self.geometry("1100x700")
        
        # * Standard Resizable Window
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.98)
        
        self.tools_visible = False
        self.waitingTarget = True
        self._setup_ui()
        
        # * Auto-Prompt Target on Startup
        self.after(500, self._initial_prompt)

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
        
        self.tab_console = self.tabview.add("Zaqi Shell")
        self.tab_tutorial = self.tabview.add("How to Use")

        # * Akses internal textbox dari CTkTextbox buat kontrol granular
        self.terminal = ctk.CTkTextbox(self.tab_console, font=("Consolas", 13), text_color="#cccccc", border_width=0, border_spacing=20, fg_color="#050505")
        self.terminal.pack(fill="both", expand=True)
        self._tw = self.terminal._textbox
        
        # * Tag warna untuk output system (Gray for system, Green for results)
        self._tw.tag_config("sysText", foreground="#555555")
        self._tw.tag_config("dimText", foreground="#333333")
        self._tw.tag_config("cyanText", foreground="#00cc66")
        self._tw.tag_config("greenText", foreground="#00cc66")
        self._tw.tag_config("prompt", foreground="#444444")
        
        # * Bind event untuk proteksi teks dan handle input
        self._tw.bind("<Return>", self._on_enter)
        self._tw.bind("<Key>", self._on_key)
        self._tw.bind("<BackSpace>", self._on_backspace)
        self._tw.bind("<Delete>", self._on_delete)
        self._tw.bind("<<Cut>>", self._block_cut)
        self._tw.bind("<Control-a>", self._block_select_all)
        
        # * Startup header
        self._tw.insert("end", "ApexOmega Console [Version: 4.6]\n", "dimText")
        self._tw.insert("end", "Zaqi Interactive Shell Edition\n\n", "dimText")
        
        # * Mark posisi awal input (semua sebelumnya protected)
        self._tw.mark_set("inputStart", "end-1c")
        self._tw.mark_gravity("inputStart", "left")

    # * Prompt awal minta target
    def _initial_prompt(self):
        self._append_system("[root@shell] ENTER TARGET IP/URL >> ", "prompt")
        self._set_input_mark()

    # * Tulis teks system yang terproteksi
    def _append_system(self, text, tag="sysText"):
        self._tw.insert("end", text, tag)
        self._tw.see("end")

    # * Set input mark setelah output baru
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
        markPos = self._tw.index("inputStart")
        userInput = self._tw.get(markPos, "end-1c").strip()
        
        # * Tambah newline setelah input
        self._tw.insert("end", "\n")
        
        if not userInput:
            self._append_prompt()
            return "break"
        
        # * Mode target input
        if self.waitingTarget:
            self.waitingTarget = False
            target = userInput
            self.core.set_active_target(target)
            
            self._append_system(f"\n[root@shell] [INITIATING AUTOMATED RECON ON: {target}]\n", "cyanText")
            self._append_system("[*] Checking connectivity... CONNECTED\n", "sysText")
            self._append_system("[*] Resolving DNS infrastructure...\n", "sysText")
            
            # -- Quick real recon --
            def quick_recon():
                try:
                    records = self.core.net.getDnsInfo(target)
                    ip = records.get('IP', 'Unknown')
                    self._append_system(f"[+] PRIMARY IP: {ip}\n", "greenText")
                    
                    tech = self.core.web.detectTech(f"http://{target}" if not target.startswith("http") else target)
                    server = tech.get('server', ['Unknown'])[0]
                    self._append_system(f"[+] SERVER TECH: {server}\n", "greenText")
                except Exception:
                    self._append_system("[-] Recon limited (target specific restriction)\n", "dimText")
                
                self._append_system(f"\n[root@shell] TARGET LOCKED: {target}\n", "greenText")
                self._append_system("[root@shell] Commands: !nmap, !webaudit, !wordpress, !chaos, !help, !exit\n\n", "cyanText")
                self._append_prompt()

            threading.Thread(target=quick_recon, daemon=True).start()
            return "break"
        
        # * Mode command
        if userInput.startswith("!"):
            self.core.execute_shell_command(userInput)
        else:
            # * Cek apakah user mau ganti target
            self.core.set_active_target(userInput)
            self._append_system(f"[root@shell] TARGET CHANGED: {userInput}\n", "greenText")
        
        self._append_prompt()
        return "break"

    # * Tampilkan prompt baru dan set input mark
    def _append_prompt(self):
        target = self.core.active_target or "none"
        self._append_system(f"[root@shell:{target}] >> ", "prompt")
        self._set_input_mark()

    # * Log output ke terminal (dipanggil dari luar class)
    def log_to_terminal(self, message, prefix="[root@shell] "):
        self._append_system(f"{prefix}{message}\n", "sysText")
        self._set_input_mark()

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
        
        tools = self.core.guided.helpDatabase.keys()
        for t in sorted(tools):
            btn = ctk.CTkButton(self.tools_frame, text=t.upper(), anchor="w", fg_color="transparent", text_color="#777777", hover_color="#1a1a1a", height=30, command=lambda x=t: self._show_how_to(x))
            btn.pack(fill="x", pady=1)

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
        txt_body.insert("end", f"TO RUN:\nType '!{tool_name}' in the Zaqi Shell.\nType '!exit' to close the module.")
        txt_body.configure(state="disabled")

    def _on_close(self):
        self.core.exitFramework()
        self.destroy()
