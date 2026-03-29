@echo off
echo [*] Cleaning previous build...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

echo [*] Starting PyInstaller Build (v5.9.4 Ultimate)...
pyinstaller --noconfirm --onefile --windowed --name "ApexOmega_Ultimate" ^
 --icon "app_icon.ico" ^
 --add-data "C:\Users\Pongo\AppData\Local\Programs\Python\Python313\Lib\site-packages\customtkinter;customtkinter/" ^
 --add-data "Modules;Modules" ^
 --add-data "UI;UI" ^
 --add-data "Core;Core" ^
 --add-data "app_icon.ico;." ^
 --add-data "version.txt;." ^
 --hidden-import=customtkinter ^
 --hidden-import=darkdetect ^
 ApexOmega.py

echo [+] Build Complete! Check dist/ folder.
pause
