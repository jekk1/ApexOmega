@echo off
setlocal enabledelayedexpansion
echo [*] Cleaning previous build...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

echo [*] Detecting Python environment paths (v5.9.7 Portable)...
for /f "delims=" %%i in ('python -c "import sys,os; print(os.path.join(sys.base_prefix, 'tcl'))"') do set "PYTHON_TCL=%%i"
for /f "delims=" %%i in ('python -c "import sys,os; print(os.path.join(sys.base_prefix, 'DLLs'))"') do set "PYTHON_DLLS=%%i"
for /f "delims=" %%i in ('python -c "import customtkinter,os; print(os.path.dirname(customtkinter.__file__))"') do set "CTK_PATH=%%i"

echo [+] TCL Path : %PYTHON_TCL%
echo [+] DLLs Path: %PYTHON_DLLS%
echo [+] CTK Path : %CTK_PATH%

echo [*] Starting PyInstaller Build (v5.9.7 Ultimate)...
pyinstaller --noconfirm --onefile --windowed --clean --name "ApexOmega_Ultimate" ^
 --icon "app_icon.ico" ^
 --add-data "%PYTHON_TCL%;tcl/" ^
 --add-binary "%PYTHON_DLLS%\tcl86t.dll;." ^
 --add-binary "%PYTHON_DLLS%\tk86t.dll;." ^
 --add-binary "%PYTHON_DLLS%\_tkinter.pyd;." ^
 --add-data "%CTK_PATH%;customtkinter/" ^
 --add-data "Modules;Modules" ^
 --add-data "UI;UI" ^
 --add-data "Core;Core" ^
 --add-data "app_icon.ico;." ^
 --add-data "version.txt;." ^
 --hidden-import=customtkinter ^
 --hidden-import=darkdetect ^
 --hidden-import=_tkinter ^
 ApexOmega.py

echo [+] Build Complete! Check dist/ folder.
pause
