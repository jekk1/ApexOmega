# ApexOmega Ultimate v6.4.0 (WiFi Warfare Edition)

Advanced Web & WiFi Penetration Testing - Professional Cyber Security Suite.
Modular, automated, and powerful tool for security auditing and vulnerability scanning.

## 🚀 NEW FEATURES v6.4.0 (The WiFi Warfare Update)

- **18 WiFi Hacking Tools** -- Full Aircrack-ng suite integration (!aircrack, !airodump, !aireplay, !wash, !reaver, !bully, !mdk3/4, !kismet, !wigle).
- **Password Cracking Engines** -- Hashcat GPU cracking & John the Ripper for offline attacks (!hashcat, !john).
- **Network Utility Tools** -- MAC changer, interface config, RF kill switch (!macchanger, !ifconfig, !iwconfig, !rfkill).
- **Mode Icon Indicator** -- Visual mode switcher (📡 WEB / 📶 WIFI) next to tabs for quick status recognition.
- **Auto-Prompt After Mode Switch** -- No more Ctrl+C needed! Direct typing after switching modes.
- **Complete WiFi Documentation** -- Full help database with syntax, modes, and examples for all WiFi tools.

## 🚀 CARRYOVER FROM v6.3.0

- **30+ Specialized Web Engines** -- Integrated 30+ tools from Kali Linux list into a single interactive console (!waf, !cmdi, !ffuf, !nuclei, !sslscan, dsb).
- **Manual Script Generation [GEN]** -- Simpan payload source code langsung ke folder `script_generation` lewat tombol [GEN] di tab Scripts.
- **Deep Assistant Docs** -- Panduan detail tiap tool sekarang bisa diakses langsung lewat Sidebar > How to Use.
- **Improved UI Sidebar** -- Navigasi kategori lebih rapi: Recon, Discovery, Vuln, API/Cloud, Exploitation, Network Control, & Utility.
- **Advanced Ghost Cursor** -- Sistem drag-and-drop file/payload ke browser yang lebih responsif dan transparan.
- **Version Persistence** -- Sinkronisasi versi global antara UI, internal logic, dan Git repository.

## 🛠️ THE PENTESTING WORKFLOW (8 MISSION STRATEGY)

### WEB HACKING MODE (📡)

1. **Reconnaissance (!recon)** -- Stalking IP, DNS, WHOIS, Tech Detection.
2. **Infrastructure Scan (!nmap)** -- Mapping port, service, dan vulnerability server.
3. **Discovery (!subdomain / !dirb)** -- Pencarian subdomain rahasia dan folder tersembunyi.
4. **Web Audit (!headers / !cookie / !form / !git)** -- Audit security layer-7 dan exposure repository.
5. **Vulnerability Scan (!vuln)** -- Scan 100+ celah (CORS, SSTI, CRLF, Host Injection, Upload, Paths).
6. **API & Cloud Hunting (!api / !cloud)** -- Bongkar jalur data REST/GraphQL dan storage bocor.
7. **CMS & Special Tools (!wp / !joomscan)** -- Audit khusus platform CMS dan signature spesifik.
8. **Stress Testing (!stress)** -- Simulasi ketahanan server terhadap serangan Layer 7 (HTTP Flood).

### WIFI HACKING MODE (📶)

1. **Recon (!wash / !kismet / !airodump)** -- Scan WPS networks, detect WiFi, capture packets.
2. **Attack (!aireplay / !mdk3 / !mdk4)** -- Deauthentication, beacon flood, DoS attacks.
3. **Crack (!aircrack / !hashcat / !john)** -- WEP/WPA2 password cracking dengan GPU acceleration.
4. **WPS Exploit (!reaver / !bully)** -- WPS PIN brute-force (4-10 jam).
5. **Utility (!macchanger / !iwconfig / !rfkill)** -- MAC spoofing, interface config, unblock WiFi.
6. **Network Control (!evil / !scanlan / !kill / !monitor)** -- ARP spoofing, bandwidth limiting, traffic monitoring.

## 📦 INSTALASI & JALANKAN (Windows Native)

```powershell
# 1. Clone Repository (Branch: main)
git clone https://github.com/jekk1/ApexOmega.git

# 2. Install Dependencies (Minimal Python 3.10+)
pip install -r requirements.txt

# 3. Gaskan Mode GUI/CLI!
python ApexOmega.py
```

## 🛠️ BUILDING FROM SOURCE (Windows Exe)

Kalo mau build jadi `.exe` sendiri, pastiin udah install PyInstaller:

```powershell
# 1. Install PyInstaller
pip install pyinstaller

# 2. Jalankan Build Script
./build_app.bat
```

> [!NOTE]
> Output `.exe` bakal ada di folder `dist/`. Build script ini udah otomatis handle asset `customtkinter` biar gak error pas dijalanin.

## 🔐 SECURITY & ETHICS

**⚠️ WARNING - WiFi Hacking:**
- HANYA gunakan di jaringan Anda sendiri atau dengan izin tertulis dari pemilik
- Memerlukan Kali Linux / Linux environment untuk full functionality
- WiFi adapter harus support monitor mode & packet injection
- Penggunaan ilegal dapat melanggar UU ITE dan hukum cyber setempat

Developed by **Zaqi** -- Cyber Security Research & Development.
**Disclaimer:** Alat ini hanya untuk tujuan edukasi dan audit keamanan profesional. Penyalahgunaan untuk aktivitas ilegal sepenuhnya tanggung jawab pengguna.

---
© 2026 ApexOmega Cyber Framework. Built for the next level of security auditing.
