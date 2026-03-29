import requests
import re
from urllib.parse import urljoin
from typing import List, Optional

# * Modul Penganalisa Kerentanan Spesifik Platform WordPress
class WordPressScanner:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {'User-Agent': 'ApexOmega/5.0 (WP Auditor)'}
        self.core = None # Will be set by core
        
        # Wordlist 50+ Plugin populer & rentan
        self.commonPlugins = [
            "wp-forms", "elementor", "contact-form-7", "woocommerce", "jetpack",
            "akismet", "wordfence", "yoast-seo", "all-in-one-wp-migration", "updraftplus",
            "classic-editor", "litespeed-cache", "w3-total-cache", "wp-super-cache", "mailchimp-for-wp",
            "really-simple-ssl", "duplicate-post", "smush", "wp-fastest-cache", "duplicator",
            "ninja-forms", "advanced-custom-fields", "monsterinsights", "redirection", "wp-mail-smtp",
            "insert-headers-and-footers", "limit-login-attempts-reloaded", "bbpress", "buddypress", "woo-commerce",
            "siteorigin-panels", "all-in-one-seo-pack", "autoptimize", "black-studio-tinymce-widget", "loco-translate",
            "cookie-notice", "slider-revolution", "visual-composer", "revslider", "js_composer",
            "wp-file-manager", "gravityforms", "easy-digital-downloads", "contact-form-7-datepicker", "wp-db-backup",
            "seo-by-rank-math", "exactmetrics", "ml-slider", "wp-multibyte-patch", "shortpixel-image-optimiser"
        ]

    def isWordPress(self, baseUrl: str) -> bool:
        """Pemeriksaan awal validasi indikator sistem root WordPress.
        
        Args:
            baseUrl: Sasaran domain untuk identifikasi jejak instalasi (*wp-login*, *wp-content*).
            
        Returns:
            Status sah infrastruktur WP (Penghindar salah sasaran deteksi).
        """
        signatures = [
            "/wp-login.php",
            "/wp-admin/",
            "/wp-content/themes/",
            "/wp-includes/"
        ]
        score = 0
        try:
            # Uji indeks utama untuk jejak wajar WP generator
            res = self.session.get(baseUrl, headers=self.headers, timeout=5)
            if "wp-content" in res.text or "wordpress" in res.text.lower():
                score += 2
                
            # Cek eksistensi struktur bawaan
            for sig in signatures:
                target = urljoin(baseUrl, sig)
                res_sig = self.session.head(target, headers=self.headers, timeout=3, allow_redirects=False)
                if res_sig.status_code in [200, 301, 302, 401, 403]:
                    score += 1
            
            return score >= 2
        except Exception:
            return False

    def scanVersion(self, baseUrl: str) -> Optional[str]:
        """Ekstraksi identitas versi mesin platform WP melalui indeks meta tags.
        
        Args:
            baseUrl: Parameter antarmuka awal halaman indeks web.
            
        Returns:
            Angka versi perangkat (jika dipaparkan).
        """
        try:
            res = self.session.get(baseUrl, headers=self.headers, timeout=5)
            # Pencari meta generator
            match = re.search(r'name="generator" content="wordpress (\d+\.\d+(\.\d+)?)"', res.text, re.I)
            if match:
                return match.group(1)
            
            # Cek parameter antrean aset gaya/skrip
            st_match = re.search(r'wp-includes/[^\'"]+\?ver=(\d+\.\d+(\.\d+)?)', res.text, re.I)
            if st_match:
                return st_match.group(1)
                
            return None
        except Exception:
            return None

    def detectVersion(self, baseUrl: str) -> Optional[str]:
        """Identifikasi versi mesin WP (Pembungkus scanVersion)."""
        return self.scanVersion(baseUrl)

    def scanPlugins(self, baseUrl: str) -> List[str]:
        """Enumerasi direktori perluasan (plugin) umum dengan pencocokan status struktur peladen.
        
        Args:
            baseUrl: Alamat utama root sistem web WP.
            
        Returns:
            Nama perluasan/plugin aktif teridentifikasi di peladen.
        """
        if not self.isWordPress(baseUrl):
            return []
            
        found = []
        for p in self.commonPlugins:
            if self.core and getattr(self.core, 'stop_requested', False):
                break
                
            # Kita uji langsung pemanggilan aset pendukung readme untuk keabsahan (Hindar WAF blok global)
            target = urljoin(baseUrl, f"/wp-content/plugins/{p}/readme.txt")
            try:
                res = self.session.head(target, headers=self.headers, timeout=3, allow_redirects=False)
                if res.status_code == 200:
                    found.append(p)
            except Exception:
                pass
        return found
        
    def enumerateTheme(self, baseUrl: str) -> Optional[str]:
        """Mengungkap varian tata visual halaman lewat pemanggilan berkas identitas tema aktif.
        
        Args:
            baseUrl: Sasaran akar domain sistem.
            
        Returns:
            Identitas tema dan rilis versinya jika ditemui (Info: Versi).
        """
        if not self.isWordPress(baseUrl):
            return None
            
        try:
            res = self.session.get(baseUrl, headers=self.headers, timeout=5)
            # Pencarian path tema di html mentah
            theme_match = re.search(r'wp-content/themes/([^/]+)/', res.text)
            if theme_match:
                theme_name = theme_match.group(1)
                
                # Permintaan pengungkapan file spesifikasi style.css
                style_url = urljoin(baseUrl, f"/wp-content/themes/{theme_name}/style.css")
                style_res = self.session.get(style_url, headers=self.headers, timeout=3)
                if style_res.status_code == 200:
                    ver_match = re.search(r'Version:\s*(\d+\.\d+(\.\d+)?)', style_res.text, re.I)
                    if ver_match:
                        return f"{theme_name} (v{ver_match.group(1)})"
                return theme_name
            return None
        except Exception:
            return None

    def enumerateUsers(self, baseUrl: str) -> List[str]:
        """Pembongkaran kerahasiaan kepemilikan panel administrator menggunakan rute peladen WP-JSON.
        
        Args:
            baseUrl: Direktori rujukan.
            
        Returns:
            Susunan pemilik terdaftar dari jalur terbuka bawaan api antarmuka peladen.
        """
        target = urljoin(baseUrl, "/wp-json/wp/v2/users")
        try:
            res = self.session.get(target, headers=self.headers, timeout=5)
            if res.status_code == 200:
                data = res.json()
                if isinstance(data, list):
                    return [f"{u.get('slug')} (ID: {u.get('id')})" for u in data]
            return []
        except Exception:
            return []

    def scanVulnFiles(self, baseUrl: str) -> List[str]:
        """Pencarian celah log bawaan WP atau arsip usang rentan ekstraksi muatan.
        
        Args:
            baseUrl: Direktori akar rujukan kueri.
            
        Returns:
            Daftar berkas dengan potensi intervensi serangan masukan.
        """
        files = [
            "xmlrpc.php",
            "wp-config.php.bak",
            "wp-content/debug.log"
        ]
        found = []
        for f in files:
            target = urljoin(baseUrl, f)
            try:
                res = self.session.head(target, headers=self.headers, timeout=3, allow_redirects=False)
                if res.status_code in [200, 403]:
                    found.append(f)
            except Exception:
                pass
        return found
