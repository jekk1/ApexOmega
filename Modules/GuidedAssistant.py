# * Pustaka Tool Pentester (v5.9 Shell Edition - Child Commands)
class GuidedAssistant:
    def __init__(self):
        # * Database Bantuan v5.9 (Full Child Command Edition)
        self.helpDatabase = {
            "recon": "Reconnaissance tahap stalking pro buat cari tau siapa owner target, servernya apa, dan IP aslinya di mana. Tanpa recon lu bakal buta total pas nyerang karena gak tau titik lemah musuh. Pake !recon [mode] buat pilih intensitas: quick (IP+DNS), deep (+WHOIS+AllDNS), atau full (+Tech+CertSubs).",

            "nmap": "Nmap itu senter sakti buat ngelongok isi rumah orang, liat pintu (port) mana yang kebuka atau jendela yang gak dikunci. Sekarang lu bisa tentuin port spesifik: !nmap 80,443,3306. Default scan 10 web ports standar.",

            "subdomain": "Subdomain discovery nyari pintu belakang kayak 'dev.target.com' yang sering dilupain admin. Pake !subdomain brute (wordlist) atau !subdomain passive (crt.sh certificate database).",

            "webaudit": "Web Audit periksa kesehatan website dari WAF detection, tech stack, sampe SQL Injection. Pake !webaudit tech (detect tech only), !webaudit sqli (SQL scan), atau !webaudit full (semua).",

            "vuln": "Vuln Atlas peta harta karun buat cari lubang vulnerability. Bisa scan spesifik: !vuln cors, !vuln ssti, !vuln crlf, !vuln host, !vuln upload, !vuln paths, atau !vuln full (semua sekaligus).",

            "api": "API Auditor spesialis bongkar jalur rahasia REST/GraphQL. Pake !api fuzz (endpoint discovery), !api methods (HTTP method check), atau !api all (kedua-duanya).",

            "cloud": "Cloud Hunter pencium data bocor di storage awan. Filter provider: !cloud s3 (AWS), !cloud firebase, !cloud gcs (Google Cloud), atau !cloud all (scan semua).",

            "stress": "Stress Testing modul buat ngetes mental server target. Format: !stress <threads> <duration_seconds>. Contoh: !stress 200 30 (200 worker selama 30 detik). Duration 0 = infinite.",

            "vhost": "VHost Discovery cari website rahasia yang nebeng di satu IP server sama. Cukup ketik !vhost, otomatis scan dari target aktif.",

            "webports": "WebPorts spesialis cari layanan web di port gak umum. Pake !webports common (10 port standar) atau !webports full (extended range).",

            "wordpress": "WordPress Scanner bongkar mesin CMS paling populer. Pake !wp version, !wp plugins, !wp users, !wp files, atau !wp all (semua scan sekaligus).",

            "wp": "WordPress Scanner bongkar mesin CMS paling populer. Pake !wp version, !wp plugins, !wp users, !wp files, atau !wp all (semua scan sekaligus).",

            "sqlmap": "SQLMap Lite detektor SQL Injection otomatis yang ngetes form input target. Cukup ketik !sqlmap, otomatis scan dari target aktif.",

            "dirb": "Dirb Directory Brute Force nyari folder harta karun tersembunyi. Pake !dirb common (6 path dasar) atau !dirb deep (17+ path lengkap).",

            "payload": "Payload Engine generator encoding otomatis. Pake !payload encode [text] atau !payload decode [format] [text]. Format: base64, hex, url.",

            "headers": "Headers Auditor cek keamanan HTTP headers (CSP, XFO, HSTS, dll). Cukup ketik !headers, otomatis audit 6 header krusial target.",

            "form": "Form Auditor cari parameter input berisiko jadi jalur SQLi/XSS. Cukup ketik !form, otomatis list semua form di landing page target.",

            "cookie": "Cookie Auditor periksa flag keamanan session cookie (HttpOnly, Secure). Cukup ketik !cookie, otomatis audit cookie target.",

            "git": "Git Hunter nyari folder .git bocor yang isinya source code. Pake !git check (exposure check) atau !git deep (coba download content).",

            "script": "Script Library berisi koleksi payload siap pakai (XSS, SQLi, Clickjacking, dll). Pake !script [kategori] buat list payload di terminal. Atau buka tab Scripts buat drag-and-drop.",

            "help": "Ketik !help buat liat semua tools + syntax. Ketik !help [nama_tool] buat liat detail penggunaan spesifik.",
            "cewl": "Tool buat fetch kata-kata dari web target buat wordlist brute-force.",
            "dmitry": "Deepmagic tool buat ngecek open ports dan info DNS.",
            "sslscan": "Scanner SSL/TLS ceritificate dan ciphers.",
            "testssl": "Mirip sslscan, versi alternatif buat audit HTTPS.",
            "wayback": "Tarik endpoint lawas dari Wayback Machine API.",
            "gau": "Get All URLs, tarik history link pake AlienVault OTX.",
            "dnsenum": "Tool enumerasi DNS subdomain otomatis.",
            "fierce": "Scanner keamanan Zone Transfer pada DNS.",
            "nikto": "Scanner web server klasik buat cari CGI aneh atau vulnerability umum.",
            "apacheusers": "Mencari kelemahan module user-dir di server Apache.",
            "waf": "Scanner khusus WAF (Web Application Firewall).",
            "cms": "Scanner CMS khusus selain WordPress (kayak Joomla).",
            "joomscan": "Auditor keamanan khusus untuk CMS Joomla.",
            "wapiti": "Basic URL fuzzer xss/sqli di parameter.",
            "webcache": "Auditor kelemahan web cache poisoning (X-Forwarded-Host).",
            "nuclei": "Scanner CVE cepat pakai template-based payload.",
            "padbuster": "Mendeteksi kelemahan enkripsi sesi Padding Oracle.",
            "cmdi": "Automated Command Injection tester.",
            "davtest": "Audit kelemahan ekstensi HTTP WebDAV upload.",
            "weevely": "Generator stealth PHP webshell standar.",
            "webacoo": "Backdoor PHP lewat integrasi Cookie.",
            "laudanum": "Koleksi referensi standar payload webshell multi-language.",
            "slowhttp": "Stress Testing level layer-7 (DOS DoS/Slowloris).",
            "ffuf": "Fuzzing cepat kilat buat URL discovery.",
            "wfuzz": "Alat injeksi URL param, berguna banget pas webnya statis.",
            "skipfish": "Mendeteksi heuristic error handling server target.",
            "urlcrazy": "Typosquatting web tool buat deteksi phising.",
            "gowitness": "Pengambil cuplikan screenshot secara visual.",
            "webtools": "Daftar panduan lengkap berbagai web pentest tools referensi.",
            "websploit": "Framework wrapper buat nge-test module sekunder sekalian."
        }

        # * Usage Database v5.9 (Syntax + Contoh per Tool)
        self.usageDatabase = {
            "recon": {
                "syntax": "!recon [quick|deep|full]",
                "modes": {
                    "quick": "IP + DNS records (default)",
                    "deep": "Quick + WHOIS + All DNS Records",
                    "full": "Deep + Tech Detection + Certificate Subdomains"
                },
                "examples": ["!recon", "!recon quick", "!recon deep", "!recon full"]
            },
            "nmap": {
                "syntax": "!nmap [port1,port2,port3]",
                "modes": {
                    "(tanpa args)": "Scan 10 web ports standar (80,443,8080,dll)",
                    "custom": "Tentuin port spesifik dipisah koma"
                },
                "examples": ["!nmap", "!nmap 80,443", "!nmap 22,80,443,3306,8080"]
            },
            "vuln": {
                "syntax": "!vuln [full|cors|ssti|crlf|host|upload|paths]",
                "modes": {
                    "full": "Scan semua vulnerability sekaligus (default)",
                    "cors": "Audit CORS misconfiguration only",
                    "ssti": "Test Server-Side Template Injection only",
                    "crlf": "Test CRLF Injection only",
                    "host": "Test Host Header Injection only",
                    "upload": "Detect file upload forms only",
                    "paths": "Fuzz 100+ sensitive paths only"
                },
                "examples": ["!vuln", "!vuln full", "!vuln cors", "!vuln ssti", "!vuln paths"]
            },
            "api": {
                "syntax": "!api [fuzz|methods|all]",
                "modes": {
                    "fuzz": "Endpoint discovery (22+ common API paths)",
                    "methods": "HTTP method check (GET,POST,PUT,DELETE,PATCH)",
                    "all": "Kedua-duanya sekaligus (default)"
                },
                "examples": ["!api", "!api fuzz", "!api methods", "!api all"]
            },
            "cloud": {
                "syntax": "!cloud [s3|firebase|gcs|all]",
                "modes": {
                    "s3": "Scan AWS S3 buckets only",
                    "firebase": "Scan Firebase databases only",
                    "gcs": "Scan Google Cloud Storage only",
                    "all": "Scan semua provider (default)"
                },
                "examples": ["!cloud", "!cloud s3", "!cloud firebase", "!cloud all"]
            },
            "dirb": {
                "syntax": "!dirb [common|deep]",
                "modes": {
                    "common": "6 directory path dasar (default)",
                    "deep": "17+ path termasuk config, backup, api endpoints"
                },
                "examples": ["!dirb", "!dirb common", "!dirb deep"]
            },
            "headers": {
                "syntax": "!headers",
                "modes": {
                    "(tanpa args)": "Audit 6 security headers: HSTS, CSP, XFO, X-Content-Type, Referrer-Policy, Permissions-Policy"
                },
                "examples": ["!headers"]
            },
            "form": {
                "syntax": "!form",
                "modes": {
                    "(tanpa args)": "Audit semua HTML forms di landing page target"
                },
                "examples": ["!form"]
            },
            "cookie": {
                "syntax": "!cookie",
                "modes": {
                    "(tanpa args)": "Audit flag keamanan cookies: HttpOnly, Secure"
                },
                "examples": ["!cookie"]
            },
            "git": {
                "syntax": "!git [check|deep]",
                "modes": {
                    "check": "Cek exposure .git/config, HEAD, index (default)",
                    "deep": "Check + coba download content yang terexpose"
                },
                "examples": ["!git", "!git check", "!git deep"]
            },
            "wp": {
                "syntax": "!wp [version|plugins|users|files|all]",
                "modes": {
                    "version": "Detect WP version only",
                    "plugins": "Enumerate installed plugins",
                    "users": "Enumerate users via WP-JSON API",
                    "files": "Check vuln files (xmlrpc, debug.log, etc)",
                    "all": "Semua scan sekaligus (default)"
                },
                "examples": ["!wp", "!wp version", "!wp plugins", "!wp users", "!wp all"]
            },
            "payload": {
                "syntax": "!payload [encode|decode] [format] [text]",
                "modes": {
                    "encode": "Encode target/text ke semua format (default)",
                    "decode base64": "Decode dari Base64",
                    "decode hex": "Decode dari Hex",
                    "decode url": "Decode dari URL encoding"
                },
                "examples": ["!payload", "!payload encode test123", "!payload decode base64 dGVzdA=="]
            },
            "subdomain": {
                "syntax": "!subdomain [brute|passive]",
                "modes": {
                    "brute": "Wordlist bruteforce 100+ subdomain (default)",
                    "passive": "Certificate Transparency search via crt.sh"
                },
                "examples": ["!subdomain", "!subdomain brute", "!subdomain passive"]
            },
            "vhost": {
                "syntax": "!vhost",
                "modes": {
                    "(tanpa args)": "Scan virtual hosts via Host header manipulation"
                },
                "examples": ["!vhost"]
            },
            "webports": {
                "syntax": "!webports [common|full]",
                "modes": {
                    "common": "10 web ports standar (default)",
                    "full": "Extended 20+ ports termasuk dev/debug ports"
                },
                "examples": ["!webports", "!webports common", "!webports full"]
            },
            "webaudit": {
                "syntax": "!webaudit [tech|sqli|full]",
                "modes": {
                    "tech": "Detect tech stack only",
                    "sqli": "SQL injection scan only",
                    "full": "Semua audit sekaligus (default)"
                },
                "examples": ["!webaudit", "!webaudit tech", "!webaudit sqli"]
            },
            "stress": {
                "syntax": "!stress <threads> <duration_seconds>",
                "modes": {
                    "<threads>": "Jumlah worker/pasukan serangan (contoh: 200)",
                    "<duration>": "Durasi waktu serangan dalam detik (0 = infinite)"
                },
                "examples": ["!stress 50 10", "!stress 200 30", "!stress 500 0"]
            },
            "script": {
                "syntax": "!script [category]",
                "modes": {
                    "(tanpa args)": "List semua kategori script yang tersedia",
                    "category": "List scripts dalam kategori tertentu (XSS, SQLi, dll)"
                },
                "examples": ["!script", "!script xss", "!script sqli", "!script clickjacking"]
            },
            "help": {
                "syntax": "!help [tool_name]",
                "modes": {
                    "(tanpa args)": "Tampilkan list tool + syntax ringkas",
                    "tool_name": "Detail penggunaan tool spesifik (detail banget)"
                },
                "examples": ["!help", "!help nmap", "!help ffuf"]
            },
            "waf": {
                "syntax": "!waf",
                "modes": {
                    "(tanpa args)": "Scanner WAF (Web Application Firewall). Nge-test target pake payload malicious buat liat siapa yang ngeblokir (Cloudflare, Sucuri, Akamai, dsb)."
                },
                "examples": ["!waf"]
            },
            "cmdi": {
                "syntax": "!cmdi",
                "modes": {
                    "(tanpa args)": "Deteksi OS Command Injection. Ngirim payload 'sleep' (Time-based) ke parameter URL buat ngetes apakah server tereksekusi command system."
                },
                "examples": ["!cmdi"]
            },
            "cms": {
                "syntax": "!cms",
                "modes": {
                    "(tanpa args)": "CMS Checker (Non-WordPress). Nyari signature buat Joomla, Drupal, Magento, dsb lewat path-path sensitif (/administrator, /CHANGELOG.txt)."
                },
                "examples": ["!cms"]
            },
            "joomscan": {
                "syntax": "!joomscan",
                "modes": {
                    "(tanpa args)": "Scanner khusus Joomla. Lebih dalem dari !cms, nyari versi spesifik lewat manifest file xml."
                },
                "examples": ["!joomscan"]
            },
            "nikto": {
                "syntax": "!nikto",
                "modes": {
                    "(tanpa args)": "Web Server Scanner klasik. Nyari file CGI-bin, server-stats, dan file sampah server yang lupa diapus."
                },
                "examples": ["!nikto"]
            },
            "davtest": {
                "syntax": "!davtest",
                "modes": {
                    "(tanpa args)": "WebDAV Tester. Ngecek apakah HTTP Method PUT diizinin buat upload webshell tanpa login."
                },
                "examples": ["!davtest"]
            },
            "urlcrazy": {
                "syntax": "!urlcrazy",
                "modes": {
                    "(tanpa args)": "Typosquatting Generator. Bikin list domain plesetan dari target (misal: g0ogle.com) buat analisa Phishing."
                },
                "examples": ["!urlcrazy"]
            },
            "wayback": {
                "syntax": "!wayback",
                "modes": {
                    "(tanpa args)": "Wayback Machine Scraper. Narik list URL lama yang pernah terekam di Internet Archive buat cari endpoint terpendam."
                },
                "examples": ["!wayback"]
            },
            "weevely": {
                "syntax": "!weevely [password]",
                "modes": {
                    "password": "Password buat trigger webshell (default: admin123)."
                },
                "examples": ["!weevely", "!weevely rahasia123"]
            },
            "testssl": {
                "syntax": "!testssl",
                "modes": {
                    "(tanpa args)": "SSL/TLS Auditor. Cek apakah sertifikat aman, protocol versi berapa (TLS 1.2/1.3), dan cipher suites nya kuat atau cupu."
                },
                "examples": ["!testssl"]
            },
            "apacheusers": {
                "syntax": "!apacheusers",
                "modes": {
                    "(tanpa args)": "Apache User Enumerator. Nyari list username linux di server via fitur mod_userdir (~root, ~admin)."
                },
                "examples": ["!apacheusers"]
            },
            "cewl": {
                "syntax": "!cewl",
                "modes": {
                    "(tanpa args)": "Wordlist Generator. Ngescan kata-kata unik dari bodi website buat dijadiin bahan brute-force password."
                },
                "examples": ["!cewl"]
            },
            "gau": {
                "syntax": "!gau",
                "modes": {
                    "(tanpa args)": "Get All URLs. Narik data OSINT dari AlienVault OTX buat list semua link beneran yang pernah aktif di domain itu."
                },
                "examples": ["!gau"]
            },
            "httrack": {
                "syntax": "!httrack",
                "modes": {
                    "(tanpa args)": "Website Cloner (Basic). Ambil source code HTML mentah halaman target buat lo analisa offline."
                },
                "examples": ["!httrack"]
            },
            "laudanum": {
                "syntax": "!laudanum [php|asp|jsp]",
                "modes": {
                    "lang": "Tinggal pilih mau webshell bahasa apa (default: php)."
                },
                "examples": ["!laudanum php", "!laudanum jsp"]
            },
            "nuclei": {
                "syntax": "!nuclei",
                "modes": {
                    "(tanpa args)": "Mini Vulnerability Scanner. Pake logic templates buatan komunitas buat cari bug kritikal (Git leak, config leak, dsb)."
                },
                "examples": ["!nuclei"]
            },
            "padbuster": {
                "syntax": "!padbuster",
                "modes": {
                    "(tanpa args)": "Padding Oracle Auditor. Ngecek apakah enkripsi cookie/session bisa didekripsi pake serangan Padding Oracle."
                },
                "examples": ["!padbuster"]
            },
            "slowhttp": {
                "syntax": "!slowhttp",
                "modes": {
                    "(tanpa args)": "Slowloris DoS Test. Ngetes apakah server bakal hang kalo kita kirim req HTTP super lambat (Layer 7)."
                },
                "examples": ["!slowhttp"]
            },
            "wapiti": {
                "syntax": "!wapiti",
                "modes": {
                    "(tanpa args)": "Parameter Fuzzer. Otomatis ngetes tiap celah di parameter URL buat cari XSS/HTML Injection."
                },
                "examples": ["!wapiti"]
            },
            "webcache": {
                "syntax": "!webcache",
                "modes": {
                    "(tanpa args)": "Web Cache Poisoning Auditor. Nyisipin header X-Forwarded-Host buat liat apakah cache server bisa diracunin."
                },
                "examples": ["!webcache"]
            },
            "websploit": {
                "syntax": "!websploit",
                "modes": {
                    "(tanpa args)": "Advanced System Audit. Gabungan dari scan HTTP methods, server fingerprinting, dan info powered-by."
                },
                "examples": ["!websploit"]
            },
            "ffuf": {
                "syntax": "!ffuf",
                "modes": {
                    "(tanpa args)": "Fast Directory Brute-Force. Pake mode HEAD request biar super ngebut nyari folder yang exist."
                },
                "examples": ["!ffuf"]
            },
            "wfuzz": {
                "syntax": "!wfuzz",
                "modes": {
                    "(tanpa args)": "SQL Parameter Fuzzer. Nyisipin payload single-quote buat ngetes apakah ada error database terekspos."
                },
                "examples": ["!wfuzz"]
            },
            "dnsenum": {
                "syntax": "!dnsenum",
                "modes": {
                    "(tanpa args)": "DNS Resolver. Nyari list subdomain murni lewat resolusi DNS socket (Host discovery)."
                },
                "examples": ["!dnsenum"]
            },
            "sslscan": {
                "syntax": "!sslscan",
                "modes": {
                    "(tanpa args)": "SSL Info Gatherer. Narik info siapa issuer sertifikatnya dan kapan expirednya murni dari handshake."
                },
                "examples": ["!sslscan"]
            },
            "dmitry": {
                "syntax": "!dmitry",
                "modes": {
                    "(tanpa args)": "Quick Port Probe (Stealth). Cek port vital (80, 443, 21, 22) secara cepet tanpa bikin server curiga."
                },
                "examples": ["!dmitry"]
            },
            "gowitness": {
                "syntax": "!gowitness",
                "modes": {
                    "(tanpa args)": "Screenshot Information. Kasih tau apa yang dibutuhin buat aktifin visual engine ini."
                },
                "examples": ["!gowitness"]
            },
            "webacoo": {
                "syntax": "!webacoo",
                "modes": {
                    "(tanpa args)": "Cookie Backdoor Generator. Bikin webshell PHP yang eksekusi perintahnya via cookie HTTP (Low detection)."
                },
                "examples": ["!webacoo"]
            },
            "fierce": {
                "syntax": "!fierce",
                "modes": {
                    "(tanpa args)": "DNS Zone Transfer Auditor. Nyoba narik data AXFR DNS buat dapet semua list IP subdomain server."
                },
                "examples": ["!fierce"]
            }
        }

        # * Pentesting Roadmap v5.9 (8 Misi Detail)
        self.roadmap = [
            "v5.9-Misi-1: Reconnaissance (!recon) - Tahap pengumpulan intelijen dasar. Kita cari IP asli, record DNS, WHOIS, sampe teknologi server yang dipake. Mode: quick/deep/full. Tanpa info ini serangan lu bakal buta arah.",
            "v5.9-Misi-2: Infrastructure Scan (!nmap) - Pemetaan port dan service server. Kita cari pintu (port) yang kebuka: 80 (HTTP), 443 (HTTPS), 22 (SSH), 3306 (MySQL). Custom ports: !nmap 80,443,3306.",
            "v5.9-Misi-3: Discovery (!subdomain / !dirb) - Cari pintu belakang: subdomain rahasia (dev, test, staging) dan directory tersembunyi (/admin, /backup, /.env). Brute force atau passive scan.",
            "v5.9-Misi-4: Web Analysis (!headers / !cookie / !form / !git) - Audit keamanan web layer: security headers, cookie flags, form parameters, dan exposed .git repository.",
            "v5.9-Misi-5: Vulnerability Scan (!vuln) - Cari lubang vulnerability: CORS Misconfig, SSTI, CRLF Injection, Host Header Injection, File Upload, dan 100+ Sensitive Path fuzzing.",
            "v5.9-Misi-6: API dan Cloud (!api / !cloud) - Bongkar urat nadi data modern: endpoint API rahasia, HTTP method bypass, dan cloud storage publik (S3, Firebase, GCS).",
            "v5.9-Misi-7: CMS Audit (!wp) - Audit khusus platform CMS: WordPress version, plugin vulnerabilities, user enumeration, dan sensitive file exposure.",
            "v5.9-Misi-8: Stress Testing (!stress) - Pengujian ketahanan akhir. Bantai server dengan tsunami HTTP request buat liat seberapa kuat pertahanan mereka. Format: !stress <threads> <duration>."
        ]

    def getSteps(self):
        return []

    def getRoadmap(self):
        return self.roadmap

    # * Ambil usage info untuk tool tertentu
    def getUsage(self, toolName):
        return self.usageDatabase.get(toolName, None)

    def searchHelp(self, query):
        query = query.lower()
        results = {}
        for k, v in self.helpDatabase.items():
            if query in k or query in v.lower():
                results[k] = v
        return results
