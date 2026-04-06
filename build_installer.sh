#!/usr/bin/env bash
# build_installer.sh
# สร้างไฟล์ binary สำหรับ Linux/macOS ด้วย PyInstaller
# วิธีใช้: chmod +x build_installer.sh && ./build_installer.sh

set -e

echo "=============================="
echo " GtsAlpha Caption Pro Builder"
echo "=============================="
echo

echo "[1/4] ติดตั้ง dependencies..."
pip install -r requirements.txt --quiet

echo "[2/4] ติดตั้ง PyInstaller..."
pip install pyinstaller --quiet

echo "[3/4] กำลัง Build binary..."
pyinstaller GtsAlpha_Caption_Pro.spec --clean --noconfirm

echo
echo "[4/4] Build สำเร็จ!"
echo " ไฟล์ binary อยู่ที่: dist/GtsAlpha_Caption_Pro"
echo " รัน: ./dist/GtsAlpha_Caption_Pro"
