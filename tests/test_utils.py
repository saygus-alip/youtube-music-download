"""Tests for src.utils module."""

import pytest

from src.exceptions import InvalidURLError
from src.utils import is_valid_youtube_url, validate_youtube_url


class TestIsValidYouTubeUrl:
    """Tests for is_valid_youtube_url."""

    def test_valid_youtube_watch_url(self):
        assert is_valid_youtube_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ") is True
        assert is_valid_youtube_url("http://youtube.com/watch?v=dQw4w9WgXcQ") is True

    def test_valid_youtu_be_url(self):
        assert is_valid_youtube_url("https://youtu.be/dQw4w9WgXcQ") is True

    def test_valid_music_youtube_url(self):
        assert is_valid_youtube_url("https://music.youtube.com/watch?v=dQw4w9WgXcQ") is True

    def test_valid_youtube_embed_url(self):
        assert is_valid_youtube_url("https://www.youtube.com/embed/dQw4w9WgXcQ") is True

    def test_invalid_url(self):
        assert is_valid_youtube_url("https://example.com/video") is False
        assert is_valid_youtube_url("not a url") is False

    def test_empty_or_whitespace(self):
        assert is_valid_youtube_url("") is False
        assert is_valid_youtube_url("   ") is False

    def test_url_with_whitespace_stripped(self):
        assert is_valid_youtube_url("  https://youtu.be/dQw4w9WgXcQ  ") is True


class TestValidateYouTubeUrl:
    """Tests for validate_youtube_url."""

    def test_valid_url_returns_cleaned(self):
        url = "  https://youtu.be/dQw4w9WgXcQ  "
        assert validate_youtube_url(url) == "https://youtu.be/dQw4w9WgXcQ"

    def test_empty_raises(self):
        with pytest.raises(InvalidURLError, match="กรุณาใส่ URL"):
            validate_youtube_url("")
        with pytest.raises(InvalidURLError, match="กรุณาใส่ URL"):
            validate_youtube_url("   ")

    def test_invalid_url_raises(self):
        with pytest.raises(InvalidURLError, match="URL ไม่ถูกต้อง"):
            validate_youtube_url("https://example.com/video")
