# ApexOmega Console v4.6

Advanced Penetration Testing Framework - Zaqi Interactive Edition.

Modular, interactive shell-based suite untuk security auditing, network reconnaissance, dan educational research.

## Fitur Utama

- **Zaqi Shell** -- Interactive command shell dengan prefix `!tool` untuk aktivasi modul
- **Network Hub** -- Port scanning, DNS records, Whois, Subdomain enumeration
- **Web Auditor** -- SQLi, XSS, LFI detection, admin finder, security header audit
- **WordPress Scanner** -- Version detection, plugin enum, user enum, vuln file check
- **Chaos Toolkit** -- Stress testing engine (Nitro Destroyer Profile)
- **Crypto Lab** -- Hash cracking, encoding/decoding, password generator
- **Apex Academy** -- Pentesting wiki dan roadmap untuk pemula
- **Auto-Update** -- Satu klik update langsung dari GitHub

## Instalasi

```bash
pip install -r requirements.txt
```

## Menjalankan

```bash
python ApexOmega.py
```

## Penggunaan Shell

1. Masukkan target IP/URL saat startup
2. Ketik `!nmap` untuk network scan
3. Ketik `!webaudit` untuk web vulnerability audit
4. Ketik `!wordpress` untuk WordPress scan
5. Ketik `!chaos` untuk stress testing
6. Ketik `!help` untuk panduan
7. Ketik `!exit` untuk keluar dari modul aktif

## Build ke EXE

```bash
build_app.bat
```

## Tech Stack

- Python 3.10+
- CustomTkinter (GUI)
- Rich (CLI Interface)
- Requests + BeautifulSoup4 (Web Scanning)
- WinSock Native Bridge (C/DLL untuk port scanning cepat)

## Credits

Developed by **Zaqi** -- Cyber Security Research & Development.
