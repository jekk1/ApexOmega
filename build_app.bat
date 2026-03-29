@echo off
echo [*] Memulai proses pembangunan Apex Omega Ultimate Edition (ONEFILE)...
echo [*] Membersihkan folder build lama...
if exist build rd /s /q build
if exist dist rd /s /q dist
if exist *.spec del /f /q *.spec

echo [*] Menjalankan PyInstaller dengan target ONEFILE...
pyinstaller --noconfirm --onefile --windowed --name "ApexOmega_Ultimate" --icon "app_icon.ico" --add-data "Modules;Modules" --add-data "UI;UI" --add-data "Core;Core" --add-data "app_icon.ico;." --add-data "version.txt;." --hidden-import=customtkinter --hidden-import=darkdetect --collect-all customtkinter ApexOmega.py

echo.
if %errorlevel% equ 0 (
    echo [SUCCESS] File EXE tunggal berhasil dibuat di folder dist/
    echo [INFO] Cari file ApexOmega_Ultimate.exe di dalam folder dist/
) else (
    echo [ERROR] Terjadi kesalahan saat proses build.
)
pause
