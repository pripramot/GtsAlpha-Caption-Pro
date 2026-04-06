@echo off
:: build_installer.bat
:: สร้างไฟล์ .exe สำหรับ Windows ด้วย PyInstaller
:: วิธีใช้: ดับเบิลคลิก build_installer.bat

echo ==============================
echo  GtsAlpha Caption Pro Builder
echo ==============================
echo.

:: ตรวจสอบ Python
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo [ERROR] ไม่พบ Python กรุณาติดตั้ง Python 3.9+ ก่อน
    echo  https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/4] ติดตั้ง dependencies...
pip install -r requirements.txt --quiet
IF ERRORLEVEL 1 (
    echo [ERROR] ติดตั้ง requirements ไม่สำเร็จ
    pause
    exit /b 1
)

echo [2/4] ติดตั้ง PyInstaller...
pip install pyinstaller --quiet
IF ERRORLEVEL 1 (
    echo [ERROR] ติดตั้ง PyInstaller ไม่สำเร็จ
    pause
    exit /b 1
)

echo [3/4] กำลัง Build .exe ...
pyinstaller GtsAlpha_Caption_Pro.spec --clean --noconfirm
IF ERRORLEVEL 1 (
    echo [ERROR] Build ล้มเหลว ตรวจสอบ log ด้านบน
    pause
    exit /b 1
)

echo.
echo [4/4] Build สำเร็จ!
echo  ไฟล์ .exe อยู่ที่: dist\GtsAlpha_Caption_Pro.exe
echo.
echo กด Enter เพื่อเปิดโฟลเดอร์ dist ...
pause
explorer dist
