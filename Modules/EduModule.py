# * Modul edukasi untuk pemula (Pentesting Academy)
class EduModule:
    def __init__(self):
        pass

    # * Kamus istilah pentester dalam bahasa Indonesia santai
    def getWiki(self):
        return {
            "XSS": "Cross-Site Scripting. Bayangin lu nyelipin catetan kecil ke website orang lain biar tampil di semua user.",
            "SQLi": "SQL Injection. Nanya ke database dengan cara licik biar dikirim semua data sensitifnya.",
            "Whois": "KTP-nya domain. Isinya info siapa yang punya, belinya kapan, dan domain-nya kemana.",
            "Brute Force": "Coba-coba sampe mampus. Lu nebak kunci pake sejuta cara sampe ada yang kebuka.",
            "Honeypot": "Sistem jebakan. Dibikin keliatan gampang di-hack biar hacker masuk ke situ padahal dipantau.",
            "Payload": "Senjata utamannya. Serangkaian kode yang lu kirim buat eksploitasi celah keamanan."
        }

    # * Langkah-langkah belajar buat jadi pentester (Roadmap)
    def getRoadmap(self):
        return [
            "1. Belajar Dasar Jaringan (IP Address, Port, TCP/UDP)",
            "2. Kuasai OS Linux (Command line adalah pedang lu)",
            "3. Paham HTTP Protocol (Gimana browser ngobrol sama server)",
            "4. Belajar SQL Dasar (Database itu gudang harta karun)",
            "5. Belajar 1 Bahasa Scripting (Python disarankan!)",
            "6. Praktek di lab legal (TryHackMe, HackTheBox)"
        ]

    # * Tips keamanan cepat buat pemula
    def getQuickTips(self):
        return [
            "Selalu pake VPN kalo lagi audit target luar.",
            "Jangan pernah audit target tanpa ijin (Gunakan platform Bug Bounty).",
            "Update tools lu secara berkala biar gak ketinggalan jaman."
        ]
