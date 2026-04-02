# * Modul edukasi untuk pemula (Pentesting Academy v4.7)
class EduModule:
    """
    EduModule itu kayak sekolah hacker online GRATIS!
    
    Punya 3 materi utama:
    
    1. WIKI - Kamus Istilah Hacker (Bahasa Manusia)
       
       "XSS itu apa?"
       → Cross-Site Scripting. Nyelipin script (biasanya JS) biar 
         jalan di browser korban via website target.
       
       "SQL Injection?"
       → Nyelipin perintah database via input form biar data 
         kesedot semua.
       
       "Reverse Shell?"
       → Teknik biar server target yang 'nelfon' balik ke komputer 
         lu (dapet akses terminal).
       
       "Honeypot?"
       → Server jebakan buat manggil hacker, padahal isinya cuma 
         rekaman aktivitas mereka.
    
    2. ROADMAP - Panduan Jadi Hacker dari 0 sampe Pro
    
       LEVEL 0: THE INFRASTRUCTURE (Dasar-dasar)
       - Paham Linux & Terminal (ls, cd, pwd)
       - File System (file teks, binary, script)
       - User Power (user biasa vs sudo/root)
       - Basic Network (IP, ping, tracert)
       
       LEVEL 1: WEB BASICS
       - HTTP Protocol (GET vs POST)
       - Browser DevTools (F12)
       - Domain & DNS (nslookup)
       
       LEVEL 2: ATTACK FUNDAMENTALS
       - Information Gathering (Whois, Port Scan)
       - Vulnerability Scan (tool otomatis)
       - Exploitation (SQLi, XSS)
       
       LEVEL 3: PROFESSIONALISM
       - Bug Bounty Platform (HackerOne, Bugcrowd)
       - Documentation (Report = bukti kerja)
    
    3. QUICK TIPS - Tips Keamanan Cepat
       - "JANGAN PERNAH audit tanpa ijin!" (Itu kriminal!)
       - "Selalu pake VM buat nyobain tool baru"
       - "Join Discord/Telegram security lokal"
       - "Gunakan platform legal kayak TryHackMe"
    
    Cocok buat lu yang:
    - Baru mau belajar hacking
    - Bingung mulai dari mana
    - Gak punya background IT
    - Mau penjelasan santai gak ribet
    """
    def __init__(self):
        pass

    # * Kamus istilah pentester dalam bahasa Indonesia santai
    def getWiki(self):
        return {
            "XSS": "Cross-Site Scripting. Nyelipin script (biasanya JS) biar jalan di browser korban via website target.",
            "SQLi": "SQL Injection. Nyelipin perintah database via input form biar data kesedot semua.",
            "WHOIS": "KTP-nya domain. Info pemilik, registrar, sampe tanggal kadaluarsa.",
            "BRUTE FORCE": "Nebak password pake kombinasi jutaan kata sampe jebol.",
            "HONEYPOT": "Server jebakan buat manggil hacker, padahal isinya cuma rekaman aktivitas mereka.",
            "PAYLOAD": "Kode jahat (senjata) yang dikirim buat eksploitasi celah.",
            "REVERSE SHELL": "Teknik biar server target yang 'nelfon' balik ke komputer lu (dapet akses terminal).",
            "C2": "Command & Control. Server pusat buat ngontrol semua komputer yang udah kena hack.",
            "PRIVSET": "Privilege Escalation. Dari user biasa naik pangkat jadi admin/root biar bisa ngapa-ngapain."
        }

    # * Langkah-langkah belajar buat jadi pentester (Zero-to-Hero Roadmap)
    def getRoadmap(self):
        return [
            "[LEVEL 0: THE INFRASTRUCTURE]",
            "1. Paham OS: Pake Linux/Terminal. Cek isi folder (ls), pindah folder (cd), liat posisi (pwd).",
            "2. File System: Tau bedanya file teks, binary, sama script (sh/py/php).",
            "3. User Power: Tau bedanya user biasa sama 'sudo' (sang penguasa root).",
            "4. Basic Network: Tau IP lu sendiri (ifconfig), tes koneksi (ping), liat rute (tracert).",
            "",
            "[LEVEL 1: WEB BASICS]",
            "5. HTTP Protocol: Gimana website ngirim data (GET vs POST).",
            "6. Browser DevTools: Teken F12, liat isinya, edit HTML-nya secara lokal.",
            "7. Domain & DNS: Tau gimana 'google.com' berubah jadi IP (nslookup).",
            "",
            "[LEVEL 2: ATTACK FUNDAMENTALS]",
            "8. Information Gathering: Cari tau sebanyak mungkin tentang target (Whois, Port Scan).",
            "9. Vulnerability Scan: Pake tool otomatis buat nyari celah (Web Scanner).",
            "10. Exploitation: Praktekin celah yang ditemuin (SQLi/XSS).",
            "",
            "[LEVEL 3: PROFESSIONALISM]",
            "11. Bug Bounty Platform: Cari duit legal di HackerOne atau Bugcrowd.",
            "12. Documentation: Catat setiap langkah lu. Report adalah bukti kerja profesional."
        ]

    # * Tips keamanan cepat buat pemula
    def getQuickTips(self):
        return [
            "JANGAN PERNAH audit target tanpa ijin (Itu tindak kriminal!).",
            "Selalu pake Virtual Machine (VM) buat nyobain tool baru.",
            "Komunitas adalah kunci. Join Discord/Telegram security lokal.",
            "Gunakan platform legal kayak TryHackMe buat latihan aman."
        ]
