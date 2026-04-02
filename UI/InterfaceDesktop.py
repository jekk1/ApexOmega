import customtkinter as ctk
import tkinter as tk
import threading
from tkinter import messagebox
import os
import sys
import subprocess
import time
import shutil
import tempfile
import ctypes
from ctypes import wintypes
import secrets

# * Set AppID buat Taskbar Icon Sync v5.8.15
try:
    myappid = 'zaqi.apexomega.terminal.v5'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

# * Tema Shell Mode (Zaqi Interactive Edition v5.9)
try:
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
except Exception as e:
    print(f"Warning: Failed to load CTK theme: {e}")

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
        self.hacker_mode = False
        self._setup_ui()
        
        # * Auto-Prompt Target on Startup is now handled by _create_shortcuts
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

            # * Clean up old shortcut v5.9
            old_shortcut_name = "apexomega.exe.lnk"
            old_targets = [
                os.path.join(desktop, old_shortcut_name),
                os.path.join(start_menu, old_shortcut_name)
            ]
            for old_p in old_targets:
                if os.path.exists(old_p):
                    try: os.remove(old_p)
                    except: pass

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
                # * Force update shortcut v5.9
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
            
            self.log_to_terminal("\n[+] Shortcuts (ApexOmega) updated on Desktop & Start Menu.\n", "[info] ")
            self.after(0, self._initial_prompt)
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

        # * --- Mode Selector (Top Bar) ---
        self.mode_frame = ctk.CTkFrame(self.content_area, fg_color="#1a1a1a", height=50, corner_radius=5)
        self.mode_frame.pack(fill="x", padx=5, pady=5)
        
        self.mode_label = ctk.CTkLabel(self.mode_frame, text="MODE:", font=("Roboto", 12, "bold"), text_color="#888888")
        self.mode_label.pack(side="left", padx=10, pady=10)
        
        self.mode_var = tk.StringVar(value="WEB")
        self.mode_web = ctk.CTkRadioButton(self.mode_frame, text="WEB HACKING", variable=self.mode_var, value="WEB", 
                                           font=("Roboto", 11, "bold"), command=self._on_mode_change)
        self.mode_web.pack(side="left", padx=5, pady=10)
        
        self.mode_wifi = ctk.CTkRadioButton(self.mode_frame, text="WIFI HACKING", variable=self.mode_var, value="WIFI", 
                                            font=("Roboto", 11, "bold"), command=self._on_mode_change)
        self.mode_wifi.pack(side="left", padx=5, pady=10)

        self.mode_status = ctk.CTkLabel(self.mode_frame, text="● WEB", font=("Roboto", 11, "bold"), text_color="#00ff00")
        self.mode_status.pack(side="right", padx=10, pady=10)
        
        # Mode indicator icon next to status
        self.mode_icon = ctk.CTkLabel(self.mode_frame, text="📡", font=("Roboto", 14), text_color="#00ff00")
        self.mode_icon.pack(side="right", padx=5, pady=10)

        self.tabview = ctk.CTkTabview(self.content_area, border_width=1, border_color="#222222", fg_color="#050505")
        self.tabview.pack(fill="both", expand=True)

        # * Tab Order: Terminal, Found, Decoder, Roadmap, Scripts, How to Use
        self.tab_console = self.tabview.add("Terminal")
        self.tab_found = self.tabview.add("Found")
        self.tab_decoder = self.tabview.add("Decoder")
        self.tab_roadmap = self.tabview.add("Roadmap")
        self.tab_scripts = self.tabview.add("Scripts")
        self.tab_tutorial = self.tabview.add("How to Use")

        # * Populate Tabs
        self._setup_roadmap_tab()
        self._setup_scripts_tab()
        self._setup_decoder_tab()

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
        self._tw.tag_config("errorText", foreground="#ff3333")
        self._tw.tag_config("danger", foreground="#ff3333")
        self._tw.tag_config("warning", foreground="#ffcc00")
        self._tw.tag_config("info", foreground="#5dade2")
        self._tw.tag_config("blueText", foreground="#3b82f6")
        self._tw.tag_config("cyanText", foreground="#00ffff")
        self._tw.tag_config("init", foreground="#aaaaaa")
        self._tw.tag_config("gen", foreground="#bb86fc")
        
        # * --- Terminal Text (Dynamic Banner v5.9.6) ---
        self._tw.insert("end", f"ApexOmega Console [Version: {self.core.VERSION}]\n", "dimText")
        self._tw.insert("end", "Titanium Absolute (Global DLL & Tcl Lock)\n\n", "dimText")
        
        # * Setup Terminal Input Controls
        self._tw.mark_set("inputStart", "end-1c")
        self._tw.mark_gravity("inputStart", "left")
        self._tw.bind("<Key>", self._on_key)
        self._tw.bind("<Button-1>", self._on_click)
        self._tw.bind("<Return>", self._on_enter, add=False)
        self._tw.bind("<BackSpace>", self._on_backspace)
        self._tw.bind("<Delete>", self._on_delete)
        self._tw.bind("<<Cut>>", self._block_cut)
        self._tw.bind("<Control-a>", self._block_select_all)
        self._tw.bind("<Control-c>", lambda e: self.core.stop_running_tool())
        self._tw.bind("<Button-3>", self._on_right_click)
        
        # * Global Panic Stop (v5.8.10)
        self.bind_all("<Escape>", self._on_panic_stop)

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
        
        # (drag_handle dipindah ke kanan di baris 350+)
        # Risk indicator
        risk_lbl = ctk.CTkLabel(item_frame, text=f"[{script['risk'][:1]}]", font=("Consolas", 11), text_color=risk_color, width=30)
        risk_lbl.pack(side="left", padx=(5, 2))
        
        # Script name (clickable)
        name_lbl = ctk.CTkLabel(item_frame, text=script["name"], font=("Consolas", 12), text_color="#cccccc", anchor="w", cursor="hand2")
        name_lbl.pack(side="left", fill="x", expand=True, padx=5)
        
        # Category tag
        cat_lbl = ctk.CTkLabel(item_frame, text=script["category"], font=("Roboto", 10), text_color="#333333", width=80)
        cat_lbl.pack(side="right", padx=8)
        
        # * Tombol [>>] untuk kirim manual ke terminal
        send_btn = ctk.CTkButton(
            item_frame, text="[>>]", width=35, height=28, 
            fg_color="#1a1a1a", text_color="cyan", hover_color="#222",
            command=lambda: self._insert_to_terminal(script["code"])
        )
        send_btn.pack(side="right", padx=(2, 5))

        # * Tombol [GEN] untuk script generation manual (Zaqi req v6.3)
        gen_btn = ctk.CTkButton(
            item_frame, text="[GEN]", width=35, height=28,
            fg_color="#1a1a1a", text_color="#bb86fc", hover_color="#222",
            command=lambda: self._generate_script_file(script)
        )
        gen_btn.pack(side="right", padx=(2, 2))

        # * Drag Handle [✥] - Pindah ke Kanan (Hyper-Ergonomic v6.0.7)
        drag_handle = ctk.CTkLabel(item_frame, text="✥", font=("Roboto", 16), text_color="cyan", width=30, cursor="fleur")
        drag_handle.pack(side="right", padx=(0, 5))
        
        # * Bindings Drag Feedback
        drag_handle.bind("<ButtonPress-1>", lambda e, s=script: self._on_script_drag_start(e, s))
        drag_handle.bind("<B1-Motion>", self._on_script_ghost_move)
        drag_handle.bind("<ButtonRelease-1>", self._on_script_drag_end)
        
        # * --- Bind events - Preview Only v5.9.5 ---
        name_lbl.bind("<Button-1>", lambda e, s=script: self._preview_script(s))
        
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
        self._insert_to_terminal(script["code"])

    # * Insert text ke terminal input area
    def _insert_to_terminal(self, code):
        self.tabview.set("Terminal")
        # Insert di posisi input saat ini
        self._tw.insert("end", code)
        self._tw.see("end")

    # * Generate script file manual (menyimpan script ke folder "script_generation")
    def _generate_script_file(self, script):
        try:
            import os
            # Set root folder dan bikin folder baru
            rootDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            targetDir = os.path.join(rootDir, "script_generation")
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
            
            # Sanitasi nama file
            clean_name = "".join([c if c.isalnum() else "_" for c in script["name"]])
            ext = script.get("ext", ".txt")
            file_path = os.path.join(targetDir, f"{clean_name}{ext}")
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(script["code"])
                
            self.log_to_terminal(f"\n[+] Script '{script['name']}' generated manually!\n", "[success] ")
            self.log_to_terminal(f"    -> Saved in: {file_path}\n\n", "dimText")
        except Exception as e:
            self.log_to_terminal(f"\n[!] Failed to generate script: {e}\n", "errorText")

    # * Search handler
    def _on_script_search(self, *args):
        query = self.script_search_var.get().lower().strip()
        self._populate_script_list(filterQuery=query)

    # * ========== DECODER TAB (v6.1 New) ==========

    # * Setup halaman Decoder dengan auto/manual mode
    def _setup_decoder_tab(self):
        for widget in self.tab_decoder.winfo_children():
            widget.destroy()

        # -- Header --
        header_frame = ctk.CTkFrame(self.tab_decoder, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(15, 10))

        lbl_title = ctk.CTkLabel(header_frame, text="UNIVERSAL DECODER v6.1", font=("Roboto", 20, "bold"), text_color="#00ffff")
        lbl_title.pack(side="left")

        lbl_hint = ctk.CTkLabel(header_frame, text="Auto-detect & Decode Multiple Encodings", font=("Roboto", 11), text_color="#555555")
        lbl_hint.pack(side="right", padx=10)

        # -- Mode Selection (Frame dengan border) --
        mode_frame = ctk.CTkFrame(self.tab_decoder, fg_color="#080808", border_width=1, border_color="#222222")
        mode_frame.pack(fill="x", padx=20, pady=10)

        self.decoder_mode_var = ctk.StringVar(value="auto")

        radio_auto = ctk.CTkRadioButton(mode_frame, text="AUTO DETECT", variable=self.decoder_mode_var, value="auto",
                                         font=("Roboto", 12, "bold"), command=self._decoder_mode_changed,
                                         fg_color="#0066cc", hover_color="#0088ff")
        radio_auto.pack(side="left", padx=15, pady=10)

        radio_manual = ctk.CTkRadioButton(mode_frame, text="MANUAL SELECT", variable=self.decoder_mode_var, value="manual",
                                           font=("Roboto", 12, "bold"), command=self._decoder_mode_changed,
                                           fg_color="#cc6600", hover_color="#ff8800")
        radio_manual.pack(side="left", padx=15, pady=10)

        # -- Dropdown Encoding Type (Always Visible) --
        dropdown_frame = ctk.CTkFrame(self.tab_decoder, fg_color="#080808", border_width=1, border_color="#222222")
        dropdown_frame.pack(fill="x", padx=20, pady=5)

        lbl_manual = ctk.CTkLabel(dropdown_frame, text="Encoding Type:", font=("Roboto", 11, "bold"), text_color="#00ff00")
        lbl_manual.pack(side="left", padx=(20, 10), pady=10)

        self.decoder_type_var = ctk.StringVar(value="base64")
        encoding_types = [
            "base64", "base64url", "base64double", "base32", "base85", "ascii85",
            "url", "urldouble", "html", "hex", "binary", "rot13", "reverse"
        ]

        self.decoder_type_menu = ctk.CTkOptionMenu(dropdown_frame, values=encoding_types, variable=self.decoder_type_var,
                                                    font=("Roboto", 11, "bold"), fg_color="#1a1a1a", button_color="#2a2a2a",
                                                    button_hover_color="#3a3a3a", width=200, height=32)
        self.decoder_type_menu.pack(side="left", padx=10, pady=10)

        lbl_hint_decode = ctk.CTkLabel(dropdown_frame, text="(For AUTO: detects automatically)  (For MANUAL: use dropdown)", 
                                        font=("Roboto", 9, "italic"), text_color="#555555")
        lbl_hint_decode.pack(side="right", padx=10, pady=10)

        # -- Input Area --
        input_frame = ctk.CTkFrame(self.tab_decoder, fg_color="#080808", border_width=1, border_color="#222222")
        input_frame.pack(fill="both", expand=False, padx=20, pady=10)

        lbl_input = ctk.CTkLabel(input_frame, text="ENCODED INPUT:", font=("Roboto", 11, "bold"), text_color="#00ff00")
        lbl_input.pack(anchor="w", padx=10, pady=(10, 5))

        self.decoder_input = ctk.CTkTextbox(input_frame, font=("Consolas", 13), fg_color="#050505", border_width=0,
                                             text_color="#cccccc", height=120)
        self.decoder_input.pack(fill="both", expand=True, padx=10, pady=5)

        # -- Action Buttons --
        btn_frame = ctk.CTkFrame(self.tab_decoder, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=5)

        self.btn_decode = ctk.CTkButton(btn_frame, text="AUTO DECODE", font=("Roboto", 13, "bold"),
                                         fg_color="#0066cc", hover_color="#0088ff", height=40, width=160,
                                         command=self._run_auto_decode)
        self.btn_decode.pack(side="left", padx=10)

        self.btn_decode_manual = ctk.CTkButton(btn_frame, text="DECODE (MANUAL)", font=("Roboto", 13, "bold"),
                                                fg_color="#cc6600", hover_color="#ff8800", height=40, width=160,
                                                command=self._run_manual_decode)
        self.btn_decode_manual.pack(side="left", padx=10)

        self.btn_encode = ctk.CTkButton(btn_frame, text="ENCODE", font=("Roboto", 13, "bold"),
                                         fg_color="#9933cc", hover_color="#aa44dd", height=40, width=120,
                                         command=self._run_encode)
        self.btn_encode.pack(side="left", padx=10)

        self.btn_clear = ctk.CTkButton(btn_frame, text="CLEAR", font=("Roboto", 13, "bold"),
                                        fg_color="#333333", hover_color="#444444", height=40, width=100,
                                        command=self._decoder_clear)
        self.btn_clear.pack(side="right", padx=10)

        self.btn_copy = ctk.CTkButton(btn_frame, text="COPY RESULT", font=("Roboto", 13, "bold"),
                                       fg_color="#006600", hover_color="#008800", height=40, width=130,
                                       command=self._decoder_copy_result)
        self.btn_copy.pack(side="right", padx=10)

        # -- Output Area --
        output_frame = ctk.CTkFrame(self.tab_decoder, fg_color="#080808", border_width=1, border_color="#222222")
        output_frame.pack(fill="both", expand=True, padx=20, pady=5)

        lbl_output = ctk.CTkLabel(output_frame, text="DECODED OUTPUT:", font=("Roboto", 11, "bold"), text_color="#00ff00")
        lbl_output.pack(anchor="w", padx=10, pady=(10, 5))

        self.decoder_output = ctk.CTkTextbox(output_frame, font=("Consolas", 13), fg_color="#050505", border_width=0,
                                              text_color="#00ff00", state="disabled")
        self.decoder_output.pack(fill="both", expand=True, padx=10, pady=5)

        # -- All Results Frame (Collapsible) --
        self.results_frame = ctk.CTkScrollableFrame(self.tab_decoder, fg_color="#080808", border_width=1, border_color="#222222", height=150)
        self.results_frame.pack(fill="x", padx=20, pady=(5, 10))

        lbl_results = ctk.CTkLabel(self.results_frame, text="ALL DECODING RESULTS:", font=("Roboto", 10, "bold"), text_color="#888888")
        lbl_results.pack(anchor="w", padx=10, pady=(5, 0))

        self.all_results_labels = []

        # Initialize manual mode visibility
        self._decoder_mode_changed()

    # * Handle decoder mode change (auto/manual)
    def _decoder_mode_changed(self):
        mode = self.decoder_mode_var.get()

        if mode == "manual":
            self.btn_decode.configure(state="disabled", fg_color="#222222", text_color="#555555")
            self.btn_decode_manual.configure(state="normal", fg_color="#cc6600", text_color="#ffffff")
            self.btn_encode.configure(state="normal", fg_color="#9933cc", text_color="#ffffff")
            # Enable dropdown - bright colors
            self.decoder_type_menu.configure(fg_color="#1a1a1a", button_color="#2a2a2a", state="normal")
        else:
            self.btn_decode.configure(state="normal", fg_color="#0066cc", text_color="#ffffff")
            self.btn_decode_manual.configure(state="disabled", fg_color="#222222", text_color="#555555")
            self.btn_encode.configure(state="disabled", fg_color="#222222", text_color="#555555")
            # Disable dropdown - gray/inactive colors
            self.decoder_type_menu.configure(fg_color="#1a1a1a", button_color="#1a1a1a", state="disabled")

    # * Run auto decode
    def _run_auto_decode(self):
        encoded_text = self.decoder_input.get("1.0", "end-1c").strip()
        
        if not encoded_text:
            self._decoder_output_show("[error] Error: Input is empty\n")
            return

        if not hasattr(self.core, 'decoder'):
            self._decoder_output_show("[error] Error: Decoder module not initialized\n")
            return

        # Run auto decode
        result = self.core.decoder.auto_decode(encoded_text)

        # Display result
        output_text = ""
        
        if result['success']:
            output_text += f"[success] ✓ Encoding Detected: {result['encoding_type']}\n"
            output_text += f"[info] Confidence: {result['confidence'] * 100:.1f}%\n"
            output_text += f"[info] Readable: {'Yes' if result.get('readable', False) else 'No'}\n"
            output_text += "[cyanText] " + "="*50 + "\n"
            output_text += f"[success] DECODED TEXT:\n\n{result['decoded_text']}\n"
        else:
            output_text += f"[error] ✗ Decoding Failed: {result.get('error', 'Unknown error')}\n"
            if result.get('all_results'):
                output_text += "[warning] Partial results available:\n"
                for r in result['all_results'][:3]:
                    output_text += f"  [info] - {r['encoding']}: {r['decoded'][:50]}...\n"

        self._decoder_output_show(output_text)

        # Show all results
        self._decoder_show_all_results(result.get('all_results', []))

    # * Run manual decode
    def _run_manual_decode(self):
        encoded_text = self.decoder_input.get("1.0", "end-1c").strip()
        encoding_type = self.decoder_type_var.get()
        
        if not encoded_text:
            self._decoder_output_show("[error] Error: Input is empty\n")
            return

        if not hasattr(self.core, 'decoder'):
            self._decoder_output_show("[error] Error: Decoder module not initialized\n")
            return

        # Run manual decode
        result = self.core.decoder.manual_decode(encoded_text, encoding_type)

        # Display result
        output_text = ""
        
        if result['success']:
            output_text += f"[success] ✓ Manual Decode ({encoding_type.upper()}):\n\n"
            output_text += f"[success] {result['decoded_text']}\n"
        else:
            output_text += f"[error] ✗ Decoding Failed: {result.get('error', 'Unknown error')}\n"

        self._decoder_output_show(output_text)
        self._decoder_show_all_results([])

    # * Run encode
    def _run_encode(self):
        text = self.decoder_input.get("1.0", "end-1c").strip()
        encoding_type = self.decoder_type_var.get()

        if not text:
            self._decoder_output_show("[error] Error: Input is empty\n")
            return

        if not hasattr(self.core, 'decoder'):
            self._decoder_output_show("[error] Error: Decoder module not initialized\n")
            return

        # Run encode
        result = self.core.decoder.encode(text, encoding_type)

        # Display result
        output_text = ""

        if result['success']:
            output_text += f"[success] ✓ Encoded ({encoding_type.upper()}):\n\n"
            output_text += f"[cyanText] {result['encoded_text']}\n"
        else:
            output_text += f"[error] ✗ Encoding Failed: {result.get('error', 'Unknown error')}\n"

        self._decoder_output_show(output_text)
        self._decoder_show_all_results([])

    # * Show all decoding results
    def _decoder_show_all_results(self, results):
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.destroy()

        if not results:
            return

        for i, result in enumerate(results[:10]):  # Show top 10
            readable_tag = "✓" if result.get('readable', False) else "✗"
            conf_pct = result.get('confidence', 0) * 100
            
            result_text = f"[{readable_tag}] {result['encoding']} ({conf_pct:.0f}%) → {result['decoded'][:60]}..."
            
            lbl = ctk.CTkLabel(self.results_frame, text=result_text, font=("Consolas", 10), 
                               text_color="#00ff00" if result.get('readable', False) else "#888888",
                               anchor="w", cursor="hand2")
            lbl.pack(fill="x", padx=10, pady=2)
            
            # Click to view full result
            lbl.bind("<Button-1>", lambda e, r=result: self._decoder_show_full_result(r))

    # * Show full result on click
    def _decoder_show_full_result(self, result):
        self.decoder_input.delete("1.0", "end")
        self.decoder_input.insert("1.0", result['decoded'])
        self._decoder_output_show(f"[info] Full result from {result['encoding']}:\n\n{result['decoded']}\n")

    # * Helper: Show output in decoder output box
    def _decoder_output_show(self, text):
        self.decoder_output.configure(state="normal")
        self.decoder_output.delete("1.0", "end")
        
        # Parse tags and insert with formatting
        lines = text.split('\n')
        for line in lines:
            tag = "end"
            if "[success]" in line:
                tag = "success"
            elif "[error]" in line:
                tag = "error"
            elif "[warning]" in line:
                tag = "warning"
            elif "[info]" in line:
                tag = "info"
            elif "[cyanText]" in line:
                tag = "cyanText"
            
            # Remove tags from display text
            display_line = line.replace("[success]", "").replace("[error]", "").replace("[warning]", "")
            display_line = display_line.replace("[info]", "").replace("[cyanText]", "").replace("[dimText]", "")
            
            self.decoder_output.insert("end", display_line + "\n", tag)
        
        self.decoder_output.configure(state="disabled")

    # * Clear decoder input/output
    def _decoder_clear(self):
        self.decoder_input.delete("1.0", "end")
        self._decoder_output_show("")
        for widget in self.results_frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.destroy()

    # * Copy result to clipboard
    def _decoder_copy_result(self):
        result_text = self.decoder_output.get("1.0", "end-1c").strip()
        if result_text:
            # Remove ANSI-like tags for clean copy
            clean_text = result_text
            for tag in ["[success]", "[error]", "[warning]", "[info]", "[cyanText]", "[dimText]"]:
                clean_text = clean_text.replace(tag, "")

            self.clipboard_clear()
            self.clipboard_append(clean_text)
            self.log_to_terminal("[success] Decoder result copied to clipboard!\n", "[success] ")

    # * Jalankan Windows OLE Drag-and-Drop (External Bridge v6.0.1)
    def _on_script_drag_start(self, event, script):
        self._preview_script(script)
        self.dragging_script = script
        
        # 1. Buat Ghost Image (Spectral Label - v6.0.1 tk.Toplevel)
        if hasattr(self, "ghost_window") and self.ghost_window:
            try: self.ghost_window.destroy()
            except: pass
            
        self.ghost_window = tk.Toplevel(self)
        self.ghost_window.overrideredirect(True)
        self.ghost_window.attributes("-topmost", True)
        self.ghost_window.attributes("-alpha", 0.9) # * Lebih pekat biar kelihatan
        self.ghost_window.configure(bg="#000000") # * Black background
        
        # Risk color bullet
        risk_c = {"Critical":"#f33","High":"#fc0","Medium":"#5de"}.get(script["risk"], "#666")
        
        ghost_lbl = tk.Label(
            self.ghost_window, text=f" ✥ {script['name']} ", 
            font=("Consolas", 11, "bold"), fg="#00ff00", bg="#000000",
            padx=8, pady=4,
            highlightthickness=1, highlightbackground=risk_c
        )
        ghost_lbl.pack()
        
        self.ghost_window.update_idletasks()
        # Update posisi awal
        self.drag_start_pos = (event.x, event.y)
        self.ole_dragging = False
        self._on_script_ghost_move(event)

    # * Update posisi Ghost Image & Trigger OLE (v6.0.5 Native Explorer Mode)
    def _on_script_ghost_move(self, event):
        if hasattr(self, "ghost_window") and self.ghost_window:
            # * Beri offset agar tidak menutupi kursor (Drop Target)
            x = event.x_root + 25
            y = event.y_root + 25
            self.ghost_window.geometry(f"+{x}+{y}")
            self.ghost_window.lift()
            self.ghost_window.update_idletasks()
            
            # * Trigger OLE Drag jika sudah geser > 10 pixel
            if not self.ole_dragging:
                dx = abs(event.x - self.drag_start_pos[0])
                dy = abs(event.y - self.drag_start_pos[1])
                if dx > 12 or dy > 12: 
                    self.ole_dragging = True
                    
                    # 1. Lepas kontrol mouse dari Python (CRITICAL!)
                    try:
                        ctypes.windll.user32.ReleaseCapture()
                    except:
                        pass
                        
                    # 2. Hapus Ghost Image lsg biar Windows OLE dapet fokus
                    if self.ghost_window:
                        self.ghost_window.destroy()
                        self.ghost_window = None
                        
                    # 3. Tembak OLE Drag
                    self._trigger_ole_drag()

    # * Akhiri Drag (v6.0.3)
    def _on_script_drag_end(self, event):
        if hasattr(self, "ghost_window") and self.ghost_window:
            try: self.ghost_window.destroy()
            except: pass
            self.ghost_window = None
        self.ole_dragging = False
        self.dragging_script = None

    # * Logic Mesin Drag-as-File (Native C# Bridge v6.1.0 + Clipboard Fallback)
    def _trigger_ole_drag(self):
        script = getattr(self, "dragging_script", None)
        if not script: return
        
        # Kompilasi jembatan jika belum ada (hanya sekali)
        bridge_path = self._ensure_drag_bridge()

        def run_drag():
            try:
                # 1. Persiapkan folder temp
                temp_dir = os.path.join(tempfile.gettempdir(), "ApexOmega_Drops")
                if not os.path.exists(temp_dir): os.makedirs(temp_dir)
                
                # 2. Buat file fisik
                clean_name = "".join([c if c.isalnum() else "_" for c in script["name"]])
                ext = script.get("ext", ".txt")
                file_path = os.path.join(temp_dir, f"{clean_name}{ext}")
                
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(script["code"])
                
                # 3. Panggil DragBridge.exe jika ada (OLE Drag ke Explorer/Editor)
                if bridge_path and os.path.exists(bridge_path):
                    subprocess.run([bridge_path, file_path], creationflags=subprocess.CREATE_NO_WINDOW)
                
                # 4. Clipboard Fallback (Browser ga nerima OLE dari external)
                self.after(0, lambda: self._clipboard_fallback(script["code"], script["name"]))
            except:
                # Kalo drag gagal total, tetep copy ke clipboard
                self.after(0, lambda: self._clipboard_fallback(script["code"], script["name"]))

        threading.Thread(target=run_drag, daemon=True).start()

    # * Clipboard fallback kalo OLE drag ga diterima target (browser sandbox)
    def _clipboard_fallback(self, code, name):
        try:
            self.clipboard_clear()
            self.clipboard_append(code)
            self.log_to_terminal(f"[+] Script '{name}' copied to clipboard (Ctrl+V to paste)\n", "[success] ")
        except:
            pass

    # * Otomatis kompilasi C# Bridge menggunakan CSC.exe bawaan Windows (v6.0.7)
    def _ensure_drag_bridge(self):
        try:
            rootDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            coreDir = os.path.join(rootDir, "Core")
            if not os.path.exists(coreDir): os.makedirs(coreDir)
            
            bridge_exe = os.path.join(coreDir, "DragBridge.exe")
            if os.path.exists(bridge_exe): return bridge_exe
            
            # * DragBridge C# v6.1.0 (Zero-Latency Drag)
            cs_source = """
            using System;
            using System.Windows.Forms;
            using System.Collections.Specialized;
            using System.IO;
            using System.Runtime.InteropServices;
            class Program {
                [DllImport("user32.dll")] static extern short GetAsyncKeyState(int vKey);
                [STAThread]
                static void Main(string[] args) {
                    if (args.Length == 0) return;
                    
                    // * Tunggu sampai mouse beneran kepencet (v6.1.0 Precission)
                    int timeout = 0;
                    while ((GetAsyncKeyState(0x01) & 0x8000) == 0 && timeout < 20) {
                        System.Threading.Thread.Sleep(5);
                        timeout++;
                    }

                    DataObject data = new DataObject();
                    data.SetFileDropList(new StringCollection { args[0] });
                    try { data.SetText(File.ReadAllText(args[0]), TextDataFormat.UnicodeText); } catch {}
                    
                    Application.DoEvents();
                    Control c = new Control();
                    c.DoDragDrop(data, DragDropEffects.Copy);
                }
            }
            """
            
            cs_file = os.path.join(coreDir, "DragBridge.cs")
            with open(cs_file, "w") as f: f.write(cs_source)
            
            # Cari CSC.exe (Compiler)
            csc_path = r"C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe"
            if not os.path.exists(csc_path): 
                csc_path = r"C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe"
            
            if os.path.exists(csc_path):
                subprocess.run([csc_path, "/target:winexe", "/out:" + bridge_exe, cs_file], 
                              creationflags=subprocess.CREATE_NO_WINDOW)
                return bridge_exe
            return None
        except:
            return None

    # * Secret Sequence: !testalltools! (Hyper-Real Hacker Visual v6.2.0)
    def start_hacker_mode(self):
        if self.hacker_mode: return
        self.hacker_mode = True
        self.log_to_terminal("\n" + "="*60 + "\n", "[success] ")
        self.log_to_terminal("  [!!!] APEXOMEGA OVERRIDE: ACTIVATED [!!!]\n", "[danger] ")
        self.log_to_terminal("="*60 + "\n\n", "[success] ")
        
        # Bind ESC globally
        self.bind_all("<Escape>", lambda e: self.stop_hacker_mode())
        
        import random, time, secrets
        tools = ["Nmap", "Metasploit", "Dirb", "Ghidra", "BurpSuite", "Wireshark", "Hashcat", "Aircrack-ng", "Sqlmap", "Hydra", "John"]
        actions = ["SCANNING", "BRUTEFORCING", "EXPLOITING", "INJECTING", "SNIFFING", "DECRYPTING", "BYPASSING", "DUMPING"]
        
        def run_hacker():
            while self.hacker_mode:
                mode = random.random()
                # * Color Randomizer v6.2.2
                tag = random.choice(["success", "success", "success", "errorText", "blueText"])
                
                if mode < 0.4: # Standard Log
                    tool = random.choice(tools)
                    act = random.choice(actions)
                    addr = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
                    log = f"[{tool}] {act} Target {addr}... [OK]\n"
                    self.after(0, lambda m=log, t=tag: self.log_to_terminal(m, t))
                    time.sleep(random.uniform(0.05, 0.1))
                
                elif mode < 0.6: # Hex Dump
                    offset = secrets.token_hex(4).upper()
                    hex_data = " ".join([secrets.token_hex(1).upper() for _ in range(8)])
                    log = f"0x{offset}: {hex_data}  {secrets.token_urlsafe(8)}\n"
                    self.after(0, lambda m=log, t=tag: self.log_to_terminal(m, t))
                    time.sleep(0.02)
                
                elif mode < 0.8: # Progress Bar
                    label = random.choice(["DCRYPT", "UPLOAD", "PWNAGE", "SYNC", "FETCH"])
                    bar_chars = 20
                    for i in range(bar_chars + 1):
                        if not self.hacker_mode: break
                        perc = int((i/bar_chars) * 100)
                        bar = "#" * i + "-" * (bar_chars - i)
                        log = f"\r  [*] {label:8} [{bar}] {perc}%"
                        # Bar tetep ijo biar rapi
                        self.after(0, lambda m=log: self.log_to_terminal(m, "success"))
                        time.sleep(0.01)
                    self.after(0, lambda: self.log_to_terminal(" [DONE]\n", "success"))
                    time.sleep(0.1)
                
                else: # Rapid Hit
                    status = random.choice(["AUTHORIZED", "GRANTED", "SUCCESS", "BYPASSED"])
                    hit = f"  >>> HIT: {secrets.token_hex(16).upper()} ... [{status}]\n"
                    self.after(0, lambda m=hit, t=tag: self.log_to_terminal(m, t))
                    time.sleep(0.01)
                
            self.after(0, lambda: self.log_to_terminal("\n[!] TERMINATED BY USER SIGINT.\n", "[warning] "))

        threading.Thread(target=run_hacker, daemon=True).start()

    def stop_hacker_mode(self):
        self.hacker_mode = False
        self.unbind_all("<Escape>")

    # ? Handler klik kanan -> Paste (v6.2.1)
    def _on_right_click(self, event):
        try:
            clipboard = self.clipboard_get()
            if clipboard:
                # Pastikan paste cuma bisa di area input (setelah prompt)
                if self._tw.compare("insert", "<", "inputStart"):
                    self._tw.mark_set("insert", "end")
                
                self._tw.insert("insert", clipboard)
                self._tw.see("end")
        except Exception:
            pass
        return "break"



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
                
            # * Paste Shield & Command Validation (v5.9.5)
            # Jika diawali < maka ini adalah payload HTML/XML, jangan anggap sebagai command/target.
            is_html_payload = userInput.lower().strip().startswith("<")
            
            if is_html_payload:
                is_potential_target = False
            else:
                # * Deteksi apakah input ini target baru (URL/IP) atau cuma payload script (v5.9.1 Fix)
                is_potential_target = (
                    not userInput.startswith("!") and 
                    "." in userInput and 
                    " " not in userInput and 
                    "<" not in userInput and 
                    ">" not in userInput and
                    "(" not in userInput and
                    len(userInput) < 100
                )
            
            # * Prioritas: !command > target_baru > payload_biasa
            if is_potential_target:
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
            elif is_potential_target:
                target = userInput
                self._append_system(f"\n[*] New Target Set: {target}\n", "cyanText")
                def recon_start():
                    self.core._run_recon_module([])
                    self.show_prompt()
                threading.Thread(target=recon_start, daemon=True).start()
            else:
                # * Cuma input biasa/payload, jangan trigger recon
                pass

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

    def _on_mode_change(self):
        """Handle mode switch between WEB and WIFI hacking"""
        mode = self.mode_var.get()
        if mode == "WEB":
            self.mode_icon.configure(text="📡", text_color="#00ff00")
            self.log_to_terminal("\n[MODE] Switched to WEB HACKING mode\n", "[success] ")
        else:
            self.mode_icon.configure(text="📶", text_color="#ff6600")
            self.log_to_terminal("\n[MODE] Switched to WIFI HACKING mode\n", "[warning] ")
        # Refresh tools sidebar
        if self.tools_visible:
            self._populate_tools()
        # Auto-show prompt agar bisa langsung ngetik (no need Ctrl+C)
        self.after(100, self.show_prompt)

    def _toggle_tools(self):
        if not self.tools_visible:
            self.tools_frame.pack(fill="both", expand=True, padx=5, pady=5)
            self._populate_tools()
            self.tools_visible = True
        else:
            self.tools_frame.pack_forget()
            self.tools_visible = False

    def _populate_tools(self):
        """Populate tools sidebar based on current mode"""
        for widget in self.tools_frame.winfo_children():
            widget.destroy()

        # Mode-specific tool categories
        web_categories = {
            "RECON / INFO": ["nmap", "recon", "webaudit", "headers", "cookie", "cewl", "dmitry", "sslscan", "testssl", "wayback", "gau"],
            "DISCOVERY": ["subdomain", "vhost", "webports", "dirb", "git", "dnsenum", "fierce", "nikto", "apacheusers"],
            "VULNERABILITY": ["vuln", "wp", "form", "waf", "cms", "joomscan", "wapiti", "webcache", "nuclei", "padbuster"],
            "API / CLOUD": ["api", "cloud", "ffuf", "wfuzz", "skipfish"],
            "EXPLOITATION": ["payload", "stress", "cmdi", "davtest", "weevely", "webacoo", "laudanum", "slowhttp"],
            "NETWORK CONTROL": ["evil", "scanlan", "kill", "monitor"],
            "UTILITY": ["help", "script", "urlcrazy", "gowitness", "webtools", "websploit"]
        }
        
        wifi_categories = {
            "WIFI RECON": ["wash", "airodump", "airodump-ng", "kismet", "wigle"],
            "WIFI ATTACKS": ["aireplay", "aireplay-ng", "mdk4", "mdk3", "reaver", "bully"],
            "WIFI CRACK": ["aircrack", "aircrack-ng", "hashcat", "john"],
            "WIFI UTILITY": ["macchanger", "ifconfig", "iwconfig", "rfkill"],
            "GENERAL": ["help", "script", "monitor"]
        }
        
        categories = wifi_categories if self.mode_var.get() == "WIFI" else web_categories

        for cat, tools in categories.items():
            lbl = ctk.CTkLabel(self.tools_frame, text=cat, font=("Roboto", 11, "bold"), text_color="#444444", anchor="w")
            lbl.pack(fill="x", pady=(10, 2), padx=5)

            for t in sorted(tools):
                btn = ctk.CTkButton(self.tools_frame, text=t.upper(), anchor="w", fg_color="transparent", text_color="#777777", hover_color="#1a1a1a", height=28, command=lambda x=t: self._show_how_to(x))
                btn.pack(fill="x", pady=0)

    # * Setup Roadmap Tab v6.3 (Flowchart Style - Beginner Friendly)
    def _setup_roadmap_tab(self):
        for widget in self.tab_roadmap.winfo_children():
            widget.destroy()

        lbl_title = ctk.CTkLabel(self.tab_roadmap, text="🗺️ PETA PENAKLUKAN WEBSITE", font=("Roboto", 28, "bold"), text_color="#00cc66")
        lbl_title.pack(pady=(20, 5))

        lbl_sub = ctk.CTkLabel(self.tab_roadmap, text="8 Langkah mudah buat hack website - Dari 0 sampe akses penuh!", font=("Roboto", 14), text_color="#555555")
        lbl_sub.pack(pady=(0, 15))

        self.roadmap_checks = []
        roadmap_frame = ctk.CTkScrollableFrame(self.tab_roadmap, fg_color="#0a0a0a", border_width=0)
        roadmap_frame.pack(fill="both", expand=True, padx=40, pady=10)

        # * Flowchart Style - Visual Boxes with Arrows
        missions = [
            {
                "num": 1,
                "title": "RECONNAISSANCE",
                "subtitle": "🔍 Stalking Target (Pengumpulan Info)",
                "desc": "Seperti detektif yang ngumpulin info target sebelum aksi. Kita cari tau:\n• IP Address & Lokasi server\n• Pemilik domain & tanggal daftar\n• Teknologi yang dipake (framework, web server)\n• Subdomain yang tersembunyi",
                "command": "!recon quick  |  !recon deep  |  !recon full",
                "color": "#3498db"  # Blue
            },
            {
                "num": 2,
                "title": "INFRASTRUCTURE SCAN",
                "subtitle": "️ Cek Pintu & Jendela (Port Scanning)",
                "desc": "Ngetok satu-satu 'pintu' (port) server buat liat apa yang kebuka:\n• Port 80/443 = Web server\n• Port 22 = SSH (remote access)\n• Port 3306 = Database MySQL\n• Port 21 = FTP (file transfer)",
                "command": "!nmap  |  !nmap 80,443,8080",
                "color": "#e74c3c"  # Red
            },
            {
                "num": 3,
                "title": "DISCOVERY",
                "subtitle": "Mapping Kerajaan Digital",
                "desc": "Nyari semua 'cabang' target:\n• Subdomain (dev.site.com, admin.site.com)\n• Folder tersembunyi (/admin, /backup, /.git)\n• File sensitif (.env, config.php, database.sql)",
                "command": "!subdomain  |  !dirb  |  !webdiscovery",
                "color": "#f39c12"  # Orange
            },
            {
                "num": 4,
                "title": "WEB ANALYSIS",
                "subtitle": "Bedah Website Mikroskopis",
                "desc": "Periksa komponen website satu-satu:\n• Security Headers (HSTS, CSP, X-Frame)\n• Cookie Security (HttpOnly, Secure flags)\n• Form Input (cek bisa inject atau gak)\n• Git Exposure (.git folder yang kebuka)",
                "command": "!headers  |  !cookie  |  !form  |  !git",
                "color": "#9b59b6"  # Purple
            },
            {
                "num": 5,
                "title": "VULNERABILITY SCAN",
                "subtitle": "Cari Penyakit/Celah Keamanan",
                "desc": "Suntik 'obat tes' buat diagnosa penyakit website:\n• CORS Misconfiguration (bisa akses dari domain lain)\n• SSTI (Server-Side Template Injection)\n• CRLF Injection (inject header HTTP)\n• File Upload (bisa upload shell atau gak)",
                "command": "!vuln full  |  !vuln cors  |  !vuln ssti",
                "color": "#e67e22"  # Dark Orange
            },
            {
                "num": 6,
                "title": "API & CLOUD AUDIT",
                "subtitle": "Cek API & Cloud Storage",
                "desc": "Audit 'pintu belakang' modern:\n• API Endpoints (/api, /graphql, /swagger)\n• Cloud Buckets (S3, Firebase, Azure Blob)\n• Data Exposure (API yang kebuka publik)\n• Authentication Bypass",
                "command": "!api fuzz  |  !cloud all  |  !cloud s3",
                "color": "#1abc9c"  # Teal
            },
            {
                "num": 7,
                "title": "CMS AUDIT",
                "subtitle": "Audit CMS (WordPress, Joomla, Drupal)",
                "desc": "Specialized scan buat CMS populer:\n• Version detection (versi lama = rentan)\n• Plugin scanning (50+ plugin rentan)\n• User enumeration (daftar user)\n• Vulnerable files (wp-config.php, backup)",
                "command": "!wp all  |  !wp version  |  !wp plugins",
                "color": "#2ecc71"  # Green
            },
            {
                "num": 8,
                "title": "STRESS TESTING",
                "subtitle": "Uji Kekuatan Server",
                "desc": "Bebani server buat tau batas maksimal:\n• HTTP Flood (ribuan request bareng-bareng)\n• Multi-threading (50-500 concurrent connections)\n• Cache bypass (tembus proteksi WAF/CDN)\n• Real-time statistics",
                "command": "!stress 50 30  |  !nitro 100 60",
                "color": "#c0392b"  # Dark Red
            }
        ]

        for i, mission in enumerate(missions):
            # Connector Arrow (except first)
            if i > 0:
                arrow_lbl = ctk.CTkLabel(roadmap_frame, text="⬇️", font=("Roboto", 24), text_color="#555555")
                arrow_lbl.pack(pady=(5, 5))

            # Mission Box
            box_frame = ctk.CTkFrame(roadmap_frame, fg_color="#0f0f0f", border_width=2, 
                                     border_color=mission["color"], corner_radius=10)
            box_frame.pack(fill="x", padx=60, pady=5)

            # Header: Number + Title + Checkbox
            header_frame = ctk.CTkFrame(box_frame, fg_color="transparent")
            header_frame.pack(fill="x", padx=15, pady=(15, 10))

            # Number badge
            num_badge = ctk.CTkLabel(header_frame, text=f"#{mission['num']}", 
                                     font=("Roboto", 16, "bold"), text_color=mission["color"],
                                     width=50)
            num_badge.pack(side="left")

            # Title
            title_lbl = ctk.CTkLabel(header_frame, text=mission["title"], 
                                     font=("Roboto", 16, "bold"), text_color="#ffffff")
            title_lbl.pack(side="left", padx=10)

            # Checkbox (right aligned)
            cb = ctk.CTkCheckBox(header_frame, text="✓", width=30, 
                                 font=("Roboto", 14, "bold"),
                                 text_color=mission["color"], fg_color=mission["color"],
                                 hover_color=mission["color"], border_color="#333333")
            cb.pack(side="right")
            self.roadmap_checks.append(cb)

            # Subtitle
            sub_lbl = ctk.CTkLabel(box_frame, text=mission["subtitle"], 
                                   font=("Roboto", 13, "italic"), text_color="#888888")
            sub_lbl.pack(anchor="w", padx=75, pady=(0, 10))

            # Description
            desc_lbl = ctk.CTkLabel(box_frame, text=mission["desc"], 
                                    font=("Roboto", 12), text_color="#aaaaaa",
                                    wraplength=600, justify="left")
            desc_lbl.pack(anchor="w", padx=75, pady=(0, 10))

            # Command box
            cmd_frame = ctk.CTkFrame(box_frame, fg_color="#1a1a1a", corner_radius=5)
            cmd_frame.pack(fill="x", padx=75, pady=(0, 15))

            cmd_lbl = ctk.CTkLabel(cmd_frame, text=f"{mission['command']}", 
                                   font=("Consolas", 11), text_color="#00ff00")
            cmd_lbl.pack(padx=10, pady=8)

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
