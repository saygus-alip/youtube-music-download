"""Utility functions for YouTube Music Downloader."""

import re

from .exceptions import InvalidURLError

# YouTube URL patterns
YOUTUBE_URL_PATTERNS = [
    r"(?:https?://)?(?:www\.)?youtube\.com/watch\?v=[\w-]+",
    r"(?:https?://)?(?:www\.)?youtube\.com/embed/[\w-]+",
    r"(?:https?://)?(?:www\.)?youtu\.be/[\w-]+",
    r"(?:https?://)?(?:www\.)?music\.youtube\.com/watch\?v=[\w-]+",
]


def is_valid_youtube_url(url: str) -> bool:
    """Check if the given string is a valid YouTube URL."""
    if not url or not url.strip():
        return False
    url = url.strip()
    for pattern in YOUTUBE_URL_PATTERNS:
        if re.match(pattern, url):
            return True
    return False


def validate_youtube_url(url: str) -> str:
    """
    Validate YouTube URL and return cleaned URL.
    Raises InvalidURLError if invalid.
    """
    if not url or not url.strip():
        raise InvalidURLError("กรุณาใส่ URL")
    cleaned = url.strip()
    if not is_valid_youtube_url(cleaned):
        raise InvalidURLError("URL ไม่ถูกต้อง กรุณาใส่ลิงก์ YouTube หรือ YouTube Music")
    return cleaned
