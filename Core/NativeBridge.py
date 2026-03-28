import socket
import os
import ctypes
from typing import Optional

# * Jembatan antara Python dan C untuk kecepatan eksekusi
class NativeBridge:
    def __init__(self, dllPath: Optional[str] = None):
        if dllPath and os.path.exists(dllPath):
            self.lib = ctypes.CDLL(dllPath)
            self._setupFunctions()
            self.useNative = True
        else:
            self.useNative = False

    # * Daftarkan return type dan argument untuk function C
    def _setupFunctions(self):
        self.lib.InitializeWinsock.restype = ctypes.c_int
        self.lib.ScanPort.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
        self.lib.ScanPort.restype = ctypes.c_int
        self.lib.CleanupWinsock.restype = None

    # * Jalankan scan port dengan fallback ke pure Python
    def scanPort(self, targetIp: str, port: int, timeoutMs: int = 500) -> bool:
        if self.useNative:
            return self.lib.ScanPort(targetIp.encode('utf-8'), port, timeoutMs) == 1
        
        return self._pythonScanFallback(targetIp, port, timeoutMs)

    # * Implementasi cadangan jika library C tidak ditemukan
    def _pythonScanFallback(self, targetIp: str, port: int, timeout: int) -> bool:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout / 1000)
                return sock.connect_ex((targetIp, port)) == 0
        except Exception:
            return False

    # * Awali sesi native networking
    def startNativeSession(self) -> bool:
        if self.useNative:
            return self.lib.InitializeWinsock() == 0
        return True

    # * Bersihkan sesi native networking
    def stopNativeSession(self):
        if self.useNative:
            self.lib.CleanupWinsock()
