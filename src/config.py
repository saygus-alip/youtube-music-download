import os
from dotenv import load_dotenv

load_dotenv()

# Download settings
DOWNLOAD_DIR = os.getenv('DOWNLOAD_DIR', 'downloads')
AUDIO_FORMAT = os.getenv('AUDIO_FORMAT', 'mp3')

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')