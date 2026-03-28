import hashlib
import base64
import urllib.parse
import string
import random

# * Modul manipulasi data dan kriptografi sederhana
class CryptoTools:
    def __init__(self):
        pass

    # * Pecahkan hash menggunakan metode brute-force lokal atau lookup (Simulasi)
    def crackHash(self, hashValue, hashType="md5", wordlist=["admin", "password", "123456", "qwerty"]):
        for word in wordlist:
            if hashType == "md5":
                if hashlib.md5(word.encode()).hexdigest() == hashValue:
                    return word
            elif hashType == "sha1":
                if hashlib.sha1(word.encode()).hexdigest() == hashValue:
                    return word
            elif hashType == "sha256":
                if hashlib.sha256(word.encode()).hexdigest() == hashValue:
                    return word
        return None

    # * Encode data ke berbagai format
    def encodeData(self, data, mode="base64"):
        if mode == "base64":
            return base64.b64encode(data.encode()).decode()
        elif mode == "hex":
            return data.encode().hex()
        elif mode == "url":
            return urllib.parse.quote(data)
        elif mode == "rot13":
            return data.translate(str.maketrans(
                "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz",
                "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm"
            ))
        elif mode == "binary":
            return ' '.join(format(ord(x), '08b') for x in data)
        return data

    # * Decode data dari berbagai format
    def decodeData(self, data, mode="base64"):
        try:
            if mode == "base64":
                return base64.b64decode(data.encode()).decode()
            elif mode == "hex":
                return bytes.fromhex(data).decode()
            elif mode == "url":
                return urllib.parse.unquote(data)
            elif mode == "rot13":
                return self.encodeData(data, "rot13") # Rot13 is reversible
        except Exception:
            return "Error decoding data"
        return data

    # * Generator password kuat untuk kebutuhan audit
    def generatePassword(self, length=16):
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(random.choice(chars) for _ in range(length))
