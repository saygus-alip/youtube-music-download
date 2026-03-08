"""YouTube Music Downloader - ดาวน์โหลดเพลงจาก YouTube และ YouTube Music."""

from .config import AUDIO_FORMAT, DOWNLOAD_DIR
from .downloader import download_audio
from .exceptions import DownloadFailedError, InvalidURLError
from .utils import is_valid_youtube_url, validate_youtube_url

__all__ = [
    "AUDIO_FORMAT",
    "DOWNLOAD_DIR",
    "DownloadFailedError",
    "InvalidURLError",
    "download_audio",
    "is_valid_youtube_url",
    "validate_youtube_url",
]
