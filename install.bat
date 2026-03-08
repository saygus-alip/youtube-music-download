@echo off
chcp 65001 >nul
echo ========================================
echo  YouTube Music Downloader - ติดตั้ง
echo ========================================
echo.

REM ตรวจสอบ Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] ไม่พบ Python กรุณาติดตั้ง Python 3.8+ จาก python.org
    pause
    exit /b 1
)

REM สร้าง venv ถ้ายังไม่มี
if not exist ".venv" (
    echo [1/3] สร้าง virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] สร้าง venv ไม่สำเร็จ
        pause
        exit /b 1
    )
    echo      สร้าง .venv เรียบร้อย
) else (
    echo [1/3] พบ .venv แล้ว
)

REM ติดตั้ง dependencies
echo.
echo [2/3] ติดตั้ง dependencies...
.venv\Scripts\python.exe -m pip install --upgrade pip -q
.venv\Scripts\python.exe -m pip install -r requirements.txt -q
.venv\Scripts\python.exe -m pip install -r requirements-dev.txt -q
if errorlevel 1 (
    echo [ERROR] ติดตั้ง dependencies ไม่สำเร็จ
    pause
    exit /b 1
)
echo      ติดตั้งเรียบร้อย

REM สร้าง .env จาก .env.example ถ้ายังไม่มี
echo.
if not exist ".env" (
    echo [3/3] สร้างไฟล์ .env จาก .env.example...
    copy .env.example .env >nul
    echo      สร้าง .env เรียบร้อย
) else (
    echo [3/3] พบ .env แล้ว
)

echo.
echo ========================================
echo  ติดตั้งเสร็จสมบูรณ์!
echo ========================================
echo.
echo  รันโปรแกรม: ดับเบิลคลิก run.bat
echo  หรือ: .venv\Scripts\python.exe main.py
echo.
echo  หมายเหตุ: ต้องติดตั้ง FFmpeg ในระบบ
echo            ดาวน์โหลดได้ที่ https://ffmpeg.org
echo.
pause
