import customtkinter as ctk
import threading
from tkinter import messagebox

# * Tema Shell Mode (Zaqi Interactive Edition v4.5)
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class InterfaceDesktop(ctk.CTk):
    def __init__(self, app_core):
        super().__init__()
        self.core = app_core
        self.title("ApexOmega Shell v4.5")
        self.geometry("1100x700")
        
        # * Standard Resizable Window
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.98)
        
        self.tools_visible = False
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
        # * Sembunyi dulu (pack_forget)
        
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

        # * -- Interactive Terminal --
        # * Kita pake textbox yang bisa diketik tapi di-handle Enter-nya
        self.terminal = ctk.CTkTextbox(self.tab_console, font=("Consolas", 13), text_color="#cccccc", border_width=0, border_spacing=20, fg_color="#050505")
        self.terminal.pack(fill="both", expand=True)
        self.terminal.bind("<Return>", self._on_enter)
        
        # * Startup System Teks (Small & Dark)
        self.terminal.insert("end", "ApexOmega Console [Version: 4.5]\n", ("small_dark",))
        self.terminal.tag_config("small_dark", foreground="#333333")

    def _initial_prompt(self):
        self.log_to_terminal("ENTER TARGET IP/URL >> ")

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

    def log_to_terminal(self, message, prefix="[root@shell] "):
        self.terminal.configure(state="normal")
        self.terminal.insert("end", f"{prefix}{message}\n")
        self.terminal.see("end")
        # * Note: Kita sisakan state normal biar user bisa ngetik

    def _on_enter(self, event):
        # * Ambil baris terakhir tempat user ngetik
        raw_text = self.terminal.get("1.0", "end-1c")
        lines = raw_text.split("\n")
        if not lines: return
        
        last_line = lines[-1]
        # * Bersihkan prefix kalo ada buat ambil command aslinya
        cmd = last_line.split(">>")[-1].strip() if ">>" in last_line else last_line.strip()
        
        # * Kalo ngetik !exit atau !command
        if cmd.startswith("!"):
            self.core.execute_shell_command(cmd)
        elif "ENTER TARGET" in last_line:
            target = last_line.split(">>")[-1].strip()
            self.core.set_active_target(target)
            self.log_to_terminal(f"TARGET SET: {target}")
            self.log_to_terminal("Type !<tool_name> to begin (e.g. !nmap)")
        
        # * Jangan biarkan Return default nambah baris kosong tanpa handle
        return None

    def _on_close(self):
        self.core.exitFramework()
        self.destroy()
