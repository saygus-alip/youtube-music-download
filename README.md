# YouTube Music Downloader 🎵

โปรแกรมดาวน์โหลดเพลงจาก YouTube และ YouTube Music ด้วย CustomTkinter GUI

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ ฟีเจอร์

- ดาวน์โหลดเพลงจาก YouTube และ YouTube Music
- แปลงเป็นไฟล์ MP3 (หรือรูปแบบอื่นตาม config)
- GUI สวยงามด้วย CustomTkinter (Dark mode)
- เลือกโฟลเดอร์บันทึกได้
- รองรับ URL หลายรูปแบบ (youtube.com, youtu.be, music.youtube.com)

## 📋 ความต้องการ

- **Python 3.8+**
- **FFmpeg** – สำหรับแปลงเป็นไฟล์ MP3 ([ดาวน์โหลด](https://ffmpeg.org/download.html))
- **pip**

## 🚀 การติดตั้ง

### วิธีที่ 1: ใช้ install.bat (Windows – แนะนำ)

1. ดับเบิลคลิก `install.bat`
2. รอจนติดตั้งเสร็จ
3. ดับเบิลคลิก `run.bat` เพื่อรันโปรแกรม

### วิธีที่ 2: ติดตั้งด้วยมือ

```bash
# 1. Clone repository
git clone https://github.com/saygus-alip/youtube-music-download.git
cd youtube-music-download

# 2. สร้าง virtual environment
python -m venv .venv

# 3. ติดตั้ง dependencies (ใช้ path เต็มของ python ใน venv)
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m pip install -r requirements-dev.txt

# 4. (Optional) สร้างไฟล์ .env
copy .env.example .env
```

### ติดตั้ง FFmpeg

- **Windows:** ดาวน์โหลดจาก [ffmpeg.org](https://ffmpeg.org/download.html) แล้วเพิ่มไปที่ PATH
- **macOS:** `brew install ffmpeg`
- **Linux:** `sudo apt install ffmpeg` (Ubuntu/Debian)

## 📖 การใช้งาน

### รันโปรแกรม

**วิธีที่ง่ายที่สุด:** ดับเบิลคลิก `run.bat`

หรือใช้คำสั่ง:
```bash
.venv\Scripts\python.exe main.py
```

### ติดตั้งเป็น package

```bash
.venv\Scripts\python.exe -m pip install -e .
youtube-music-download
```

## ⚙️ การตั้งค่า

แก้ไขไฟล์ `.env` (คัดลอกจาก `.env.example`):

| ตัวแปร | คำอธิบาย | ค่าเริ่มต้น |
|--------|----------|-------------|
| DOWNLOAD_DIR | โฟลเดอร์บันทึกไฟล์ | downloads |
| AUDIO_FORMAT | รูปแบบไฟล์ (mp3, m4a, opus, wav) | mp3 |
| LOG_LEVEL | ระดับ log | INFO |

## 🧪 รัน Tests

```bash
.venv\Scripts\python.exe -m pytest tests/ -v
```

## ⚠️ แก้ปัญหา

**ModuleNotFoundError: No module named 'customtkinter'**
```bash
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

**ModuleNotFoundError: No module named 'setuptools'**
```bash
.venv\Scripts\python.exe -m pip install setuptools
```

**PowerShell: ไม่อนุญาตให้รันสคริปต์**
- ใช้ `run.bat` หรือ `install.bat` แทน
- หรือรัน: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**FFmpeg not found / ดาวน์โหลดไม่สำเร็จ**
- ตรวจสอบว่า FFmpeg ติดตั้งแล้ว: `ffmpeg -version`
- ตรวจสอบว่า FFmpeg อยู่ใน PATH

## 📁 โครงสร้างโปรเจกต์

```
youtube-music-download/
├── main.py              # CustomTkinter GUI หลัก
├── install.bat          # สคริปต์ติดตั้ง (Windows)
├── run.bat              # สคริปต์รันโปรแกรม
├── pyproject.toml       # การตั้งค่าโปรเจกต์
├── requirements.txt    # Dependencies หลัก
├── requirements-dev.txt # Dependencies สำหรับพัฒนา
├── src/
│   ├── config.py        # การตั้งค่า
│   ├── downloader.py    # ใช้ yt-dlp ดาวน์โหลด
│   ├── utils.py         # ตรวจสอบ URL
│   ├── exceptions.py    # Custom exceptions
│   └── logger.py        # Logging
└── tests/
    ├── test_utils.py
    └── test_downloader.py
```

## 📄 License

MIT License
