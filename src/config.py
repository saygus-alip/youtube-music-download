import os
from dotenv import load_dotenv

load_dotenv()

# Download settings
DOWNLOAD_DIR = os.getenv('DOWNLOAD_DIR', 'downloads')
AUDIO_FORMAT = os.getenv('AUDIO_FORMAT', 'mp3')

# Metadata - ใส่หน้าปกและข้อมูลเพลงให้เหมือนเพลงจริง
EMBED_THUMBNAIL = os.getenv('EMBED_THUMBNAIL', 'true').lower() in ('true', '1', 'yes')
EMBED_METADATA = os.getenv('EMBED_METADATA', 'true').lower() in ('true', '1', 'yes')

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')