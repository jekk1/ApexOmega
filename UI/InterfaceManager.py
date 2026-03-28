from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.layout import Layout
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

console = Console()

class InterfaceManager:
    # * Menampilkan banner utama dengan gaya modern
    @staticmethod
    def showBanner():
        bannerText = Text()
        bannerLines = [
            "  █████╗ ██████╗ ███████╗██╗  ██╗      ██████╗ ",
            " ██╔══██╗██╔══██╗██╔════╝╚██╗██╔╝     ██╔═══██╗",
            " ███████║██████╔╝█████╗   ╚███╔╝      ██║   ██║",
            " ██╔══██║██╔═══╝ ██╔══╝   ██╔██╗      ██║   ██║",
            " ██║  ██║██║     ███████╗██╔╝ ██╗     ╚██████╔╝",
            " ╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝      ╚═════╝ "
        ]
        for line in bannerLines:
            bannerText.append(line + "\n", style="bold green")
        
        bannerPanel = Panel(
            bannerText,
            subtitle="[bold green]Version 4.6 | Developed by Zaqi[/]",
            border_style="green",
            padding=(1, 2)
        )
        console.print(bannerPanel)

    # * Menampilkan menu utama untuk pemilihan tool
    @staticmethod
    def showMainMenu():
        table = Table(title="[bold green]Main Modules[/]", show_header=True, header_style="bold green", box=None)
        table.add_column("No", style="dim", width=4)
        table.add_column("Module Name", style="bold green")
        table.add_column("Description", style="italic green")

        table.add_row("01", "Network Hub", "Port Scanning, DNS, Whois, & Subdomains")
        table.add_row("02", "Web Auditor", "Vulnerability, CMS, Admin Finder, SSL")
        table.add_row("03", "Crypto Lab", "Hash Cracking, Encoding, Passgen")
        table.add_row("04", "Chaos Toolkit", "Honeypots, Reverse IP, Brute Force")
        table.add_row("05", "Apex Academy", "Pentesting Wiki & Roadmap")
        table.add_row("09", "Guided Scan", "Auto-audit on a single target IP/URL")
        table.add_row("00", "Exit", "Close the framework safely")

        console.print(table)

    # * Melacak progress scanning secara live
    @staticmethod
    def showScanProgress(taskName):
        return Progress(
            SpinnerColumn(),
            TextColumn(f"[bold green]{taskName}[/] - [progress.description]{{task.description}}"),
            BarColumn(bar_width=40, style="green", complete_style="bold green"),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        )

    # * Menampilkan tabel hasil scan yang rapi
    @staticmethod
    def showResultTable(title, columns, rows):
        table = Table(title=f"[bold green]{title}[/]", show_header=True, header_style="bold green")
        for col in columns:
            table.add_column(col, style="green")
        for row in rows:
            table.add_row(*row)
        console.print(table)

    # * Menampilkan bantuan singkat untuk setiap tool (Beginner Friendly)
    @staticmethod
    def showHelp(moduleName):
        helpData = {
            "01": "Dapatkan info jaringan target secara mendalam (Whois, DNS, Subdomain).",
            "02": "Audit keamanan website buat nyari celah (SQLi, XSS) atau file sensitif.",
            "03": "Urusan sandi dan kode (Pecahin hash MD5/SHA atau encode data).",
            "04": "Satu set alat 'khusus' buat trik advance dan eksplorasi server.",
            "05": "Tempat belajar buat lu yang pengen tau lebih banyak dunia cyber.",
            "09": "Otomatisasi! Masukin target, biarin sistem yang kerja buat lu."
        }
        msg = helpData.get(moduleName, "Pilih menu lewat angka buat mulai.")
        console.print(Panel(Text(msg, style="italic green"), title="Guide", border_style="bold green"))

    # * Mencetak log status dengan format yang rapi
    @staticmethod
    def logStatus(message, type="info"):
        styles = {
            "info": "bold green",
            "success": "bold green",
            "error": "bold red",
            "warning": "bold yellow"
        }
        logo = {
            "info": "[*]",
            "success": "[+]",
            "error": "[-]",
            "warning": "[!]"
        }
        style = styles.get(type, "white")
        prefix = logo.get(type, "")
        console.print(f"[{style}]{prefix}[/] {message}")
