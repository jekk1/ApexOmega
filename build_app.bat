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

echo [*] Starting PyInstaller Build (v6.3.0 Ultimate)...
pyinstaller --noconfirm --clean ApexOmega_Ultimate.spec

echo [+] Build Complete! Check dist/ folder.
pause
