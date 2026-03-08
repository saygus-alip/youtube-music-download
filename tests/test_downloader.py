"""Tests for src.downloader module."""

from unittest.mock import MagicMock, patch

import pytest
import yt_dlp

from src.downloader import download_audio
from src.exceptions import DownloadFailedError


class TestDownloadAudio:
    """Tests for download_audio function."""

    @patch("src.downloader.yt_dlp.YoutubeDL")
    def test_extract_info_returns_none_raises(self, mock_ydl_class, tmp_path):
        """Test DownloadFailedError when extract_info returns None."""
        mock_ydl = MagicMock()
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl
        mock_ydl.extract_info.return_value = None

        with pytest.raises(DownloadFailedError, match="ไม่สามารถดึงข้อมูลวิดีโอได้"):
            download_audio("https://youtube.com/watch?v=test", output_dir=str(tmp_path))

    @patch("src.downloader.yt_dlp.YoutubeDL")
    def test_no_audio_file_created_raises(self, mock_ydl_class, tmp_path):
        """Test DownloadFailedError when no mp3 file is created."""
        mock_ydl = MagicMock()
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl
        mock_ydl.extract_info.return_value = {"title": "Test Song"}

        with patch("src.downloader.os.listdir", return_value=[]):
            with pytest.raises(DownloadFailedError, match="ไม่พบไฟล์ที่ดาวน์โหลด"):
                download_audio("https://youtube.com/watch?v=test", output_dir=str(tmp_path))

    @patch("src.downloader.yt_dlp.YoutubeDL")
    def test_download_error_raises(self, mock_ydl_class, tmp_path):
        """Test DownloadFailedError when yt-dlp raises DownloadError."""
        mock_ydl = MagicMock()
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl
        mock_ydl.extract_info.side_effect = yt_dlp.utils.DownloadError("Video unavailable")

        with pytest.raises(DownloadFailedError, match="ดาวน์โหลดไม่สำเร็จ"):
            download_audio("https://youtube.com/watch?v=test", output_dir=str(tmp_path))
