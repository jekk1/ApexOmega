import customtkinter as ctk
import threading
from tkinter import messagebox
import ctypes
import os
import sys
import shutil
import secrets

# * Set AppID buat Taskbar Icon Sync v5.8.15
try:
    myappid = 'zaqi.apexomega.terminal.v5'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

# * Tema Shell Mode (Zaqi Interactive Edition v5.9)
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class InterfaceDesktop(ctk.CTk):
    def __init__(self, app_core):
        super().__init__()
        self.core = app_core
        self.title(f"ApexOmega Shell v{self.core.VERSION} (Script Section Edition)")
        self.geometry("1100x700")
        
        # * Standard Resizable Window
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.98)
        
        self.tools_visible = True
        self.waitingTarget = True
        self.dragging_script = None
        self._setup_ui()
        
        # * Auto-Prompt Target on Startup
        self.after(500, self._initial_prompt)
        self._populate_tools()
        self.tools_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # * Set Window Icon v5.8.11 (Taskbar Sync)
        self.after(200, self._set_window_icon)
        self._create_shortcuts()

    def _create_shortcuts(self):
        try:
            import os, sys, subprocess, secrets
            desktop = os.path.join(os.environ.get("USERPROFILE"), "Desktop")
            start_menu = os.path.join(os.environ.get("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs")
            
            shortcut_name = "ApexOmega.lnk"
            
            targets = [
                os.path.join(desktop, shortcut_name),
                os.path.join(start_menu, shortcut_name)
            ]

            target_exe = sys.executable
            work_dir = os.path.dirname(sys.executable)
            
            # * Find Permanent Icon Path v5.8.16 (APPDATA Sync)
            appdata_pongo = os.path.join(os.environ.get("APPDATA"), "ApexOmega")
            if not os.path.exists(appdata_pongo):
                os.makedirs(appdata_pongo, exist_ok=True)
                
            icon_perm = os.path.join(appdata_pongo, "app_icon.ico")
            
            if getattr(sys, 'frozen', False):
                icon_src = os.path.join(sys._MEIPASS, 'app_icon.ico')
            else:
                icon_src = 'app_icon.ico'
                
            if os.path.exists(icon_src) and not os.path.exists(icon_perm):
                shutil.copy2(icon_src, icon_perm)

            for shortcut_path in targets:
                if os.path.exists(shortcut_path): continue
                
                vbs_code = f"""
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{shortcut_path}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "{target_exe}"
oLink.WorkingDirectory = "{work_dir}"
oLink.IconLocation = "{icon_perm},0"
oLink.Description = "Apex Omega Pentest Framework"
oLink.Save
"""
                vbs_path = os.path.join(os.environ.get("TEMP"), f"ao_short_{secrets.token_hex(2)}.vbs")
                with open(vbs_path, "w") as f:
                    f.write(vbs_code)
                
                subprocess.run(["cscript", "//nologo", vbs_path], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0)
                os.remove(vbs_path)
            
            self.log_to_terminal("[+] Shortcuts (ApexOmega) created on Desktop & Start Menu.\n", "[info] ")
        except Exception:
            pass

    def _set_window_icon(self):
        try:
            icon_perm = os.path.join(os.environ.get("APPDATA"), "ApexOmega", "app_icon.ico")
            if os.path.exists(icon_perm):
                icon_path = icon_perm
            elif getattr(sys, 'frozen', False):
                icon_path = os.path.join(sys._MEIPASS, 'app_icon.ico')
            else:
                icon_path = os.path.abspath('app_icon.ico')
            
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
                try:
                    from PIL import Image, ImageTk
                    img = Image.open(icon_path)
                    self.iconphoto(True, ImageTk.PhotoImage(img))
                except Exception:
                    pass
        except Exception:
            pass

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

        self.credit_label = ctk.CTkLabel(self.sidebar, text="By Zaqi", font=("Roboto", 11, "italic"), text_color="dim gray")
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
        self.tab_scripts = self.tabview.add("Scripts")
        
        # * Populate Tabs
        self._setup_roadmap_tab()
        self._setup_scripts_tab()

        # * Terminal
        self.terminal = ctk.CTkTextbox(self.tab_console, font=("Consolas", 13), text_color="#cccccc", border_width=0, border_spacing=20, fg_color="#050505")
        self.terminal.pack(fill="both", expand=True)
        self._tw = self.terminal._textbox
        
        # * Tag warna untuk output
        self._tw.tag_config("sysText", foreground="#666666")
        self._tw.tag_config("dimText", foreground="#333333")
        self._tw.tag_config("prompt", foreground="#555555")
        self._tw.tag_config("inspect", foreground="#888888")
        self._tw.tag_config("success", foreground="#00ff00")
        self._tw.tag_config("greenText", foreground="#00ff00")
        self._tw.tag_config("error", foreground="#ff3333")
        self._tw.tag_config("danger", foreground="#ff3333")
        self._tw.tag_config("warning", foreground="#ffcc00")
        self._tw.tag_config("info", foreground="#5dade2")
        self._tw.tag_config("cyanText", foreground="#00ffff")
        self._tw.tag_config("init", foreground="#aaaaaa")
        self._tw.tag_config("gen", foreground="#bb86fc")
        
        # * Bind event untuk proteksi
        self._tw.bind("<Control-c>", lambda e: self.core.stop_running_tool())
        
        lbl_info = ctk.CTkLabel(self.tab_console, text="[!] CTRL+C TO STOP | !EXIT TO ROOT | !HELP FOR MANUAL", font=("Roboto", 10), text_color="#444444")
        lbl_info.pack(side="bottom", pady=5)
        self._tw.bind("<Key>", self._on_key)
        self._tw.bind("<Button-1>", self._on_click)
        self._tw.bind("<Return>", self._on_enter, add=False)
        self._tw.bind("<BackSpace>", self._on_backspace)
        self._tw.bind("<Delete>", self._on_delete)
        self._tw.bind("<<Cut>>", self._block_cut)
        self._tw.bind("<Control-a>", self._block_select_all)
        
        # * Global Panic Stop (v5.8.10)
        self.bind_all("<Escape>", self._on_panic_stop)
        
        self._tw.insert("end", f"ApexOmega Console [Version: {self.core.VERSION}]\n", "dimText")
        self._tw.insert("end", "Titanium Absolute (Global DLL & Tcl Lock)\n\n", "dimText")
        
        self._tw.mark_set("inputStart", "end-1c")
        self._tw.mark_gravity("inputStart", "left")

        # * --- Setup Tab Found ---
        self.found_box = ctk.CTkTextbox(self.tab_found, font=("Consolas", 13), text_color="#00ff00", fg_color="#050505", border_width=0, border_spacing=20)
        self.found_box.pack(fill="both", expand=True)
        self.found_box.insert("end", "[*] HARTA KARUN SYSTEM (v5.9)\n", "success")
        self.found_box.insert("end", "[*] Hasil scouting penting bakal dicatet di sini otomatis.\n", "dimText")
        self.found_box.insert("end", "-"*50 + "\n\n")
        self.found_box.configure(state="disabled")

    # * ========== SCRIPTS TAB (v5.9 New) ==========

    # * Setup halaman Scripts dengan kategori, search, preview, dan drag-drop
    def _setup_scripts_tab(self):
        for widget in self.tab_scripts.winfo_children():
            widget.destroy()
        
        # -- Header --
        header_frame = ctk.CTkFrame(self.tab_scripts, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(15, 5))
        
        lbl_title = ctk.CTkLabel(header_frame, text="SCRIPT LIBRARY v5.9", font=("Roboto", 20, "bold"), text_color="#00ffff")
        lbl_title.pack(side="left")
        
        lbl_hint = ctk.CTkLabel(header_frame, text="Click = Preview | Double-Click = Send to Terminal", font=("Roboto", 11), text_color="#555555")
        lbl_hint.pack(side="right")
        
        # -- Search Bar --
        search_frame = ctk.CTkFrame(self.tab_scripts, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=5)
        
        self.script_search_var = ctk.StringVar()
        self.script_search_var.trace_add("write", self._on_script_search)
        
        search_entry = ctk.CTkEntry(search_frame, textvariable=self.script_search_var, placeholder_text="Search scripts...", font=("Consolas", 13), fg_color="#111111", border_color="#333333", height=35)
        search_entry.pack(fill="x")
        
        # -- Main Split: Script List (top) + Preview (bottom) --
        paned_frame = ctk.CTkFrame(self.tab_scripts, fg_color="transparent")
        paned_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        # Script List (scrollable)
        self.script_list_frame = ctk.CTkScrollableFrame(paned_frame, fg_color="#080808", border_width=1, border_color="#222222")
        self.script_list_frame.pack(fill="both", expand=True, pady=(0, 5))
        
        # Preview Pane
        preview_container = ctk.CTkFrame(paned_frame, fg_color="#080808", border_width=1, border_color="#222222", height=180)
        preview_container.pack(fill="x", pady=(5, 0))
        preview_container.pack_propagate(False)
        
        preview_header = ctk.CTkFrame(preview_container, fg_color="transparent")
        preview_header.pack(fill="x", padx=10, pady=(8, 2))
        
        self.preview_title = ctk.CTkLabel(preview_header, text="PREVIEW", font=("Roboto", 12, "bold"), text_color="#555555")
        self.preview_title.pack(side="left")
        
        self.btn_send_to_terminal = ctk.CTkButton(preview_header, text="SEND TO TERMINAL", font=("Roboto", 11, "bold"), fg_color="#1a3a1a", text_color="#00ff00", hover_color="#2a4a2a", height=28, width=160, command=self._send_preview_to_terminal)
        self.btn_send_to_terminal.pack(side="right")
        
        self.preview_box = ctk.CTkTextbox(preview_container, font=("Consolas", 12), text_color="#00ff00", fg_color="#050505", border_width=0, wrap="word")
        self.preview_box.pack(fill="both", expand=True, padx=5, pady=(0, 5))
        
        self.current_preview_code = ""
        
        # Populate scripts
        self._populate_script_list()

    # * Buat daftar script per kategori di script list
    def _populate_script_list(self, filterQuery=""):
        for widget in self.script_list_frame.winfo_children():
            widget.destroy()
        
        categories = self.core.script_lib.getCategories()
        
        for cat in categories:
            scripts = self.core.script_lib.getScripts(cat)
            
            # Filter berdasarkan search query
            if filterQuery:
                scripts = [s for s in scripts if filterQuery in s["name"].lower() or filterQuery in s["description"].lower() or filterQuery in s["category"].lower()]
            
            if not scripts:
                continue
            
            # -- Category Header --
            cat_frame = ctk.CTkFrame(self.script_list_frame, fg_color="transparent")
            cat_frame.pack(fill="x", pady=(10, 2))
            
            lbl_cat = ctk.CTkLabel(cat_frame, text=f"-- {cat.upper()} --", font=("Roboto", 11, "bold"), text_color="#444444")
            lbl_cat.pack(anchor="w", padx=10)
            
            # -- Script Items --
            for script in scripts:
                self._create_script_item(script)

    # * Buat satu item script yang bisa diklik dan di-drag
    def _create_script_item(self, script):
        risk_colors = {
            "Critical": "#ff3333",
            "High": "#ffcc00",
            "Medium": "#5dade2",
            "Low": "#666666"
        }
        risk_color = risk_colors.get(script["risk"], "#666666")
        
        item_frame = ctk.CTkFrame(self.script_list_frame, fg_color="#0d0d0d", corner_radius=4, height=36)
        item_frame.pack(fill="x", padx=5, pady=1)
        item_frame.pack_propagate(False)
        
        # Risk indicator
        risk_lbl = ctk.CTkLabel(item_frame, text=f"[{script['risk'][:1]}]", font=("Consolas", 11), text_color=risk_color, width=30)
        risk_lbl.pack(side="left", padx=(8, 2))
        
        # Script name (clickable)
        name_lbl = ctk.CTkLabel(item_frame, text=script["name"], font=("Consolas", 12), text_color="#cccccc", anchor="w", cursor="hand2")
        name_lbl.pack(side="left", fill="x", expand=True, padx=5)
        
        # Category tag
        cat_lbl = ctk.CTkLabel(item_frame, text=script["category"], font=("Roboto", 10), text_color="#333333", width=80)
        cat_lbl.pack(side="right", padx=8)
        
        # Send button
        send_btn = ctk.CTkButton(item_frame, text=">>", font=("Consolas", 11, "bold"), fg_color="transparent", text_color="#00ff00", hover_color="#1a3a1a", width=30, height=24, command=lambda s=script: self._send_script_to_terminal(s))
        send_btn.pack(side="right", padx=2)
        
        # Bind events
        name_lbl.bind("<Button-1>", lambda e, s=script: self._preview_script(s))
        name_lbl.bind("<Double-Button-1>", lambda e, s=script: self._send_script_to_terminal(s))
        
        # Drag-and-drop bindings
        name_lbl.bind("<ButtonPress-1>", lambda e, s=script: self._on_drag_start(e, s))
        name_lbl.bind("<B1-Motion>", self._on_drag_motion)
        name_lbl.bind("<ButtonRelease-1>", self._on_drag_release)
        
        # Hover effect
        def on_enter(e, f=item_frame):
            f.configure(fg_color="#1a1a1a")
        def on_leave(e, f=item_frame):
            f.configure(fg_color="#0d0d0d")
        
        item_frame.bind("<Enter>", on_enter)
        item_frame.bind("<Leave>", on_leave)
        name_lbl.bind("<Enter>", on_enter)
        name_lbl.bind("<Leave>", on_leave)

    # * Preview script di preview pane
    def _preview_script(self, script):
        self.current_preview_code = script["code"]
        self.preview_title.configure(text=f"PREVIEW: {script['name']} [{script['risk']}]")
        
        self.preview_box.configure(state="normal")
        self.preview_box.delete("1.0", "end")
        self.preview_box.insert("end", f"// {script['description']}\n\n", "dimText")
        self.preview_box.insert("end", script["code"])

    # * Kirim code dari preview pane ke terminal
    def _send_preview_to_terminal(self):
        if self.current_preview_code:
            self._insert_to_terminal(self.current_preview_code)

    # * Kirim script langsung ke terminal
    def _send_script_to_terminal(self, script):
        self._preview_script(script)
        self._insert_to_terminal(script["code"])

    # * Insert text ke terminal input area
    def _insert_to_terminal(self, code):
        self.tabview.set("Terminal")
        # Insert di posisi input saat ini
        self._tw.insert("end", code)
        self._tw.see("end")

    # * Drag-and-drop handlers
    def _on_drag_start(self, event, script):
        self.dragging_script = script
        self._drag_label = ctk.CTkLabel(self, text=f"[{script['name']}]", font=("Consolas", 11), text_color="#00ff00", fg_color="#1a1a1a", corner_radius=4)

    def _on_drag_motion(self, event):
        if self.dragging_script and hasattr(self, '_drag_label'):
            try:
                x = event.x_root - self.winfo_rootx()
                y = event.y_root - self.winfo_rooty()
                self._drag_label.place(x=x + 10, y=y + 10)
            except Exception:
                pass

    def _on_drag_release(self, event):
        if self.dragging_script and hasattr(self, '_drag_label'):
            try:
                self._drag_label.destroy()
            except Exception:
                pass
            
            # Cek apakah drop di area terminal
            try:
                x = event.x_root - self.winfo_rootx()
                y = event.y_root - self.winfo_rooty()
                
                # Area terminal detection
                tw_x = self.terminal.winfo_rootx() - self.winfo_rootx()
                tw_y = self.terminal.winfo_rooty() - self.winfo_rooty()
                tw_w = self.terminal.winfo_width()
                tw_h = self.terminal.winfo_height()
                
                if tw_x <= x <= tw_x + tw_w and tw_y <= y <= tw_y + tw_h:
                    self._insert_to_terminal(self.dragging_script["code"])
            except Exception:
                pass
            
            self.dragging_script = None

    # * Search handler
    def _on_script_search(self, *args):
        query = self.script_search_var.get().lower().strip()
        self._populate_script_list(filterQuery=query)

    # * ========== END SCRIPTS TAB ==========

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

    # * Magnet Kursor
    def _on_click(self, event):
        self.after(10, lambda: self._tw.mark_set("insert", "end-1c"))

    # * Blokir ketikan di area protected
    def _on_key(self, event):
        if event.keysym in ("Return", "BackSpace", "Delete", "Left", "Right", "Up", "Down", "Home", "End"):
            self._tw.mark_set("insert", "end-1c")
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

    # * Blokir select all
    def _block_select_all(self, event):
        markPos = self._tw.index("inputStart")
        self._tw.tag_remove("sel", "1.0", "end")
        self._tw.tag_add("sel", markPos, "end-1c")
        return "break"

    # * Handle Enter
    def _on_enter(self, event):
        try:
            last_line = self._tw.get("end-2l", "end-1c")
            userInput = ""
            if ">>" in last_line:
                userInput = last_line.split(">>")[-1].strip()
            
            if not userInput:
                markPos = self._tw.index("inputStart")
                userInput = self._tw.get(markPos, "end-1c").strip()

            if not userInput or any(p in userInput for p in ["[*]", "[!]", "[+]", "[-]"]):
                return "break"
                
            is_new_target = not userInput.startswith("!") and not (" " in userInput or len(userInput) > 100)
            if is_new_target:
                self.core.set_active_target(userInput)

            self._tw.insert("end", "\n")
            target_display = self.core.active_target or "none"
            prompt_header = f"[root@shell:{target_display}] >> "
            self._tw.insert("end", prompt_header, "prompt")
            self._tw.mark_set("inputStart", "end-1c")
            self._tw.mark_gravity("inputStart", "left")
            self._tw.mark_set("insert", "end-1c")
            self._tw.see("end")

            if userInput.startswith("!"):
                self.core.execute_shell_command(userInput)
            else:
                target = userInput
                if " " in target or len(target) > 100: return "break"
                
                self._append_system(f"\n[*] New Target Set: {target}\n", "cyanText")
                def recon_start():
                    self.core._run_recon_module([])
                    self.show_prompt()
                threading.Thread(target=recon_start, daemon=True).start()

        except Exception as e:
            self.log_to_terminal(f"\n[!] UI Logic Error: {str(e)}\n", "error")
        
        return "break"

    # * Global Panic Stop Handler
    def _on_panic_stop(self, event=None):
        self.log_to_terminal("\n[!] PANIC STOP: ESCAPE KEY PRESSED! Cleaning up...\n", "danger")
        self.core.stop_running_tool()
        return "break"

    # * Tampilkan prompt baru
    def show_prompt(self):
        def _exec():
            target = self.core.active_target or "none"
            self._append_system(f"\n[root@shell:{target}] >> ", "prompt")
            self._set_input_mark()
        self.after(0, _exec)

    # * Log output ke terminal
    def log_to_terminal(self, message, tag="sysText"):
        def _exec():
            if message.startswith("\r"):
                self._tw.delete("end-1c linestart", "end-1c")
                clean_msg = message.replace("\r", "")
            else:
                clean_msg = message
                
            clean_tag = tag.replace("[", "").replace("]", "").strip()
            self._tw.insert("end", clean_msg, clean_tag)
            self._tw.see("end")
            self._set_input_mark()
        self.after(0, _exec)

    # * Log ke tab Found
    def log_to_found(self, message):
        def _exec():
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
        for widget in self.tools_frame.winfo_children():
            widget.destroy()
        
        categories = {
            "RECON / INFO": ["nmap", "recon", "webaudit", "headers", "cookie"],
            "DISCOVERY": ["subdomain", "vhost", "webports", "dirb", "git"],
            "VULNERABILITY": ["vuln", "wp", "form"],
            "API / CLOUD": ["api", "cloud"],
            "EXPLOITATION": ["payload", "stress"],
            "UTILITY": ["help", "script"]
        }
        
        for cat, tools in categories.items():
            lbl = ctk.CTkLabel(self.tools_frame, text=cat, font=("Roboto", 11, "bold"), text_color="#444444", anchor="w")
            lbl.pack(fill="x", pady=(10, 2), padx=5)
            
            for t in sorted(tools):
                btn = ctk.CTkButton(self.tools_frame, text=t.upper(), anchor="w", fg_color="transparent", text_color="#777777", hover_color="#1a1a1a", height=28, command=lambda x=t: self._show_how_to(x))
                btn.pack(fill="x", pady=0)

    # * Setup Roadmap Tab v5.9 (8 Misi)
    def _setup_roadmap_tab(self):
        for widget in self.tab_roadmap.winfo_children():
            widget.destroy()

        lbl_title = ctk.CTkLabel(self.tab_roadmap, text="MISI PENAKLUKAN WEBSITE", font=("Roboto", 24, "bold"), text_color="#00cc66")
        lbl_title.pack(pady=(30, 5))
        
        lbl_sub = ctk.CTkLabel(self.tab_roadmap, text="8 Langkah menuju akses penuh (v5.9 Detailed Guide)", font=("Roboto", 13), text_color="#555555")
        lbl_sub.pack(pady=(0, 20))
        
        self.roadmap_checks = []
        roadmap_frame = ctk.CTkScrollableFrame(self.tab_roadmap, fg_color="#0a0a0a", border_width=1, border_color="#222222")
        roadmap_frame.pack(fill="both", expand=True, padx=80, pady=20)
        
        # * 8 Misi Detail
        missions = [
            ("1. Reconnaissance (!recon)", "Stalking IP, DNS, WHOIS, Tech Detection. Mode: !recon quick | deep | full"),
            ("2. Infrastructure Scan (!nmap)", "Port scanning: !nmap (default 10 ports) atau !nmap 80,443,3306 (custom)"),
            ("3. Discovery (!subdomain / !dirb)", "Subdomain brute/passive dan directory bruteforce common/deep"),
            ("4. Web Analysis (!headers / !cookie / !form / !git)", "Audit security headers, cookie flags, form inputs, dan .git exposure"),
            ("5. Vulnerability Scan (!vuln)", "CORS, SSTI, CRLF, Host Injection, Upload, 100+ Path Fuzzing"),
            ("6. API & Cloud (!api / !cloud)", "Endpoint fuzzing, method check, S3/Firebase/GCS bucket hunting"),
            ("7. CMS Audit (!wp)", "WP version, plugins, users, vulnerable files: !wp all"),
            ("8. Stress Testing (!stress)", "Load test: !stress <threads> <duration>. Duration 0 = infinite")
        ]
        
        for i, (m, desc) in enumerate(missions):
            cb = ctk.CTkCheckBox(roadmap_frame, text=m, font=("Roboto", 15, "bold"), text_color="#00ff00", fg_color="#00cc66", hover_color="#00aa55", border_color="#333333")
            cb.pack(anchor="w", padx=40, pady=(20, 2))
            
            lbl_desc = ctk.CTkLabel(roadmap_frame, text=desc, font=("Roboto", 12), text_color="#666666", wraplength=500, justify="left")
            lbl_desc.pack(anchor="w", padx=75, pady=(0, 10))
            
            self.roadmap_checks.append(cb)

    # * Tandai misi selesai
    def update_roadmap_check(self, step_idx):
        if 0 <= step_idx < len(self.roadmap_checks):
            self.roadmap_checks[step_idx].select()

    # * Reset semua misi pas ganti target
    def reset_roadmap(self):
        for cb in self.roadmap_checks:
            cb.deselect()

    # * Show How to Use (v5.9 with Usage Syntax)
    def _show_how_to(self, tool_name):
        self.tabview.set("How to Use")
        for widget in self.tab_tutorial.winfo_children():
            widget.destroy()
        
        info = self.core.guided.helpDatabase.get(tool_name, "No data available.")
        usage = self.core.guided.getUsage(tool_name)
        
        # -- Title --
        lbl_title = ctk.CTkLabel(self.tab_tutorial, text=f"DOCS: {tool_name.upper()}", font=("Roboto", 20, "bold"), text_color="cyan")
        lbl_title.pack(pady=(20, 10))
        
        # -- Content Area --
        txt_body = ctk.CTkTextbox(self.tab_tutorial, font=("Consolas", 13), wrap="word", fg_color="transparent")
        txt_body.pack(fill="both", expand=True, padx=40, pady=10)
        
        tw = txt_body._textbox
        tw.tag_config("header", foreground="#00ffff", font=("Roboto", 14, "bold"))
        tw.tag_config("syntax", foreground="#00ff00", font=("Consolas", 14, "bold"))
        tw.tag_config("mode", foreground="#ffcc00")
        tw.tag_config("example", foreground="#5dade2")
        tw.tag_config("desc", foreground="#cccccc")
        tw.tag_config("dim", foreground="#666666")
        
        # Usage section
        if usage:
            tw.insert("end", "SYNTAX\n", "header")
            tw.insert("end", f"  {usage['syntax']}\n\n", "syntax")
            
            tw.insert("end", "MODES / ARGUMENTS\n", "header")
            for m, desc in usage['modes'].items():
                tw.insert("end", f"  {m:20}", "mode")
                tw.insert("end", f" - {desc}\n", "desc")
            
            tw.insert("end", "\nEXAMPLES\n", "header")
            for ex in usage['examples']:
                tw.insert("end", f"  $ {ex}\n", "example")
            
            tw.insert("end", "\n")
        
        # Description
        tw.insert("end", "DESCRIPTION\n", "header")
        tw.insert("end", f"  {info}\n\n", "desc")
        
        tw.insert("end", "QUICK START\n", "header")
        tw.insert("end", f"  Type '!{tool_name}' in the Terminal.\n", "dim")
        tw.insert("end", "  Type '!exit' to close the module.\n", "dim")
        tw.insert("end", "  Type '!help' for all commands.\n", "dim")
        
        txt_body.configure(state="disabled")

    def _on_close(self):
        self.core.exitFramework()
        self.destroy()
