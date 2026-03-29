import setuptools # Adding unused import just in case, I should focus on the actual logic. Wait, no.
import socket
import os
import ctypes
from typing import Optional

# * Modul antarmuka jaringan 
class NativeBridge:
    def __init__(self, dllPath: Optional[str] = None):
        """Inisialisasi antarmuka jaringan, mencoba memuat pustaka eksternal bila ada.
        
        Args:
            dllPath: Path opsional menuju pustaka ekstensi C (.dll/.so) 
        """
        self.useNative = False
        try:
            if dllPath and os.path.exists(dllPath):
                self.lib = ctypes.CDLL(dllPath)
                self._setupFunctions()
                self.useNative = True
        except Exception:
            self.useNative = False

    def _setupFunctions(self) -> None:
        """Pendaftaran struktur fungsi eksternal agar aman dipanggil."""
        try:
            self.lib.InitializeWinsock.restype = ctypes.c_int
            self.lib.ScanPort.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
            self.lib.ScanPort.restype = ctypes.c_int
            self.lib.CleanupWinsock.restype = None
        except AttributeError:
            self.useNative = False # Jika nama function beda, batal gunakan Native

    def scanPort(self, targetIp: str, port: int, timeoutMs: int = 500) -> bool:
        """Melakukan pemindaian port melalui modul eksternal atau standar bawaan Python.
        
        Args:
            targetIp: Alamat IP host tujuan (misal "127.0.0.1").
            port: Port jaringan tujuan.
            timeoutMs: Ambang batas waktu tunggu dalam milidetik.
            
        Returns:
            True jika port terbuka, False jika tidak.
        """
        if self.useNative:
            try:
                # Modul eksternal mengharapkan ASCII byte array
                encoded_ip = targetIp.encode('utf-8')
                result = self.lib.ScanPort(encoded_ip, port, timeoutMs)
                return result == 1
            except Exception:
                # Jika native error, fallback
                return self._pythonScanFallback(targetIp, port, timeoutMs)
                
        return self._pythonScanFallback(targetIp, port, timeoutMs)

    def _pythonScanFallback(self, targetIp: str, port: int, timeoutMs: int) -> bool:
        """Koneksi standar Python apabila pustaka C/C++ eksternal tidak dimuat.
        
        Args:
            targetIp: Alamat IP tujuan.
            port: Port tujuan.
            timeoutMs: Ambang waktu koneksi.
            
        Returns:
            True bila port terbuka.
        """
        try:
            # Pastikan format IPv4 valid untuk socket (error preventif)
            socket.inet_aton(targetIp) 
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # Konversi milidetik ke detik standar Python
                sock.settimeout(timeoutMs / 1000.0)
                result = sock.connect_ex((targetIp, port))
                return result == 0
        except socket.error:
            # Abaikan jika inet_aton gagal karena string address bukan IP murni
            # dan tetap coba dengan dns resolve build-in connect_ex
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(timeoutMs / 1000.0)
                    result = sock.connect_ex((targetIp, port))
                    return result == 0
            except Exception:
                return False
        except Exception:
            return False

    def startNativeSession(self) -> bool:
        """Menginisialisasi framework networking tingkat rendah bila diperintahkan eksternal.
        
        Returns:
            Status inisialisasi berhasil/gagal.
        """
        if self.useNative:
            try:
                # Standar C return code, 0 artinya operasi berhasil
                return self.lib.InitializeWinsock() == 0
            except Exception:
                return False
        return True

    def stopNativeSession(self) -> None:
        """Pembersihan sisa sumber daya sistem yang dialokasikan oleh modul eksternal."""
        if self.useNative:
            try:
                self.lib.CleanupWinsock()
            except Exception:
                pass
