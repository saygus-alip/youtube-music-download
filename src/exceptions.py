class DownloaderError(Exception):
    """Base exception for downloader"""
    pass

class InvalidURLError(DownloaderError):
    """Invalid YouTube URL"""
    pass

class DownloadFailedError(DownloaderError):
    """Download failed"""
    pass