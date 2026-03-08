@echo off
REM รัน YouTube Music Downloader โดยไม่ต้อง activate venv
"%~dp0.venv\Scripts\python.exe" "%~dp0main.py" %*
