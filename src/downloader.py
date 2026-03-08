"""YouTube Music downloader using yt-dlp - ดาวน์โหลดพร้อมหน้าปกและ metadata."""

import os

import yt_dlp

from .config import (
    AUDIO_FORMAT,
    DOWNLOAD_DIR,
    EMBED_METADATA,
    EMBED_THUMBNAIL,
)
from .exceptions import DownloadFailedError
from .logger import get_logger

logger = get_logger(__name__)


def download_audio(url: str, output_dir: str | None = None) -> str:
    """
    Download audio from YouTube/YouTube Music พร้อมหน้าปกและ metadata.

    ไฟล์ที่ได้จะมี:
    - หน้าปก (Album Art) จาก thumbnail ของวิดีโอ
    - Metadata: ชื่อเพลง, ศิลปิน, ช่อง

    Args:
        url: YouTube/YouTube Music URL
        output_dir: โฟลเดอร์บันทึก (default: จาก config)

    Returns:
        Path ไปยังไฟล์ที่ดาวน์โหลด

    Raises:
        DownloadFailedError: ถ้าดาวน์โหลดไม่สำเร็จ
    """
    out_dir = output_dir or DOWNLOAD_DIR
    os.makedirs(out_dir, exist_ok=True)

    output_template = os.path.join(out_dir, "%(title)s.%(ext)s")

    # Postprocessors: ลำดับสำคัญ! ต้องเป็น ExtractAudio -> Metadata -> Thumbnail
    postprocessors = [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": AUDIO_FORMAT,
            "preferredquality": "192",
        },
    ]
    if EMBED_METADATA:
        postprocessors.append({"key": "FFmpegMetadata", "add_metadata": True})
    if EMBED_THUMBNAIL:
        postprocessors.append({"key": "EmbedThumbnail", "already_have_thumbnail": False})

    ydl_opts = {
        "format": "bestaudio/best",
        "writethumbnail": EMBED_THUMBNAIL,
        "postprocessors": postprocessors,
        "outtmpl": output_template,
        "quiet": True,
        "no_warnings": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if info is None:
                raise DownloadFailedError("ไม่สามารถดึงข้อมูลวิดีโอได้")

            # Find the downloaded file (most recently modified)
            files = [
                os.path.join(out_dir, f)
                for f in os.listdir(out_dir)
                if f.endswith(f".{AUDIO_FORMAT}")
            ]
            if not files:
                raise DownloadFailedError("ไม่พบไฟล์ที่ดาวน์โหลด")

            output_path = max(files, key=os.path.getmtime)
            logger.info("ดาวน์โหลดสำเร็จ (พร้อมหน้าปก): %s", output_path)
            return output_path

    except yt_dlp.utils.PostProcessingError as e:
        # บางวิดีโอ metadata ยาวเกินไป - ไฟล์อาจถูกสร้างแล้ว (มีแค่ไม่มี thumbnail)
        logger.warning("PostProcessing error, checking for existing file: %s", e)
        files = [os.path.join(out_dir, f) for f in os.listdir(out_dir) if f.endswith(f".{AUDIO_FORMAT}")]
        if files:
            output_path = max(files, key=os.path.getmtime)
            logger.info("ดาวน์โหลดสำเร็จ (ไม่มีหน้าปก): %s", output_path)
            return output_path
        raise DownloadFailedError(f"ประมวลผลไฟล์ไม่สำเร็จ: {str(e)}") from e
    except yt_dlp.utils.DownloadError as e:
        logger.exception("Download error: %s", e)
        raise DownloadFailedError(f"ดาวน์โหลดไม่สำเร็จ: {str(e)}") from e
    except Exception as e:
        logger.exception("Unexpected error: %s", e)
        raise DownloadFailedError(f"เกิดข้อผิดพลาด: {str(e)}") from e
