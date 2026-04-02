class WebToolsGuide:
    """
    WebToolsGuide itu kayak katalog referensi tools pentesting eksternal.
    
    ApexOmega punya banyak tool bawaan, TAPI kadang lu butuh tool khusus.
    Di sini ada 70+ tools eksternal yang bisa lu install & pake:
    
    🔍 RECONNAISSANCE (Pengumpulan Info):
    - photon - Crawler website super cepat
    - gospider - Web spider modern
    - hakrawler - Crawler buat OSINT
    - subfinder - Subdomain discovery tool
    - theharvester - Email & subdomain hunter
    
    📁 DIRECTORY SCANNING:
    - dirb - Classic directory scanner
    - dirsearch - Fast web path scanner
    - gobuster - Directory/DNS bruteforcer
    - ffuf - Fast web fuzzer (Go-based)
    - feroxbuster - Recursive content discovery
    
    🛡️ VULNERABILITY SCANNING:
    - nikto - Web server scanner (CGI, outdated files)
    - nuclei - Template-based vulnerability scanner
    - wapiti - Web application vulnerability scanner
    - skipfish - Automated security reconnaissance
    
    💉 INJECTION TOOLS:
    - sqlmap - Automatic SQL injection tool
    - commix - Command injection automation
    - xsstrike - XSS detection suite
    - ssrfmap - SSRF exploitation
    
    📊 ANALYSIS & DEBUGGING:
    - burpsuite - Full-featured web pentest platform
    - owasp-zap - Free security testing platform
    - mitmproxy - HTTP/HTTPS proxy
    - wireshark - Network protocol analyzer
    
    🔐 PASSWORD TOOLS:
    - cewl - Custom wordlist generator
    - hashcat - Password hash cracker
    - john - John the Ripper password cracker
    - hydra - Network login cracker
    
    📱 CMS-SPECIFIC:
    - wpscan - WordPress security scanner
    - joomscan - Joomla vulnerability scanner
    - drupscan - Drupal security scanner
    
    ☁️ CLOUD & API:
    - aws-cli - Amazon Web Services CLI
    - gcloud - Google Cloud CLI
    - postman - API testing platform
    
    🎯 SPECIAL PURPOSE:
    - cutycapt - Web screenshot utility
    - httprobe - HTTP/HTTPS probe tool
    - httpx - Multi-purpose HTTP toolkit
    - nuclei - Fast vulnerability scanner
    
    💡 CARA PAKE:
    Ketik !webtools di terminal buat liat daftar lengkap!
    """
    def __init__(self, core):
        self.core = core
        
    # * Nampilin list web pentest tools ke terminal UI
    def show_tools(self):
        tools = [
            "1. apache-users - Identifikasi user dari instalasi Apache.",
            "2. arjun - Pencari hidden HTTP parameters/query.",
            "3. beef-xss - Browser Exploitation Framework (XSS tool).",
            "4. burpsuite - Platform komprehensif buat web app security testing.",
            "5. cadaver - WebDAV client buat pentest.",
            "6. caido - Lightweight web security auditing toolkit (alternatif Burp).",
            "7. cewl - Custom wordlist generator khusus crawling web.",
            "8. cmseek - CMS Detection and Exploitation suite.",
            "9. commix - Automated command injection exploitation.",
            "10. crlfuzz - CRLF vulnerability scanner.",
            "11. cutycapt - Nge-capture halaman web ke bentuk gambar.",
            "12. davtest - Tool buat nge-test file upload lewat WebDAV.",
            "13. defectdojo - Open-source application vulnerability management.",
            "14. dirb - Web content scanner / directory bruteforcing.",
            "15. dirbuster - Dir/File bruteforce via wordlist (GUI).",
            "16. dirsearch - Web path scanner cepat (CLI).",
            "17. dotdotpwn - Directory traversal fuzzer.",
            "18. dvwa - Damn Vulnerable Web App (buat dicoba serang).",
            "19. evilginx2 - Phishing framework with MFA bypass.",
            "20. feroxbuster - Fast, simple, recursive content discovery.",
            "21. ffuf - Fast web fuzzer ditulis pake Go.",
            "22. getallurls - Fetch known URLs dari AlienVault, Wayback, dll.",
            "23. gobuster - Directory/DNS/vhost bruteforcing tool.",
            "24. gophish - Open-source phishing toolkit.",
            "25. gospider - Fast web spider.",
            "26. gowitness - Web screenshot utility.",
            "27. hakrawler - Web crawler buat kumpulin URL & paths.",
            "28. httrack - Offline browser / website cloner.",
            "29. httprint - Web server fingerprinting tool.",
            "30. httprobe - Probe working HTTP/HTTPS servers.",
            "31. httpx-toolkit - Fast/multi-purpose HTTP toolkit.",
            "32. joomscan - Joomla CMS vulnerability scanner.",
            "33. jsql-injection - Java tool for SQL injection.",
            "34. juice-shop - OWASP vulnerable web app.",
            "35. laudanum - Kumpulan file inject (webshells).",
            "36. mitmproxy - Interactive HTTP/HTTPS proxy.",
            "37. nikto - Web server scanner (cari CGI, files jadul, dsb).",
            "38. nuclei - Fast vulnerability scanner bersistem template.",
            "39. padbuster - Padding oracle attack script.",
            "40. paros - Java web proxy for vulnerability assessment.",
            "41. photon - Incredibly fast crawler buat OSINT web.",
            "42. skipfish - Fully automated, active web security recon.",
            "43. slowhttptest - Layer 7 slow HTTP DoS tools.",
            "44. sqlmap - Automatic SQL injection & database takeover.",
            "45. sqlninja - SQL Injection exploit on MS SQL server.",
            "46. sqlsus - MySQL injection & takeover tool.",
            "47. sstimap - Server-side template injection (SSTI) testing.",
            "48. subfinder - Subdomain discovery tool cepat.",
            "49. sublist3r - Cepat cari subdomain pakai open sources.",
            "50. testssl.sh - Cek cipher, protokol, kerentanan TLS/SSL.",
            "51. urlcrazy - Typosquatting web tool.",
            "52. wafw00f - Identifikasi & fingerprinting WAF (Web App Firewall).",
            "53. wapiti - Web application vulnerability scanner.",
            "54. watobo - Semi-automated web app security testing.",
            "55. waybackpy - Akses Wayback Machine API (buat OSINT website endpoint).",
            "56. web-cache-vulnerability-scanner - Cek kerentanan Web Cache.",
            "57. webacoo - Web Backdoor Cookie Script-Kit.",
            "58. webscarab - Web communication analyzer tool.",
            "59. webshells - Kumpulan payload webshell.",
            "60. websploit - Web & Network hacking framework.",
            "61. weevely - Weaponized web shell (PHP).",
            "62. wfuzz - Web application fuzzer.",
            "63. whatweb - Next generation web scanner (fingerprinting).",
            "64. wpscan - Black box WordPress vulnerability scanner.",
            "65. xsser - Otomasi payload XSS attack.",
            "66. xsstrike - Advanced XSS scanner + payload generator.",
            "67. zaproxy - OWASP ZAP (Proxy + Web vulnerability scanner)."
        ]
        
        self.core.gui.log_to_terminal("\n================ KALI WEB PENTEST TOOLS ================\n", "[info] ")
        for t in tools:
            self.core.gui.log_to_terminal(f"  {t}\n", "[success] ")
        self.core.gui.log_to_terminal("========================================================\n", "[info] ")
