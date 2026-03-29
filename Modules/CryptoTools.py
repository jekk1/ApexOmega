import hashlib
import string
import random
import os
from typing import Optional, List, Dict, Union

# * Modul manipulasi data dan kriptografi standar
class CryptoTools:
    def __init__(self):
        self.default_wordlist = [
            "admin", "password", "123456", "12345678", "123456789", "qwerty", "root", "user", 
            "login", "rahasia", "indonesia", "bismillah", "sayang", "cinta", "kucing", "garuda",
            "merdeka", "jakarta", "bandung", "surabaya", "manchester", "chelsea", "arsenal",
            "liverpool", "madrid", "barcelona", "12345", "111111", "000000", "rahasia123",
            "bismillah123", "indonesia123", "sayang123", "cinta123", "password123", "admin123",
            "admin12345", "admin1234", "admin1", "admin12", "qwertyuiop", "asdfghjkl", "zxcvbnm",
            "qazwsx", "123qwe", "qwe123", "12345qwe", "administrator", "guest", "test"
        ]

    def hash_identifier(self, hashValue: str) -> str:
        """Deteksi tipe hash berdasarkan panjang karakter.
        
        Args:
            hashValue: String hash yang ingin dideteksi.
            
        Returns:
            String nama algoritma hash (MD5, SHA1, SHA256) atau Unknown.
        """
        length = len(hashValue)
        if length == 32:
            return "md5"
        elif length == 40:
            return "sha1"
        elif length == 64:
            return "sha256"
        elif length == 128:
            return "sha512"
        return "Unknown"

    def compareHashes(self, plainText: str, hashValue: str, hashType: str = "md5") -> bool:
        """Bandingkan teks biasa dengan nilai hash yang diberikan.
        
        Args:
            plainText: Teks biasa yang akan dihash.
            hashValue: Nilai hash untuk dibandingkan.
            hashType: Algoritma hashing (md5, sha1, sha256). Defaults to md5.
            
        Returns:
            True jika cocok, False jika tidak.
        """
        try:
            hashType = hashType.lower()
            if hashType == "md5":
                hashed = hashlib.md5(plainText.encode()).hexdigest()
            elif hashType == "sha1":
                hashed = hashlib.sha1(plainText.encode()).hexdigest()
            elif hashType == "sha256":
                hashed = hashlib.sha256(plainText.encode()).hexdigest()
            else:
                return False
            return hashed == hashValue
        except Exception:
            return False

    def crackHash(self, hashValue: str, hashType: Optional[str] = None, wordlist_path: Optional[str] = None) -> Optional[str]:
        """Pecahkan hash menggunakan brute-force wordlist.
        
        Args:
            hashValue: String hash yang akan dipecahkan.
            hashType: Algoritma hash. Jika None, akan dideteksi otomatis.
            wordlist_path: Path ke file wordlist external (.txt). Jika None, pakai default internal.
            
        Returns:
            Teks hasil crack (password asli) atau None jika tidak ditemukan.
        """
        if not hashType:
            hashType = self.hash_identifier(hashValue)
            if hashType == "Unknown":
                return None
        
        words_to_test = self.default_wordlist
        
        if wordlist_path and os.path.exists(wordlist_path):
            try:
                with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                    # Ambil kata, bersihkan whitespace/newline, lompati empty string
                    words_to_test = [line.strip() for line in f if line.strip()]
            except Exception:
                pass # Fallback ke default wordlist kalau gagal baca file
                
        for word in words_to_test:
            if self.compareHashes(word, hashValue, hashType):
                return word
                
        return None

    def batch_crack(self, hashList: List[str], wordlist_path: Optional[str] = None) -> Dict[str, str]:
        """Pecahkan daftar hash sekaligus menggunakan wordlist.
        
        Args:
            hashList: List berisi string hash.
            wordlist_path: Path file wordlist external opsional.
            
        Returns:
            Dictionary mapping hash ke password asli (jika ditemukan).
        """
        results = {}
        for hash_val in hashList:
            cracked = self.crackHash(hash_val, wordlist_path=wordlist_path)
            if cracked:
                results[hash_val] = cracked
        return results

    def generatePassword(self, length: int = 16) -> str:
        """Generator password acak kriptografis yang kuat.
        
        Args:
            length: Panjang password yang dihasilkan.
            
        Returns:
            String password acak.
        """
        try:
            chars = string.ascii_letters + string.digits + "!@#$%^&*"
            return ''.join(random.choice(chars) for _ in range(length))
        except Exception:
            return "ErrorGeneratingPassword"
