from typing import List, Dict, Optional

# * Modul Bantuan & Panduan Penggunaan Alat Bantu Keamanan
class GuidedAssistant:
    def __init__(self):
        # * Database Basis Pengetahuan Perangkat
        self.helpDatabase: Dict[str, str] = {
            "recon": "Tahap pengumpulan informasi (Reconnaissance) untuk mendeteksi identitas peladen, layanan DNS, dan alamat IP asli target. Gunakan !recon [mode]: quick (IP+DNS), deep (+WHOIS+AllDNS), atau full (+Tech+CertSubs).",
            "nmap": "Pemeriksa keterbukaan port. Digunakan untuk memeriksa celah layanan aktif. Gunakan format !nmap [port spesifik] (contoh: 80,443). Jika tanpa parameter, memindai 10 port standar.",
            "subdomain": "Pencarian rentang subdomain (contoh: 'dev.target.com'). Gunakan !subdomain brute (wordlist bruteforce) atau !subdomain passive (pencarian jejak sertifikat crt.sh).",
            "webaudit": "Pemeriksaan umum kerentanan aplikasi web seperti deteksi WAF dan kerentanan SQLi statis. Gunakan !webaudit tech, !webaudit sqli, atau !webaudit full.",
            "vuln": "Atlas pemindaian kerentanan spesifik. Mendukung modul: !vuln cors, !vuln ssti, !vuln crlf, !vuln host, !vuln upload, !vuln paths, atau !vuln full.",
            "api": "Auditor titik akhir API REST/GraphQL internal. Gunakan !api fuzz (pencarian endpoint), !api methods (pemeriksaan HTTP method), atau !api all.",
            "cloud": "Pendeteksi bucket penyimpanan awan publik (Data Leakage). Parameter: !cloud s3 (AWS), !cloud firebase, !cloud gcs, atau !cloud all.",
            "stress": "Pengujian daya tahan respon peladen melalui beban asinkron (Stress Testing). Format: !stress <jumlah_utas> <durasi_detik> (0 untuk konstan).",
            "vhost": "Penemuan Host Virtual pada satu peladen IP yang sama. Menjalankan injeksi parameter header antarmuka.",
            "webports": "Pencarian layanan web tersembunyi. Mode !webports common (10 HTTP ports) atau !webports full (port tambahan).",
            "wp": "Pemeriksaan arsitektur CMS WordPress. Parameter terdukung: !wp version, !wp plugins, !wp users, !wp files, atau !wp all.",
            "wordpress": "Sistem alias untuk perintah !wp. Silakan gunakan parameter serupa (contoh: !wordpress plugins).",
            "sqlmap": "Otomasi uji dasar keamanan kerentanan SQL Injection pada input formulir pendaratan aplikasi.",
            "dirb": "Alat pencarian manual jalur-jalur root direktori fungsional. Parameter !dirb common (standar operasi) atau !dirb deep (daftar lebih ekstensif).",
            "payload": "Format konversi karakter cepat untuk kebutuhan generator serangan. Gunakan !payload encode [teks] atau !payload decode [format] [teks]. Format standar: base64, hex, url.",
            "headers": "Pemeriksaan parameter keamanan respon HTTP target (CORS, HSTS, X-Frame-Options).",
            "form": "Modul analisis potensi parameter masukan berisiko injeksi HTML/DOM.",
            "cookie": "Evaluasi kontrol kebijakan sesi keamanan melalui bendera set-cookie (HttpOnly, Secure).",
            "git": "Pendektesi jejak kerentanan sistem versi kontrol terbuka (.git). Cek menggunakan !git check (identifikasi) atau !git deep (pengambilan metadata).",
            "script": "Pustaka parameter script injeksi. Tampilkan perintah dengan !script [kategori] (XSS/SQLi dsb).",
            "help": "Daftar fungsionalitas sintaks ringkas. Tambahkan argumen spesifik (contoh: !help nmap).",
            "cewl": "Pengekstrak kata khusus halaman menjadi format kamus wordlist lokal.",
            "dmitry": "Information Gathering untuk kueri perutean peladen dasar open ports / nama host resolusi.",
            "sslscan": "Evaluator validitas spesifikasi serta algoritma keamanan sertifikasi koneksi SSL/TLS.",
            "testssl": "Sistem evaluasi alternatif HTTPS serupa dengan kapabilitas modul SSLScan.",
            "wayback": "Tarikan historis relasi tautan yang terdokumentasi via arsip Wayback Machine API.",
            "gau": "Penyelaman informasi arsip tautan melalui intelijen keamanan AlienVault OTX.",
            "dnsenum": "Pengurai sub zona fariasi rute (resolusi lookup dns enumerasi).",
            "fierce": "Simulasi otentikasi lemah AXFR zone transfer domain sistem target.",
            "nikto": "Uji kelemahan peladen warisan masa lalu (CGI binaries) hingga kesalahan konfigurasi mutakhir.",
            "apacheusers": "Alat validasi nama pemilik user Unix via konfigurasi direktori modul mod_userdir apache.",
            "waf": "Uji sistem WAF filter eksternal menggunakan simulasi kiriman string bermuatan anomali.",
            "cms": "Detektor arsitektur aplikasi (selain WP) seperti tipe CMS dasar Drupal & Magento.",
            "joomscan": "Auditor kelemahan bawaan kerangka pengembangan perangkat lunak CMS Joomla.",
            "wapiti": "Penganalisa kerentanan aplikasi peladen dalam sisi injeksi manipulasi URI.",
            "webcache": "Evaluator HTTP/1 header perantara untuk kemungkinan eksploit keracunan tembolok peladen.",
            "nuclei": "Rangka kerja dinamis sistem eksploit deteksi template CVE masa lalu secara kustom.",
            "padbuster": "Mencari petunjuk masalah pada kebocoran komputasi enkripsi padding (Padding Oracle).",
            "cmdi": "Automasi dasar pada penilaian serangan sistem Injeksi Perintah Operasi Berbasis Waktu/Jeda.",
            "davtest": "Inspeksi fungsi modul DAV pada PUT/PROPFIND pada otorisasi konektor terlewat tanpa sandi.",
            "weevely": "Sistem pembuatan perangkat muatan balik pada tipe modul PHP siluman.",
            "webacoo": "Alat penjamin sesi pertahanan koneksi balik muatan PHP dengan otentikasi pengkodean kuki.",
            "laudanum": "Pusat rujukan kode-kode templat mentah standar bahasa ganda peladen web pasca-serangan.",
            "slowhttp": "Evaluator daya tahan respon server memproses asinkron melalui DoS level aplikasi dasar.",
            "ffuf": "Mesin fuzzer URI berkemampuan asinkron secara gesit tanpa muatan penuh sumber daya unduhan.",
            "wfuzz": "Uji fuzz parameter dengan injeksi kutip memicu eksposur celah pemrosesan kueri mentah.",
            "skipfish": "Probe heuristik pasif mengukur kelakuan sistem tanggapan pada dokumen referensi tidak logis.",
            "urlcrazy": "Mesin analisis kemiripan domain tipografi pergeseran pelafalan terkait investigasi penipuan (Phishing).",
            "gowitness": "Alat pengambil tangkap gambar visual antarmuka otomatis berbasis tanpa kepala (Headless Mode).",
            "webtools": "Daftar pustaka tambahan tentang standar pengujian serta rujukan referensi panduan lengkap.",
            "websploit": "Pembangkit kombinasi meta-data uji dari fungsi header audit teridentifikasi berkesalahan kelola."
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
