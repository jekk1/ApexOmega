import base64
import urllib.parse

# * Modul generator payload sederhana buat bypass/test (v4.7)
class PayloadGen:
    def __init__(self):
        pass

    # * Encode teks ke berbagai format
    def generate(self, text):
        results = {}
        try:
            # -- Base64 --
            b64_bytes = base64.b64encode(text.encode("utf-8"))
            results["Base64"] = b64_bytes.decode("utf-8")
            
            # -- Hex --
            results["Hex"] = text.encode("utf-8").hex()
            
            # -- URL Encode --
            results["URL"] = urllib.parse.quote(text)
            
            # -- HTML Entity (Simple) --
            results["HTML"] = text.replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;")
            
            return results
        except Exception:
            return None

    # * Decode teks dari format tertentu
    def decode(self, text, format_type="base64"):
        try:
            if format_type.lower() == "base64":
                return base64.b64decode(text).decode("utf-8")
            elif format_type.lower() == "hex":
                return bytes.fromhex(text).decode("utf-8")
            elif format_type.lower() == "url":
                return urllib.parse.unquote(text)
            return "Format not supported"
        except Exception:
            return "Decoding error: Invalid format"
