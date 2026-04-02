from typing import List, Dict, Optional, Any

# * Modul Bantuan & Panduan Penggunaan Alat Bantu Keamanan
class GuidedAssistant:
    """
    GuidedAssistant itu kayak Google Translate + Wikihow buat hacker pemula.
    
    Punya 3 fitur utama:
    
    1. HELP DATABASE - Kamus istilah hacker
       - "XSS itu apa sih?" → Cross-Site Scripting, nyelipin script di website
       - "SQL Injection itu?" → Nyelipin perintah SQL buat sedot database
       - "Reverse Shell?" → Teknik biar server yang 'nelfon' balik ke lu
       - "Honeypot?" → Server jebakan buat nangkep hacker
    
    2. ROADMAP - Panduan jadi hacker dari 0 sampe jago
       - Level 0: Belajar dasar (Linux, terminal, network)
       - Level 1: Web basics (HTTP, HTML, browser dev tools)
       - Level 2: Attack fundamentals (recon, scan, exploit)
       - Level 3: Professional (bug bounty, documentation)
    
    3. QUICK TIPS - Tips keamanan cepat
       - "Jangan pernah audit tanpa ijin!"
       - "Pake VM buat nyobain tool baru"
       - "Join komunitas security lokal"
       - "Latihan di platform legal (TryHackMe, HackTheBox)"
    
    Tool ini cocok buat lu yang:
    - Baru belajar cybersecurity
    - Bingung mulai dari mana
    - Butuh penjelasan sederhana tanpa jargon ribet
    - Mau tau arti istilah-istilah aneh di dunia hacking
    
    Anggap aja kayak punya mentor pribadi yang sabar jelasin!
    """
    def __init__(self):
        # * Database Basis Pengetahuan Perangkat
        self.helpDatabase: Dict[str, str] = {
            "recon": """Tahap pengumpulan informasi (Reconnaissance) - Ini adalah LANGKAH PERTAMA dan PALING PENTING sebelum melakukan attack!
            
🎯 APA TUJUANNYA?
Seperti detektif yang stalking target, kita kumpulin SEMUA info publik tentang target:
• IP Address asli server (bisa jadi beda dari domain)
• Lokasi geografis server (negara, kota, ISP)
• Pemilik domain & tanggal registrasi
• Email admin & nomor telepon (dari WHOIS)
• Teknologi yang dipake (web server, framework, CMS)
• Subdomain-subdomain tersembunyi

📊 MODE YANG TERSEDIA:
• quick = IP + DNS resolution (cepat, 5 detik)
• deep = Quick + WHOIS data + DNS lengkap (15 detik)
• full = Deep + Technology detection + Certificate subdomain (30 detik)

💡 CONTOH PENGGUNAAN:
!recon          → Mode default (quick)
!recon quick    → IP & DNS aja
!recon deep     → Plus WHOIS & DNS records
!recon full     → SEMUA info + tech stack detection

⚠️ CATATAN:
- Tool ini 100% PASSIVE (gak nyentuh server target langsung)
- Gak ninggalin jejak di log server target
- Legal buat dipake karena data publik""",

            "nmap": """Network Mapper - Tool LEGENDARIS buat port scanning yang dipake sama professional pentester!

🎯 APA TUJUANNYA?
Ngetok satu-satu 'pintu' (port) server buat liat layanan apa yang jalan:
• Port 21 = FTP (file transfer, sering vulnerable)
• Port 22 = SSH (remote access, bisa di-bruteforce)
• Port 23 = Telnet (unencrypted, bahaya!)
• Port 25 = SMTP (email server)
• Port 53 = DNS
• Port 80 = HTTP (web server)
• Port 443 = HTTPS (secure web)
• Port 3306 = MySQL database
• Port 3389 = Remote Desktop (RDP)
• Port 8080 = Alternative HTTP

📊 CARA KERJA:
Tool ini ngirim packet khusus ke setiap port, terus liat responnya:
• OPEN = Port aktif, ada layanan yang jalan
• CLOSED = Port gak dipake
• FILTERED = Port diblokir firewall

💡 CONTOH PENGGUNAAN:
!nmap              → Scan 10 port paling umum (80, 443, 22, dll)
!nmap 80,443       → Scan port spesifik
!nmap 1-1000       → Scan range port
!nmap 22,80,3306   → Scan port pilihan

⚠️ PERINGATAN:
- Bisa ke-detect sama IDS/IPS (Intrusion Detection System)
- Beberapa port scan bisa crash layanan jadul
- Gunakan dengan bijak!""",

            "subdomain": """Subdomain Enumeration - Nyari semua 'cabang' dari domain target!

🎯 APA TUJUANNYA?
Perusahaan besar punya BANYAK subdomain yang sering LUPA diproteksi:
• dev.target.com (development server - sering vulnerable)
• admin.target.com (dashboard admin - high value target)
• api.target.com (API endpoint - bisa leak data)
• staging.target.com (staging server - data production)
• mail.target.com (email server)
• vpn.target.com (VPN gateway)

📊 METODE YANG DIPAKE:
1. BRUTE FORCE - Tebak subdomain umum pake wordlist
2. PASSIVE (crt.sh) - Intip sertifikat SSL yang terdaftar
3. DNS ENUMERATION - Cek DNS records

💡 CONTOH PENGGUNAAN:
!subdomain brute   → Bruteforce pake wordlist
!subdomain passive → Cari dari sertifikat SSL (silent)
!subdomain         → Default (passive mode)

⚠️ KENAPA INI PENTING?
Sering banget subdomain yang:
• Lupa di-update (software jadul, vulnerable)
• Gada proteksi WAF
• Password default
• Bisa jadi 'pintu belakang' ke production!""",

            "webaudit": """Web Application Audit - Pemeriksaan KESELURUHAN keamanan website!

🎯 APA TUJUANNYA?
Audit lengkap semua aspek keamanan web:
1. TECHNOLOGY DETECTION - Tau website pake apa
   • Web server (Apache, Nginx, IIS)
   • Framework (Laravel, Django, Rails)
   • CMS (WordPress, Joomla, Drupal)
   • Database (MySQL, PostgreSQL, MongoDB)

2. WAF DETECTION - Cek ada proteksi atau gak
   • Cloudflare
   • Akamai
   • ModSecurity
   • Imperva

3. SQL INJECTION CHECK - Test input forms
   • Login forms
   • Search boxes
   • URL parameters

💡 CONTOH PENGGUNAAN:
!webaudit tech     → Technology detection only
!webaudit sqli     → SQL injection test only
!webaudit full     → SEMUA audit (recommended)

⚠️ HASIL YANG DIDAPAT:
• Daftar teknologi + versi
• WAF detected atau tidak
• Potential vulnerabilities
• Security score""",

            "vuln": """Vulnerability Atlas Scanner - Scanner CERDAS yang nyari celah keamanan spesifik!

🎯 APA TUJUANNYA?
Suntik 'obat tes' ke website buat diagnosa penyakit keamanan:

1. CORS MISCONFIGURATION
   • Website seharusnya cuma terima request dari domain sendiri
   • Kalo salah config, hacker bisa ambil data user dari browser korban
   • Contoh: bank.com bisa diakses dari hacker.com

2. SSTI (Server-Side Template Injection)
   • Website modern pake template engine (Jinja2, Twig, PHP)
   • Kalo input user gak difilter, bisa inject code berbahaya
   • Bisa dapet remote code execution!

3. CRLF INJECTION
   • Inject header HTTP palsu
   • Set cookie malicious
   • Redirect ke website phishing
   • Cache poisoning

4. HOST HEADER INJECTION
   • Manipulasi header Host HTTP
   • Password reset link bisa diarahkan ke domain hacker
   • Cache poisoning

5. FILE UPLOAD VULNERABILITY
   • Cek apakah bisa upload file berbahaya
   • Upload PHP shell buat remote control
   • Upload HTML buat phishing

💡 CONTOH PENGGUNAAN:
!vuln full         → Scan semua vulnerability
!vuln cors         → CORS check only
!vuln ssti         → SSTI check only
!vuln crlf         → CRLF check only
!vuln host         → Host header check
!vuln upload       → File upload check
!vuln paths        → Sensitive paths check (100+ paths!)

⚠️ PERINGATAN:
- Tool ini AKTIF nyuntik payload (bisa ke-detect)
- Beberapa test bisa trigger WAF
- Gunakan hanya di environment yang ada ijin!""",

            "api": """API Security Auditor - Inspektur khusus buat API (Application Programming Interface)!

🎯 APA TUJUANNYA?
API itu kayak pelayan restoran:
• Lu pesan (request) → API ambil dari server → Sajiin ke lu (response)
• Masalahnya: Gimana kalo pelayannya bisa dibohongi?

1. ENDPOINT FUZZING - Cari 'pintu masuk' API yang tersembunyi
   • /api, /api/v1, /api/v2, /graphql, /rest
   • /swagger, /api-docs (dokumentasi yang kadang kebuka publik!)
   • /admin/api, /user/api (endpoint internal yang bocor)
   • /auth, /login, /register, /token

2. HTTP METHODS CHECK - Cek metode apa aja yang bisa dipake
   • GET (ambil data)
   • POST (kirim data)
   • PUT (update data)
   • DELETE (hapus data) ← Ini BAHAYA kalo gak diproteksi!
   • OPTIONS (cek method tersedia)

3. AUTHENTICATION BYPASS
   • Kadang API lupa proteksi endpoint tertentu
   • Bisa akses data user tanpa login
   • Contoh: /api/users tanpa auth

💡 CONTOH PENGGUNAAN:
!api fuzz          → Cari semua endpoint API
!api methods       → Check HTTP methods
!api all           → SEMUA audit API

⚠️ DATA YANG BISA LEAK:
• User credentials
• Personal information
• API keys & tokens
• Database records""",

            "cloud": """Cloud Storage Auditor - Detektif harta karun di cloud!

🎯 APA TUJUANNYA?
Perusahaan modern nyimpen data di cloud storage:
• AWS S3 (Amazon)
• Firebase (Google)
• Google Cloud Storage
• Azure Blob (Microsoft)
• DigitalOcean Spaces

MASALAH BESAR: Banyak yang LUPA setting permission!

Bayangin lu punya gudang data di cloud, tapi:
• Gak dikunci (public access)
• Siapa aja bisa baca (data leakage)
• Siapa aja bisa tulis (upload malware)
• Siapa aja bisa hapus (sabotage)

📊 CARA KERJA:
1. BUCKET NAMING PERMUTATIONS - Tebak nama bucket
   • Dari nama domain, bikin variasi:
   • nama.com → nama, nama-bucket, nama-storage
   • bucket-nama, nama.prod, nama.dev

2. PERMISSION CHECKING - Cek apakah bucket kebuka
   • Bisa baca file? (data breach)
   • Bisa upload file? (bisa nyelipin malware)
   • Bisa hapus file? (sabotage)

💡 CONTOH PENGGUNAAN:
!cloud s3          → Scan AWS S3 buckets only
!cloud firebase    → Scan Firebase databases only
!cloud gcs         → Scan Google Cloud Storage only
!cloud all         → Scan SEMUA cloud providers

⚠️ DATA YANG SERING KEBOCORAN:
• Database backup (.sql, .dump)
• Config file (.env, credentials.json)
• User data (CSV, Excel dengan data pelanggan)
• Log file (bisa ada password/API key)
• Source code backup""",

            "wp": """WordPress Security Scanner - Montir khusus buat website WordPress!

🎯 APA TUJUANNYA?
WordPress itu platform website PALING POPULER di dunia (30%+ website):
• Karena saking populernya, BANYAK hacker yang nyari celah WP
• Tool ini khusus audit keamanan WordPress

1. VERSION DETECTION - Tau versi WP yang dipake
   • Versi lama = BANYAK celah keamanan
   • Info ini penting buat milih exploit yang cocok

2. PLUGIN SCANNER - Cek plugin yang terinstall
   • Scan 50+ plugin populer yang sering vulnerable
   • Elementor, Contact Form 7, WooCommerce, dll
   • Plugin outdated = PINTU MASUK hacker!

3. USER ENUMERATION - Daftar user yang ada
   • Lewat author ID di URL
   • Lewat REST API
   • Buat brute force login lebih akurat

4. FILE DETECTION - Cari file sensitif
   • wp-config.php (database password!)
   • Backup files
   • Debug logs
   • Upload directories

💡 CONTOH PENGGUNAAN:
!wp version        → Check WP version only
!wp plugins        → Scan installed plugins
!wp users          → Enumerate users
!wp files          → Check sensitive files
!wp all            → SEMUA audit WordPress (recommended)

⚠️ PLUGIN YANG SERING VULNERABLE:
• Contact Form 7
• Elementor
• WooCommerce
• WP Forms
• All-in-One WP Migration""",

            "wordpress": """WordPress Security Scanner - Montir khusus buat website WordPress!

🎯 APA TUJUANNYA?
WordPress itu platform website PALING POPULER di dunia (30%+ website):
• Karena saking populernya, BANYAK hacker yang nyari celah WP
• Tool ini khusus audit keamanan WordPress
• Alias untuk !wp (sama fungsinya)

1. VERSION DETECTION - Tau versi WP yang dipake
   • Versi lama = BANYAK celah keamanan
   • Info ini penting buat milih exploit yang cocok

2. PLUGIN SCANNER - Cek plugin yang terinstall
   • Scan 50+ plugin populer yang sering vulnerable
   • Elementor, Contact Form 7, WooCommerce, dll
   • Plugin outdated = PINTU MASUK hacker!

3. USER ENUMERATION - Daftar user yang ada
   • Lewat author ID di URL
   • Lewat REST API
   • Buat brute force login lebih akurat

4. FILE DETECTION - Cari file sensitif
   • wp-config.php (database password!)
   • Backup files
   • Debug logs
   • Upload directories

💡 CONTOH PENGGUNAAN:
!wordpress version   → Check WP version only
!wordpress plugins   → Scan installed plugins
!wordpress users     → Enumerate users
!wordpress files     → Check sensitive files
!wordpress all       → SEMUA audit WordPress (recommended)

⚠️ PLUGIN YANG SERING VULNERABLE:
• Contact Form 7
• Elementor
• WooCommerce
• WP Forms
• All-in-One WP Migration""",

            "sqlmap": """SQLMap - Automatic SQL Injection tool!

🎯 APA TUJUANNYA?
Tool LEGENDARIS buat SQL injection automation:
• Detect SQL injection vulnerabilities
• Exploit injection automatically
• Dump database tables
• Get shell access

📊 FITUR UNGGULAN:

1. AUTOMATIC DETECTION
   • Deteksi SQL injection otomatis
   • Support GET, POST, Cookie, User-Agent
   • Time-based & Error-based detection

2. DATABASE DUMP
   • Download semua tabel
   • Export users & passwords
   • Get admin credentials

3. SHELL ACCESS
   • Upload webshell
   • Get OS shell access
   • Execute commands

💡 CONTOH PENGGUNAAN:
!sqlmap              → Auto-detect SQL injection
!sqlmap --dbs        → Dump all databases
!sqlmap --tables     → List all tables
!sqlmap --dump       → Dump data

⚠️ PERINGATAN:
• Tool ini SANGAT NOISY (pasti ke-detect)
• Bisa crash database kalo salah pake
• HANYA buat authorized testing!""",

            "headers": """Security Headers Auditor - Inspektur safety buat header HTTP!

🎯 APA TUJUANNYA?
Header HTTP itu kayak 'surat keterangan' dari server:
• "Ini lho website saya, pake HTTPS ya!"
• "Jangan coba-coba inject script di sini!"
• "Data user gak boleh di-share ke domain lain!"

📊 6 HEADER KEAMANAN YANG DICEK:

1. HSTS (Strict-Transport-Security) - Paksa HTTPS
   • Tanpa ini: User bisa akses via HTTP (gak aman)
   • Dengan ini: Browser MAKSA pake HTTPS

2. CSP (Content-Security-Policy) - Anti XSS
   • Batasi dari mana script bisa dimuat
   • Kalo ada hacker inject script dari domain lain → DIBLOKIR

3. X-Frame-Options - Anti Clickjacking
   • Mencegah website di-embed di iframe hacker
   • Tanpa ini: Hacker bisa bikin website lu 'dipake' buat phishing

4. X-Content-Type-Options - Anti MIME Sniffing
   • Browser jangan nebak-nebak tipe file
   • File .jpg ya .jpg, bukan .exe yang disamarkan

5. Referrer-Policy - Kontrol Privacy
   • Batasi info yang dikirim ke website lain
   • Jangan sampe URL sensitif kebocoran

6. Permissions-Policy - Kontrol Fitur Browser
   • Matikan fitur yang gak dipake (camera, mic, location)
   • Kurangi attack surface

💡 CONTOH PENGGUNAAN:
!headers           → Scan semua security headers

⚠️ HASIL SCAN:
• ✓ FOUND = Header ada, website AMAN
• ✗ MISSING = Header gak ada, POTENSI BAHAYA!""",

            "cookie": """Cookie Security Auditor - Cek keamanan session cookies!

🎯 APA TUJUANNYA?
Cookie itu kayak 'tiket masuk' ke website:
• Kalo tiketnya dipalsukan, hacker bisa login sebagai user lain
• Tool ini cek apakah cookie diproteksi dengan benar

📊 YANG DICEK:

1. HTTPONLY FLAG
   • Tanpa flag ini: JavaScript bisa baca cookie
   • Dengan flag: Cookie gak bisa diakses via JS (anti XSS cookie theft)

2. SECURE FLAG
   • Tanpa flag: Cookie bisa dikirim via HTTP (unencrypted)
   • Dengan flag: Cookie HANYA via HTTPS (encrypted)

3. SAMESITE FLAG
   • Tanpa flag: Cookie bisa dikirim ke domain lain (CSRF attack)
   • Dengan flag: Cookie HANYA untuk same-site requests

💡 CONTOH PENGGUNAAN:
!cookie            → Audit semua cookies

⚠️ RISIKO:
• Session hijacking (hacker ambil alih akun)
• CSRF attacks (aksi atas nama user)
• Cookie theft via XSS""",

            "form": """Form Input Analyzer - Cek keamanan form input!

🎯 APA TUJUANNYA?
Form input (login, search, contact) itu PINTU MASUK utama buat hacker:
• Tool ini cek apakah input difilter dengan benar
• Bisa di-inject atau gak

📊 YANG DICEK:

1. XSS VULNERABILITY
   • Input form bisa di-inject script JavaScript
   • Contoh: <script>alert('XSS')</script>

2. SQL INJECTION
   • Input bisa di-inject perintah SQL
   • Contoh: ' OR 1=1-- (login tanpa password)

3. COMMAND INJECTION
   • Input bisa di-inject command server
   • Contoh: ; rm -rf / (hapus semua file)

4. PATH TRAVERSAL
   • Input bisa akses file di luar folder yang seharusnya
   • Contoh: ../../etc/passwd

💡 CONTOH PENGGUNAAN:
!form              → Analyze semua form di halaman

⚠️ FORM YANG SERING VULNERABLE:
• Login forms
• Search boxes
• Contact forms
• File upload forms
• Comment sections""",

            "git": """Git Exposure Detector - Cek apakah folder .git kebuka publik!

🎯 APA TUJUANNYA?
Folder .git itu 'otak' dari version control:
• Berisi SEMUA history code
• Berisi commit messages
• Kadang berisi password & API keys yang pernah di-commit
• Kalo kebuka publik = BENCANA!

📊 YANG BISA KEBOCORAN:
• Source code lengkap
• Database credentials
• API keys & secrets
• Email developer
• Internal documentation
• Password yang pernah di-commit (meski udah dihapus!)

💡 CONTOH PENGGUNAAN:
!git check         → Check apakah .git folder accessible
!git deep          → Deep scan, coba download metadata

⚠️ CARA HACKER EKSPLOITASI:
1. Akses /.git/config
2. Download semua objects
3. Reconstruct source code
4. Cari credentials di history
5. BOOM! Full access!""",

            "dirb": """Directory Bruteforce Scanner - Nyari folder/file tersembunyi!

🎯 APA TUJUANNYA?
Website punya BANYAK folder/file yang gak ke-link di homepage:
• /admin (dashboard admin)
• /backup (database backup)
• /.env (config file dengan password)
• /phpinfo.php (info server lengkap)
• /wp-config.php (WordPress config)

📊 CARA KERJA:
• Tool ini 'ngetok' ribuan kemungkinan folder/file
• Pake wordlist dengan nama-nama umum
• Kalo ada response (200, 301, 403) = FOUND!

💡 CONTOH PENGGUNAAN:
!dirb common       → Scan folder umum (cepat)
!dirb deep         → Scan lebih banyak folder (lambat tapi lengkap)

⚠️ FILE YANG SERING KEBOCORAN:
• .env (database password, API keys)
• .git/config (source code history)
• backup.sql (database dump)
• config.php (configuration)
• wp-config.php (WordPress config)""",

            "payload": """Payload Generator - Pabrik senjata buat penetration testing!

🎯 APA TUJUANNYA?
Bikin 'peluru' khusus buat nembus celah keamanan:

📊 JENIS PAYLOAD:

1. XSS (Cross-Site Scripting)
   • <script>alert(1)</script>
   • <img src=x onerror=alert('XSS')>
   • <svg/onload=alert('XSS')>

2. SQL Injection
   • ' OR 1=1--
   • admin' --
   • ' UNION SELECT 1,2,3--

3. Command Injection (RCE)
   • ; id
   • | whoami
   • `sleep 5`

4. SSTI (Server-Side Template Injection)
   • {{7*7}}
   • ${7*7}
   • <%= 7*7 %>

5. CRLF Injection
   • %0d%0aSet-Cookie:crlf=1
   • \\r\\nLocation: http://attacker.com

💡 CONTOH PENGGUNAAN:
!payload encode base64 admin    → Encode 'admin' ke Base64
!payload decode base64 YWRtaW4= → Decode Base64 ke 'admin'
!payload encode url hello world → Encode ke URL format

⚠️ SEMUA PAYLOAD DI-ENCODE JUGA:
• Base64
• URL Encode
• Hex
• Binary""",

            "stress": """Stress Testing Engine - Uji kekuatan server dengan beban berat!

🎯 APA TUJUANNYA?
Kayak stress test jembatan - kita uji apakah website bisa nahan beban:
• Normalnya: 10-100 pengunjung per menit
• Stress test: Kita datengin 1000+ pengunjung bareng-bareng

TUJUANNYA BUKAN buat nge-DDoS (itu ilegal!), tapi:
• Tau batas maksimal server
• Cari tau apakah ada proteksi DDoS
• Liat gimana website behave under pressure

📊 CARA KERJA:

1. MULTI-THREADING - Ribuan koneksi paralel
   • Setiap thread = 1 'pengunjung'
   • 50 threads = 50 pengunjung bareng-bareng
   • Bisa sampe 500+ threads

2. REQUEST FLOOD - Banjir request
   • Tiap thread kirim request terus-terusan
   • Server bakal kewalahan kalo gak kuat

3. CACHE BYPASS - Tembus proteksi
   • Pake IP random biar gak kebanned
   • Cache buster biar gak dilayanin dari cache
   • User-Agent random biar kayak banyak device berbeda

💡 CONTOH PENGGUNAAN:
!stress 50 30      → 50 threads, 30 detik
!stress 100 60     → 100 threads, 60 detik
!stress 200 0      → 200 threads, unlimited (STOP dengan Ctrl+C)

⚠️ PERINGATAN:
• Cuma pake di website LU SENDIRI atau yang ada IJIN TERTULIS!
• Bisa bikin server DOWN
• ILEGAL kalo pake di website orang lain!""",

            "evil": """EvilLimiter - Network Control Tool buat WiFi!

🎯 APA TUJUANNYA?
Tool ini bisa NGONTROL device lain yang connect ke WiFi yang sama:
• Limit bandwidth (buat internetan lemot)
• Putus koneksi (buat dia disconnect dari WiFi)
• Monitor traffic (intip data yang lalu-lalang)

⚙️ CARA KERJANYA?

1. ARP SPOOFING - Jadi 'perantara' jahat
   • Normalnya: HP → Router → Internet
   • Setelah di-spoof: HP → KOMPUTER LU → Router → Internet
   • Sekarang lu di tengah-tengah (Man-in-the-Middle!)

2. BANDWIDTH LIMITING - Kasih 'rem' ke target
   • Upload dibatesin (misal: cuma 5kbit/detik)
   • Download dibatesin (misal: cuma 10kbit/detik)
   • Target bakal ngerasa internetan super lemot

3. CONNECTION KILLER - Putusin koneksi
   • ARP method: Banjirin target ARP response palsu
   • SYN method: Spam port target sampe error
   • Target: "Kok WiFi-nya disconnect terus ya?"

4. TRAFFIC MONITORING - Intip lalu-lalang data
   • Hitung jumlah packet
   • Liat berapa bytes yang lewat
   • Deteksi HTTP vs HTTPS traffic

💡 CONTOH PENGGUNAAN:
!scanlan                      → Scan WiFi, liat siapa aja yang connect
!evil 192.168.1.100 10kbit    → Limit bandwidth target
!kill 192.168.1.100           → Putusin koneksi target
!monitor 192.168.1.100 30     → Monitor traffic 30 detik

⚠️ PERINGATAN KERAS:
• HANYA pake di jaringan LU SENDIRI!
• Atau jaringan yang ADA IJIN TERTULIS dari pemilik
• Pake di WiFi orang lain = ILEGAL (UU ITE!)
• Bisa kena pasal hacking & unauthorized access""",

            "scanlan": """Network Scanner - Scan WiFi buat liat semua device yang connect!

🎯 APA TUJUANNYA?
• Liat siapa aja yang connect ke WiFi yang sama
• Tau IP address, MAC address, dan hostname tiap device
• Identifikasi device yang mencurigakan

📊 INFO YANG DIDAPAT:
• IP Address (192.168.1.xxx)
• MAC Address (AA:BB:CC:DD:EE:FF)
• Hostname (iPhone-John, Laptop-Admin, dll)

💡 CONTOH PENGGUNAAN:
!scanlan           → Scan seluruh jaringan lokal

⚠️ CARA PAKAI:
1. Pastikan connect ke WiFi target
2. Jalankan !scanlan
3. Tunggu hasil scan (5-30 detik)
4. Liat daftar device
5. Pilih target buat attack""",

            "kill": """Connection Killer - Putus koneksi target dari WiFi!

🎯 APA TUJUANNYA?
• Disconnect device dari WiFi tanpa password
• Ganggu koneksi hacker/attacker
• Test ketahanan network

📊 METHOD YANG TERSEDIA:

1. ARP METHOD (Default)
   • Banjirin target ARP response palsu
   • Target bingung, disconnect sendiri
   • Lebih stealth, gak terlalu noisy

2. SYN METHOD
   • Spam port target dengan SYN packets
   • Port error, connection drop
   • Lebih aggressive, lebih cepat detect

💡 CONTOH PENGGUNAAN:
!kill 192.168.1.100              → Disconnect target (ARP method)
!kill 192.168.1.100 arp          → Disconnect dengan ARP
!kill 192.168.1.100 syn          → Disconnect dengan SYN

⚠️ PERINGATAN:
• HANYA pake di jaringan sendiri!
• Bisa ganggu koneksi penting
• ILEGAL kalo pake di WiFi orang lain!""",

            "monitor": """Traffic Monitor - Intip data yang lalu-lalang di jaringan!

🎯 APA TUJUANNYA?
• Monitor traffic jaringan real-time
• Liat berapa banyak data yang dikirim
• Deteksi jenis traffic (HTTP, HTTPS, dll)

📊 STATISTIK YANG DIDAPAT:
• Total Packets - Jumlah packet yang lewat
• Total Bytes - Jumlah data (bytes)
• TCP Packets - Traffic TCP
• UDP Packets - Traffic UDP
• ICMP Packets - Ping/ICMP traffic
• HTTP Traffic - Unencrypted web traffic
• HTTPS Traffic - Encrypted web traffic

💡 CONTOH PENGGUNAAN:
!monitor                       → Monitor semua traffic (10 detik)
!monitor 192.168.1.100         → Monitor target spesifik (10 detik)
!monitor 192.168.1.100 30      → Monitor target 30 detik

⚠️ CATATAN:
• HTTPS traffic ter-enkripsi, gak bisa baca isi
• HTTP traffic BISA dibaca isinya (cookie, password, dll)
• Butuh scapy untuk full functionality""",

            # ========== WIFI HACKING TOOLS ==========
            "aircrack": """Aircrack-ng - WiFi WEP/WPA2 Password Cracker!

🎯 APA TUJUANNYA?
Crack password WiFi dari captured handshake (.cap file)

📊 CARA KERJA:
• Analisis capture file dari airodump-ng
• Brute-force password dengan wordlist
• Support WEP dan WPA/WPA2

💡 CONTOH PENGGUNAAN:
!aircrack capture.cap        → Crack file capture.cap
!aircrack handshake.cap      → Crack handshake WiFi

⚠️ CATATAN:
• Butuh file .cap dari airodump-ng
• Butuh wordlist yang bagus (rockyou.txt)
• Proses bisa lama tergantung wordlist""",

            "airodump": """Airodump-ng - WiFi Packet Capture!

🎯 APA TUJUANNYA?
Capture WiFi packets buat disimpan ke file .cap

📊 INFO YANG DIDAPAT:
• BSSID (MAC Address AP)
• ESSID (Nama WiFi)
• Channel
• Encryption (WEP/WPA/WPA2)
• Connected clients

💡 CONTOH PENGGUNAAN:
!airodump wlan0mon           → Capture packets
!airodump                    → Default interface

⚠️ CATATAN:
• Butuh monitor mode (wlan0mon)
• File .cap disimpan otomatis
• Gunakan dengan aircrack-ng""",

            "aireplay": """Aireplay-ng - WiFi Packet Injection!

🎯 APA TUJUANNYA?
Inject packets ke jaringan WiFi target

📊 SERANGAN YANG TERSEDIA:
• Deauthentication (putusin koneksi client)
• Fake Authentication
• ARP Request Replay
• Fragmentation Attack

💡 CONTOH PENGGUNAAN:
!aireplay deauth             → Deauth attack
!aireplay                    → Default attack

⚠️ CATATAN:
• Butuh monitor mode
• Deauth = putusin koneksi client dari AP
• Client bakal reconnect, handshake bisa dicapture""",

            "wash": """Wash - WPS Scanner!

🎯 APA TUJUANNYA?
Scan dan identifikasi jaringan dengan WPS enabled

📊 INFO YANG DIDAPAT:
• BSSID target
• ESSID (nama WiFi)
• WPS version
• Lock status (locked/unlocked)

💡 CONTOH PENGGUNAAN:
!wash wlan0mon               → Scan WPS networks
!wash                        → Default scan

⚠️ CATATAN:
• Butuh monitor mode
• Target WiFi dengan WPS enabled
• Gunakan dengan reaver/bully""",

            "reaver": """Reaver - WPS PIN Cracker!

🎯 APA TUJUANNYA?
Brute-force WPS PIN buat dapet password WiFi

📊 CARA KERJA:
• Exploit WPS design flaw
• Brute-force PIN (11 digit)
• Recover WPA passphrase

💡 CONTOH PENGGUNAAN:
!reaver AA:BB:CC:DD:EE:FF    → Attack target BSSID
!reaver                      → Default target

⚠️ CATATAN:
• Bisa makan waktu 4-10 JAM!
• Target harus WPS enabled
• Beberapa router punya WPS lock""",

            "bully": """Bully - WPS PIN Cracker (Alternative)!

🎯 APA TUJUANNYA?
Alternative to Reaver untuk WPS cracking

📊 KEUNGGULAN:
• Lebih ringan dari Reaver
• Support lebih banyak options
• Better error handling

💡 CONTOH PENGGUNAAN:
!bully AA:BB:CC:DD:EE:FF     → Attack target
!bully                       → Default target

⚠️ CATATAN:
• Sama seperti Reaver
• Butuh WPS enabled target
• Proses bisa lama""",

            "mdk3": """MDK3 - WiFi DoS Tool!

🎯 APA TUJUANNYA?
Denial of Service attack ke jaringan WiFi

📊 MODE SERANGAN:
• D (Deauthentication) - Putusin semua client
• B (Beacon flood) - Fake AP spam
• M (Michael shutdown) - TKIP attack
• P (Probe request) - SSID discovery

💡 CONTOH PENGGUNAAN:
!mdk3 deauth                 → Deauth attack
!mdk3                        → Default attack

⚠️ CATATAN:
• SANGAT DESTRUCTIVE!
• Bisa bikin down seluruh jaringan
• ILEGAL tanpa ijin!""",

            "mdk4": """MDK4 - WiFi DoS Tool (Updated)!

🎯 APA TUJUANNYA?
Updated version dari MDK3

📊 PERBAIKAN:
• Better performance
• More stable
• Newer attack vectors

💡 CONTOH PENGGUNAAN:
!mdk4 deauth                 → Deauth attack
!mdk4                        → Default attack

⚠️ CATATAN:
• Sama seperti MDK3
• Lebih powerful
• Gunakan dengan hati-hati!""",

            "kismet": """Kismet - WiFi Detector/Sniffer!

🎯 APA TUJUANNYA?
Detect dan sniff semua WiFi networks di area

📊 FITUR:
• Passive WiFi detection
• Hidden SSID discovery
• Channel hopping
• GPS logging

💡 CONTOH PENGGUNAAN:
!kismet wlan0                → Detect networks
!kismet                      → Default interface

⚠️ CATATAN:
• Passive detection (stealth)
• Bisa detect hidden SSID
• Support GPS mapping""",

            "wigle": """Wigle - WiFi Mapping (API)!

🎯 APA TUJUANNYA?
Search WiFi networks dari Wigle.net database

📊 INFO YANG DIDAPAT:
• Network location
• SSID & BSSID
• Encryption type
• Last seen time

💡 CONTOH PENGGUNAAN:
!wigle network               → Search networks
!wigle                       → Default search

⚠️ CATATAN:
• Butuh Wigle.net API key
• Online database
• Global WiFi mapping""",

            "macchanger": """Macchanger - MAC Address Changer!

🎯 APA TUJUANNYA?
Change MAC address untuk anonymity

📊 FUNGSI:
• Random MAC generation
• Vendor-specific MAC
• Reset to original

💡 CONTOH PENGGUNAAN:
!macchanger wlan0            → Change MAC
!macchanger                  → Default interface

⚠️ CATATAN:
• Untuk anonymity
• Bypass MAC filtering
• Reset setelah reboot""",

            "ifconfig": """Ifconfig - Network Interface Config!

🎯 APA TUJUANNYA?
View/configure network interfaces

📊 INFO YANG DIDAPAT:
• IP address
• Netmask
• MAC address
• Interface status

💡 CONTOH PENGGUNAAN:
!ifconfig wlan0              → Show interface
!ifconfig                    → All interfaces

⚠️ CATATAN:
• Basic network tool
• View interface info
• Configure IP/MAC""",

            "iwconfig": """Iwconfig - Wireless Interface Config!

🎯 APA TUJUANNYA?
Configure wireless interfaces

📊 INFO YANG DIDAPAT:
• ESSID (network name)
• Mode (Managed/Monitor)
• Frequency/Channel
• Signal level
• Encryption key

💡 CONTOH PENGGUNAAN:
!iwconfig wlan0              → Show wireless info
!iwconfig                    → All wireless

⚠️ CATATAN:
• Wireless-specific tool
• Check monitor mode status
• View signal strength""",

            "rfkill": """Rfkill - WiFi Blocker/Unblocker!

🎯 APA TUJUANNYA?
Block/unblock wireless devices

📊 FUNGSI:
• List blocked devices
• Unblock WiFi
• Block WiFi
• Check kill switch

💡 CONTOH PENGGUNAAN:
!rfkill list                 → List devices
!rfkill unblock all          → Unblock all
!rfkill                      → Default (list)

⚠️ CATATAN:
• Hardware/software block
• Check if WiFi is blocked
• Unblock if needed""",

            "hashcat": """Hashcat - GPU Password Cracker!

🎯 APA TUJUANNYA?
Crack password hashes dengan GPU acceleration

📊 SUPPORT:
• WPA/WPA2 handshakes
• MD5, SHA1, SHA256
• NTLM hashes
• 300+ hash types

💡 CONTOH PENGGUNAAN:
!hashcat handshake.hccapx    → Crack WiFi
!hashcat hash.txt            → Crack hashes

⚠️ CATATAN:
• Butuh GPU (NVIDIA/AMD)
• Sangat cepat (jutaan/sec)
• Support wordlist rules""",

            "john": """John the Ripper - Password Cracker!

🎯 APA TUJUANNYA?
Classic password cracking tool

📊 FITUR:
• Auto-detect hash type
• Dictionary attacks
• Brute-force mode
• Rule-based cracking

💡 CONTOH PENGGUNAAN:
!john hash.txt               → Crack hashes
!john                        → Default

⚠️ CATATAN:
• CPU-based cracking
• Slower than hashcat
• Very reliable""",

            "script": """Script Library - Gudang senjata 100+ payload siap pakai!

🎯 APA TUJUANNYA?
Kumpulan payload lengkap untuk berbagai situasi:

📁 KATEGORI PAYLOAD:

1. XSS (Cross-Site Scripting) - 20+ varian
   • Basic, IMG Tag, SVG, Cookie Stealer, dll

2. SQL Injection - 15+ varian
   • Basic, UNION SELECT, Blind SQLi, Time-based

3. Command Injection - 10+ varian
   • Linux, Windows, Reverse Shell

4. SSTI (Server-Side Template Injection)
   • Jinja2, Twig, Freemarker

5. LFI/RFI (File Inclusion)
   • Local File Inclusion
   • Remote File Inclusion

6. XXE (XML External Entity)
   • XML injection payloads

🎯 FITUR UNGGULAN:
• DRAG & DROP - Tinggal drag script ke desktop
• PREVIEW - Liat isi script sebelum dipake
• SEARCH - Cari payload berdasarkan nama/kategori
• RISK LEVEL - Label bahaya (Low/Medium/High/Critical)
• SEND TO TERMINAL - Kirim payload langsung ke terminal
• GENERATE FILE - Save script ke folder

💡 CONTOH PENGGUNAAN:
!script XSS          → Liat semua payload XSS
!script SQLi         → Liat semua payload SQL Injection
!script              → Liat semua kategori

⚠️ INGAT: Payload ini SENJATA!
• Pake hanya untuk testing yang ADA IJIN
• Jangan pernah pake untuk kejahatan
• Bertanggung jawab atas setiap aksi""",

            "help": """Help System - Panduan lengkap semua command!

🎯 APA TUJUANNYA?
• Liat daftar semua command yang tersedia
• Baca dokumentasi detail tiap tool
• Tau syntax dan contoh penggunaan

💡 CONTOH PENGGUNAAN:
!help                → Liat SEMUA command
!help nmap           → Dokumentasi nmap
!help evil           → Dokumentasi EvilLimiter
!help vuln           → Dokumentasi vulnerability scanner

⚠️ TIP:
• Ketik !help [nama_tool] buat info detail
• Semua command ada di tab 'How to Use'
• Tab 'Roadmap' kasih panduan step-by-step""",

            "webtools": """Web Tools Reference - Katalog 70+ tools pentesting eksternal!

🎯 APA TUJUANNYA?
ApexOmega punya banyak tool bawaan, TAPI kadang lu butuh tool khusus.
Di sini ada referensi 70+ tools eksternal yang bisa lu install:

📁 KATEGORI TOOLS:

🔍 RECONNAISSANCE:
• photon, gospider, hakrawler (crawlers)
• subfinder, theharvester (subdomain hunters)

📁 DIRECTORY SCANNING:
• dirb, dirsearch, gobuster, ffuf (directory bruteforce)

🛡️ VULNERABILITY SCANNING:
• nikto, nuclei, wapiti, skipfish (vulnerability scanners)

💉 INJECTION TOOLS:
• sqlmap (SQL injection)
• commix (command injection)
• xsstrike (XSS detection)

📊 ANALYSIS:
• burpsuite (full pentest platform)
• owasp-zap (free security testing)
• mitmproxy (HTTP proxy)
• wireshark (network analyzer)

🔐 PASSWORD TOOLS:
• cewl (wordlist generator)
• hashcat, john (password crackers)
• hydra (network login cracker)

💡 CONTOH PENGGUNAAN:
!webtools          → Liat SEMUA referensi tools

⚠️ CATATAN:
• Tools ini EKSTERNAL (harus install sendiri)
• Referensi lengkap ada di tab 'Web Tools Guide'""",

            "cewl": """CeWL (Custom Word List) - Generator wordlist dari website target!

🎯 APA TUJUANNYA?
• Bikin wordlist KHUSUS dari kata-kata di website target
• Lebih efektif dari wordlist umum
• Password sering pake kata dari website sendiri!

📊 CARA KERJA:
1. Crawl website target
2. Ambil semua teks/kata
3. Filter kata-kata unik
4. Jadikan wordlist

💡 CONTOH PENGGUNAAN:
!cewl                → Generate wordlist dari homepage

⚠️ TIP:
• Wordlist ini COCOK buat brute force password
• Admin sering pake nama perusahaan/project sebagai password""",

            "dmitry": """DMITRY (Deepmagic Information Gathering) - Tool klasik info gathering!

🎯 APA TUJUANNYA?
• Whois lookup (info domain)
• DNS enumeration
• Email gathering
• Subdomain discovery

💡 CONTOH PENGGUNAAN:
!dmitry              → Run semua module DMITRY

⚠️ CATATAN:
• Tool ini PASSIVE (gak nyentuh server)
• Legal buat dipake""",

            "sslscan": """SSL/TLS Scanner - Cek keamanan sertifikat HTTPS!

🎯 APA TUJUANNYA?
• Cek versi SSL/TLS yang dipake
• Deteksi cipher yang lemah
• Cari vulnerability SSL/TLS

📊 YANG DICEK:
• SSL/TLS version (SSLv3, TLS 1.0, 1.1, 1.2, 1.3)
• Cipher suites
• Certificate validity
• Known vulnerabilities (POODLE, BEAST, dll)

💡 CONTOH PENGGUNAAN:
!sslscan             → Scan SSL/TLS configuration

⚠️ HASIL:
• ✓ Secure = Configuration aman
• ✗ Vulnerable = Ada celah keamanan""",

            "wayback": """Wayback Machine Scraper - Cari URL historis dari website!

🎯 APA TUJUANNYA?
• Internet Archive nyimpen HISTORY website
• URL yang udah dihapus masih ada di Wayback
• Bisa nemu endpoint/file yang udah dihapus

💡 CONTOH PENGGUNAAN:
!wayback             → Fetch URLs dari Wayback Machine

⚠️ TIP:
• Sering nemu /admin, /backup yang udah dihapus
• URL lama mungkin masih accessible""",

            "gau": """GAU (Get All Urls) - Fetch URL dari AlienVault OTX & Wayback!

🎯 APA TUJUANNYA?
• Kumpulin SEMUA URL yang pernah ada dari target
• Sumber: AlienVault OTX, Wayback Machine, Common Crawl
• Lebih lengkap dari wayback aja

💡 CONTOH PENGGUNAAN:
!gau                 → Fetch all known URLs

⚠️ TIP:
• Cocok buat discovery endpoint tersembunyi
• URL yang gak ke-link di website pun bisa ketemu""",

            "dnsenum": """DNS Enumeration - Enumerasi DNS records lengkap!

🎯 APA TUJUANNYA?
• A records (IP addresses)
• MX records (mail servers)
• NS records (name servers)
• TXT records (SPF, DKIM, dll)
• Zone transfer (AXFR)

💡 CONTOH PENGGUNAAN:
!dnsenum             → Enumerate all DNS records

⚠️ TIP:
• Zone transfer yang misconfigured bisa kasih SEMUA DNS records""",

            "fierce": """Fierce Domain Scanner - DNS reconnaissance tool!

🎯 APA TUJUANNYA?
• Zone transfer testing
• Subdomain enumeration
• DNS reconnaissance

💡 CONTOH PENGGUNAAN:
!fierce              → Run Fierce DNS scan

⚠️ CATATAN:
• Zone transfer yang berhasil = dapet semua subdomain""",

            "nikto": """Nikto Web Server Scanner - Scanner LEGENDARIS sejak 2001!

🎯 APA TUJUANNYA?
• Scan 6700+ potentially dangerous files/CGIs
• Check for outdated server software
• Server configuration issues
• 270+ server plugins

💡 CONTOH PENGGUNAAN:
!nikto               → Run Nikto scan

⚠️ CATATAN:
• Tool ini NOISY (pasti ke-detect)
• Tapi SANGAT lengkap""",

            "apacheusers": """Apache Users Enumerator - Cari username dari modul mod_userdir!

🎯 APA TUJUANNYA?
• Apache mod_userdir bisa leak username
• URL: http://target/~username/
• Username ini bisa buat brute force SSH/FTP

💡 CONTOH PENGGUNAAN:
!apacheusers         → Enumerate Apache users

⚠️ TIP:
• Username ini VALID (bukan tebakan)
• Cocok buat brute force""",

            "waf": """WAF Detector - Deteksi Web Application Firewall!

🎯 APA TUJUANNYA?
• Tau apakah target pake WAF
• Identifikasi jenis WAF (Cloudflare, Akamai, dll)
• Penting buat milih exploit yang tepat

📊 WAF YANG DIDETEKSI:
• Cloudflare
• Akamai
• Imperva
• ModSecurity
• Nginx Generic
• Dan lain-lain

💡 CONTOH PENGGUNAAN:
!waf                 → Detect WAF

⚠️ TIP:
• Kalo ada WAF, perlu bypass techniques khusus""",

            "cms": """CMS Detector - Deteksi Content Management System!

🎯 APA TUJUANNYA?
• Identifikasi CMS (Drupal, Joomla, Magento, dll)
• Tau versi CMS
• Penting buat milih exploit yang cocok

💡 CONTOH PENGGUNAAN:
!cms                 → Detect CMS

⚠️ CATATAN:
• WordPress pake !wp (lebih spesifik)""",

            "joomscan": """Joomla Scanner - Audit keamanan Joomla CMS!

🎯 APA TUJUANNYA?
• Joomla version detection
• Vulnerable components
• Configuration issues

💡 CONTOH PENGGUNAAN:
!joomscan            → Scan Joomla site

⚠️ CATATAN:
• Khusus buat Joomla saja""",

            "wapiti": """Wapiti Web Vulnerability Scanner - Scanner injeksi otomatis!

🎯 APA TUJUANNYA?
• SQL Injection
• XSS (Cross-Site Scripting)
• Command Injection
• File Disclosure
• CRLF Injection

💡 CONTOH PENGGUNAAN:
!wapiti              → Run Wapiti scan

⚠️ CATATAN:
• Scanner ini OTOMATIS (gak perlu config)""",

            "webcache": """Web Cache Poisoning Detector - Cek keracunan cache!

🎯 APA TUJUANNYA?
• Deteksi HTTP header yang bisa dimanipulasi
• Cache poisoning attacks
• Web cache deception

💡 CONTOH PENGGUNAAN:
!webcache            → Check web cache vulnerability

⚠️ TIP:
• Cache poisoning bisa affect SEMUA user""",

            "nuclei": """Nuclei - Template-based vulnerability scanner!

🎯 APA TUJUANNYA?
• Scan pake template CVE-known vulnerabilities
• Fast & accurate
• Community templates

💡 CONTOH PENGGUNAAN:
!nuclei              → Run Nuclei scan

⚠️ CATATAN:
• Template-based = sangat akurat""",

            "padbuster": """PadBuster - Padding Oracle attack tool!

🎯 APA TUJUANNYA?
• Padding Oracle attacks
• Decrypt encrypted data
• Cookie decryption

💡 CONTOH PENGGUNAAN:
!padbuster           → Run Padding Oracle test

⚠️ CATATAN:
• Advanced technique, butuh crypto knowledge""",

            "cmdi": """Command Injection Detector - Deteksi injeksi command!

🎯 APA TUJUANNYA?
• Test input forms untuk command injection
• Time-based detection
• Output-based detection

💡 CONTOH PENGGUNAAN:
!cmdi                → Test command injection

⚠️ TIP:
• Command injection = Remote Code Execution!""",

            "davtest": """DAVTest - Test WebDAV file upload!

🎯 APA TUJUANNYA?
• Test WebDAV PUT method
• Upload test files
• Check execution capability

💡 CONTOH PENGGUNAAN:
!davtest             → Test WebDAV upload

⚠️ CATATAN:
• WebDAV yang misconfigured = bisa upload shell""",

            "weevely": """Weevely - PHP Webshell generator!

🎯 APA TUJUANNYA?
• Generate PHP webshell
• Multi-language support
• Obfuscated code

💡 CONTOH PENGGUNAAN:
!weevely             → Generate webshell

⚠️ PERINGATAN:
• HANYA buat testing yang ADA IJIN!
• Webshell = backdoor access""",

            "webacoo": """Webacoo - Cookie-based PHP backdoor!

🎯 APA TUJUANNYA?
• Generate cookie-authenticated backdoor
• Stealth communication
• Multi-command support

💡 CONTOH PENGGUNAAN:
!webacoo             → Generate Webacoo backdoor

⚠️ PERINGATAN:
• HANYA buat authorized testing!""",

            "laudanum": """Laudanum - Collection of injectable code!

🎯 APA TUJUANNYA?
• Kumpulan webshells berbagai bahasa
• PHP, ASP, JSP, dll
• Various obfuscation levels

💡 CONTOH PENGGUNAAN:
!laudanum            → Show available shells

⚠️ CATATAN:
• Reference library saja""",

            "slowhttp": """SlowHTTPTest - Layer 7 DoS test tool!

🎯 APA TUJUANNYA?
• Test Slowloris attack
• HTTP DoS vulnerability
• Connection exhaustion

💡 CONTOH PENGGUNAAN:
!slowhttp            → Test slow HTTP DoS

⚠️ PERINGATAN:
• Bisa bikin server DOWN!
• HANYA buat authorized testing!""",

            "ffuf": """FFUF (Fuzz Faster U Fool) - Fast web fuzzer!

🎯 APA TUJUANNYA:
• Directory brute force
• Virtual host discovery
• Parameter fuzzing
• FAST (Go-based)

💡 CONTOH PENGGUNAAN:
!ffuf                → Run FFUF fuzz

⚠️ CATATAN:
• Sangat cepat, bisa custom wordlist""",

            "wfuzz": """WFuzz - Web application fuzzing tool!

🎯 APA TUJUANNYA:
• Parameter fuzzing
• SQL injection testing
• XSS testing
• Brute force

💡 CONTOH PENGGUNAAN:
!wfuzz               → Run WFuzz test

⚠️ CATATAN:
• Flexible, banyak option""",

            "skipfish": """Skipfish - Web application security scanner!

🎯 APA TUJUANNYA:
• Automated reconnaissance
• Vulnerability detection
• Heuristic analysis

💡 CONTOH PENGGUNAAN:
!skipfish            → Run Skipfish scan

⚠️ CATATAN:
• Comprehensive scan""",

            "urlcrazy": """URLCrazy - Typosquatting detector!

🎯 APA TUJUANNYA:
• Generate domain typos
• Phishing detection
• Brand protection

💡 CONTOH PENGGUNAAN:
!urlcrazy            → Generate typosquats

⚠️ TIP:
• Cocok buat cari phishing domains""",

            "gowitness": """GoWitness - Web screenshot tool!

🎯 APA TUJUANNYA:
• Take screenshots of websites
• Bulk screenshot
• Visual reconnaissance

💡 CONTOH PENGGUNAAN:
!gowitness           → Take screenshot

⚠️ CATATAN:
• Visual proof of concept""",

            "websploit": """WebSploit Framework - All-in-one web attack framework!

🎯 APA TUJUANNYA:
• Multiple attack modules
• Vulnerability scanning
• Exploitation tools

💡 CONTOH PENGGUNAAN:
!websploit           → Run WebSploit

⚠️ CATATAN:
• Framework lengkap""",

            "vhost": """Virtual Host Discovery - Cari website tersembunyi di IP yang sama!

🎯 APA TUJUANNYA:
• Satu IP bisa hosting banyak website
• Virtual host discovery
• Host header injection

💡 CONTOH PENGGUNAAN:
!vhost               → Discover virtual hosts

⚠️ TIP:
• Bisa nemu website admin yang tersembunyi""",

            "webports": """Web Port Scanner - Cari layanan web di port tidak biasa!

🎯 APA TUJUANNYA:
• Scan common web ports (80, 443, 8080, 8443, dll)
• Find hidden web services
• Alternative port discovery

💡 CONTOH PENGGUNAAN:
!webports common     → Scan 10 common ports
!webports full       → Scan 50+ ports

⚠️ TIP:
• Admin panel sering di port 8080, 8443""",

            "testssl": """TestSSL.sh - Comprehensive SSL/TLS testing!

🎯 APA TUJUANNYA:
• SSL/TLS version check
• Cipher analysis
• Certificate validation
• Known vulnerability detection

💡 CONTOH PENGGUNAAN:
!testssl             → Run TestSSL scan

⚠️ CATATAN:
• Lebih lengkap dari sslscan""",

            "gau": """GAU - Get All URLs from multiple sources!

🎯 APA TUJUANNYA:
• AlienVault OTX
• Wayback Machine
• Common Crawl
• URLScan.io

💡 CONTOH PENGGUNAAN:
!gau                 → Fetch all URLs

⚠️ TIP:
• Lengkap banget buat discovery""",
        }

        # * Pemetaan Detail Format Parameter Panggilan
        self.usageDatabase: Dict[str, Dict[str, Any]] = {
            "recon": {
                "syntax": "!recon [quick|deep|full]",
                "modes": {
                    "quick": "IP + Resolusi Jejak (standar)",
                    "deep": "Quick + WHOIS data terbuka",
                    "full": "Deep + Enumerasi Teknologi Ekstra"
                },
                "examples": ["!recon", "!recon quick", "!recon deep"]
            },
            "nmap": {
                "syntax": "!nmap [port1,port2,port3]",
                "modes": {
                    "-": "Sistem standar 10 port (80, 443, dll)",
                    "custom": "Daftar manual port sasaran berset koma"
                },
                "examples": ["!nmap", "!nmap 80,443", "!nmap 22,3306"]
            },
            "vuln": {
                "syntax": "!vuln [full|cors|ssti|crlf|host|upload|paths]",
                "modes": {
                    "full": "Menjalankan seluruh tipe pemindaian",
                    "cors": "Audit kesalahan parameter CORS",
                    "paths": "Pemindaian daftar direktori terlarang otomatis"
                },
                "examples": ["!vuln", "!vuln cors", "!vuln paths"]
            },
            "api": {
                "syntax": "!api [fuzz|methods|all]",
                "modes": {
                    "fuzz": "Mendeteksi endpoint API standar industri",
                    "methods": "Identifikasi HTTP options dan keamanan restriksi methods"
                },
                "examples": ["!api", "!api fuzz", "!api all"]
            },
            "cloud": {
                "syntax": "!cloud [s3|firebase|gcs|all]",
                "modes": {
                    "s3": "Pemeriksaan klaster khusus penyimpanan S3 AWS",
                    "all": "Memindai seluruh peladen cloud major otomatis"
                },
                "examples": ["!cloud", "!cloud s3"]
            },
            "dirb": {
                "syntax": "!dirb [common|deep]",
                "modes": {
                    "common": "Menelusuri direktori inti wajar (standar tinggi)",
                    "deep": "Menelusuri direktori ekstensif"
                },
                "examples": ["!dirb", "!dirb deep"]
            },
            "git": {
                "syntax": "!git [check|deep]",
                "modes": {
                    "check": "Audit identifikasi folder /.git standar",
                    "deep": "Pendalaman dengan verifikasi pembacaan metadata"
                },
                "examples": ["!git", "!git check", "!git deep"]
            },
            "wp": {
                "syntax": "!wp [version|plugins|users|files|all]",
                "modes": {
                    "plugins": "Enumerasi modul instalasi aktif terbaca",
                    "users": "Identifikasi pengguna WP via fitur REST API",
                    "all": "Eksekusi penuh penilaian postur keamanan WP"
                },
                "examples": ["!wp", "!wp plugins", "!wp all"]
            },
            "payload": {
                "syntax": "!payload [encode|decode] [format] [text]",
                "modes": {
                    "encode": "Persenyawaan teks asli ke pelbagai model sandi ASCII/Base64/URL",
                    "decode": "Dekompresi kembali sandi berekstensi ke plain text"
                },
                "examples": ["!payload encode admin", "!payload decode base64 YWRtaW4="]
            },
            "stress": {
                "syntax": "!stress <jumlah_utas> <durasi_detik>",
                "modes": {
                    "<threads>": "Rentang pekerja paralel koneksi",
                    "<duration>": "Ambang waktu aktif (0=tak terhingga)"
                },
                "examples": ["!stress 50 15", "!stress 100 0"]
            },
            "help": {
                "syntax": "!help [nama_perintah]",
                "modes": {
                    "-": "Melihat fungsi umum global",
                    "tool_name": "Rujukan terarah detail per pustaka"
                },
                "examples": ["!help", "!help nmap", "!help vulns"]
            },
            "evil": {
                "syntax": "!evil <target_ip> [upload_limit] [download_limit]",
                "modes": {
                    "<target_ip>": "Alamat IP target dalam jaringan lokal",
                    "<upload_limit>": "Batas upload (contoh: 5kbit, 10kbit, 1mbit)",
                    "<download_limit>": "Batas download (contoh: 10kbit, 20kbit, 2mbit)"
                },
                "examples": ["!evil 192.168.1.100", "!evil 192.168.1.100 10kbit 20kbit"]
            },
            "scanlan": {
                "syntax": "!scanlan",
                "modes": {
                    "-": "Scan otomatis seluruh device dalam jaringan lokal"
                },
                "examples": ["!scanlan"]
            },
            "kill": {
                "syntax": "!kill <target_ip> [arp|syn]",
                "modes": {
                    "<target_ip>": "Alamat IP target yang akan di-disconnect",
                    "arp": "Method ARP spoofing (default)",
                    "syn": "Method SYN flood ke open ports"
                },
                "examples": ["!kill 192.168.1.100", "!kill 192.168.1.100 arp", "!kill 192.168.1.100 syn"]
            },
            "monitor": {
                "syntax": "!monitor [target_ip] [duration]",
                "modes": {
                    "<target_ip>": "IP target spesifik (opsional, kosong = semua)",
                    "<duration>": "Durasi monitoring dalam detik (default: 10)"
                },
                "examples": ["!monitor", "!monitor 192.168.1.100", "!monitor 192.168.1.100 30"]
            },
            # WiFi Tools
            "aircrack": {
                "syntax": "!aircrack [capture_file.cap]",
                "modes": {
                    "<capture_file>": "File .cap dari airodump-ng capture"
                },
                "examples": ["!aircrack capture.cap", "!aircrack handshake.cap"]
            },
            "airodump": {
                "syntax": "!airodump [interface]",
                "modes": {
                    "<interface>": "Wireless interface (default: wlan0mon)"
                },
                "examples": ["!airodump wlan0mon", "!airodump"]
            },
            "aireplay": {
                "syntax": "!aireplay [attack_type] [target_bssid]",
                "modes": {
                    "<attack_type>": "Attack type (default: deauth)",
                    "<target_bssid>": "Target BSSID (optional)"
                },
                "examples": ["!aireplay deauth", "!aireplay"]
            },
            "wash": {
                "syntax": "!wash [interface]",
                "modes": {
                    "<interface>": "Wireless interface in monitor mode"
                },
                "examples": ["!wash wlan0mon", "!wash"]
            },
            "reaver": {
                "syntax": "!reaver [target_bssid]",
                "modes": {
                    "<target_bssid>": "BSSID target WiFi"
                },
                "examples": ["!reaver AA:BB:CC:DD:EE:FF", "!reaver"]
            },
            "bully": {
                "syntax": "!bully [target_bssid]",
                "modes": {
                    "<target_bssid>": "BSSID target WiFi"
                },
                "examples": ["!bully AA:BB:CC:DD:EE:FF", "!bully"]
            },
            "mdk3": {
                "syntax": "!mdk3 [attack_type] [target]",
                "modes": {
                    "<attack_type>": "Attack mode (default: deauth)",
                    "<target>": "Target BSSID or 'all'"
                },
                "examples": ["!mdk3 deauth", "!mdk3"]
            },
            "mdk4": {
                "syntax": "!mdk4 [attack_type] [target]",
                "modes": {
                    "<attack_type>": "Attack mode (default: deauth)",
                    "<target>": "Target BSSID or 'all'"
                },
                "examples": ["!mdk4 deauth", "!mdk4"]
            },
            "kismet": {
                "syntax": "!kismet [interface]",
                "modes": {
                    "<interface>": "Wireless interface (default: wlan0)"
                },
                "examples": ["!kismet wlan0", "!kismet"]
            },
            "wigle": {
                "syntax": "!wigle [search_query]",
                "modes": {
                    "<search_query>": "Search term for Wigle.net"
                },
                "examples": ["!wigle network", "!wigle"]
            },
            "macchanger": {
                "syntax": "!macchanger [interface]",
                "modes": {
                    "<interface>": "Network interface to change MAC"
                },
                "examples": ["!macchanger wlan0", "!macchanger"]
            },
            "ifconfig": {
                "syntax": "!ifconfig [interface]",
                "modes": {
                    "<interface>": "Network interface (optional, show all if empty)"
                },
                "examples": ["!ifconfig wlan0", "!ifconfig"]
            },
            "iwconfig": {
                "syntax": "!iwconfig [interface]",
                "modes": {
                    "<interface>": "Wireless interface (optional)"
                },
                "examples": ["!iwconfig wlan0", "!iwconfig"]
            },
            "rfkill": {
                "syntax": "!rfkill [list|unblock all]",
                "modes": {
                    "list": "List all blocked/unblocked devices",
                    "unblock all": "Unblock all wireless devices"
                },
                "examples": ["!rfkill list", "!rfkill unblock all", "!rfkill"]
            },
            "hashcat": {
                "syntax": "!hashcat [hash_file] [wordlist]",
                "modes": {
                    "<hash_file>": "Hash file to crack",
                    "<wordlist>": "Wordlist file (default: rockyou.txt)"
                },
                "examples": ["!hashcat handshake.hccapx", "!hashcat hash.txt"]
            },
            "john": {
                "syntax": "!john [hash_file]",
                "modes": {
                    "<hash_file>": "Hash file to crack"
                },
                "examples": ["!john hash.txt", "!john"]
            }
        }

        # * Panduan Metodologi Dasar Pemindaian
        self.roadmap: List[str] = [
            "Fase 1: Reconnaissance (!recon) - Melakukan pengumpulan data dasar seperti IP Resolusi dan pencatatan publik (WHOIS) sebagai kerangka pemetaan peladen.",
            "Fase 2: Pemindaian Infrastruktur (!nmap / !dmitry) - Menemukan keterbukaan pintu lalu lintas jaringan untuk mengenali permukaan serangan target.",
            "Fase 3: Pemetaan Konten (!dirb / !subdomain / !api) - Enumerasi sumber daya dan modul tersembunyi seperti direktori administratif maupun titik akhir layanan antarmuka sistem.",
            "Fase 4: Penilaian Kerentanan Aplikasi (!vuln / !webaudit / !wp) - Pengukuran aspek keamanan per fitur aplikasi yang dapat mengekspos kelalaian validasi otorisasi lintas origin atau identifikasi arsitektur berbasis risiko.",
            "Fase 5: Uji Pertahanan Aplikasi Web (!waf / !headers / !cookie) - Menguji filter sistem proteksi serta audit lapisan perlindungan transport protokol jaringan peladen."
        ]

    def getSteps(self) -> List[str]:
        """Pemberian tahapan tambahan, dapat dikustomisasi bila dibutuhkan."""
        return []

    def getRoadmap(self) -> List[str]:
        """Mengambil narasi pedoman evaluasi pentest keamanan."""
        return self.roadmap

    def getUsage(self, toolName: str) -> Optional[Dict[str, Any]]:
        """Membaca detail fungsi dari suatu modul keamanan.
        
        Args:
            toolName: Nama perintah modul target.
            
        Returns:
            Log konvensi pemanggilan modul beserta contoh referensi.
        """
        return self.usageDatabase.get(toolName.lower())

    def searchHelp(self, query: str) -> Dict[str, str]:
        """Pencarian deskripsi dalam basis pustaka modul.
        
        Args:
            query: Untaian string kueri pertanyaan.
            
        Returns:
            Dictionary perolehan hasil pencarian modul relevan.
        """
        query = query.lower()
        results = {}
        for k, v in self.helpDatabase.items():
            if query in k or query in v.lower():
                results[k] = v
        return results
