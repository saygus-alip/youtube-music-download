#!/usr/bin/env python3
"""YouTube Music Downloader - ดาวน์โหลดเพลงพร้อมหน้าปกและ metadata."""

import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

import customtkinter as ctk

from src.config import AUDIO_FORMAT, DOWNLOAD_DIR
from src.downloader import download_audio
from src.exceptions import DownloadFailedError, InvalidURLError
from src.utils import validate_youtube_url


class YouTubeDownloaderApp:
    """YouTube Music Downloader - GUI สำหรับดาวน์โหลดเพลงพร้อมหน้าปก."""

    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("YouTube Music Downloader")
        self.root.geometry("560x520")
        self.root.minsize(480, 480)

        # State
        self.is_downloading = False
        self.download_dir = DOWNLOAD_DIR

        self._create_widgets()
        self._center_window()

    def _create_widgets(self):
        """Create all GUI widgets."""
        # Container หลัก
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=24, pady=24)

        # === Header - เน้น YouTube Music ===
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill=tk.X, pady=(0, 24))

        # ไอคอน + Title
        title_row = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_row.pack(fill=tk.X)

        # กล่องหน้าปก placeholder (สไตล์ album art)
        art_frame = ctk.CTkFrame(
            title_row,
            width=56,
            height=56,
            corner_radius=8,
            fg_color=("#E53935", "#C62828"),  # YouTube Music red
            border_width=0,
        )
        art_frame.pack(side=tk.LEFT)
        art_frame.pack_propagate(False)

        art_label = ctk.CTkLabel(
            art_frame, text="♪", font=ctk.CTkFont(size=28), text_color="white"
        )
        art_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Title & Subtitle
        text_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        text_frame.pack(side=tk.LEFT, padx=(16, 0))

        title_label = ctk.CTkLabel(
            text_frame,
            text="YouTube Music Downloader",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        title_label.pack(anchor=tk.W)

        subtitle = ctk.CTkLabel(
            text_frame,
            text="ดาวน์โหลดพร้อมหน้าปกและข้อมูลเพลง • MP3 คุณภาพสูง",
            font=ctk.CTkFont(size=12),
            text_color="gray",
        )
        subtitle.pack(anchor=tk.W)

        # === URL Input Card ===
        url_card = ctk.CTkFrame(main_frame, corner_radius=12, fg_color=("#2b2b2b", "#1a1a1a"))
        url_card.pack(fill=tk.X, pady=(0, 16))

        url_inner = ctk.CTkFrame(url_card, fg_color="transparent")
        url_inner.pack(fill=tk.X, padx=20, pady=16)

        ctk.CTkLabel(url_inner, text="ลิงก์เพลง", font=ctk.CTkFont(weight="bold")).pack(
            anchor=tk.W
        )
        self.url_entry = ctk.CTkEntry(
            url_inner,
            placeholder_text="วาง URL จาก YouTube Music หรือ YouTube...",
            height=40,
            font=ctk.CTkFont(size=13),
        )
        self.url_entry.pack(fill=tk.X, pady=(8, 0))
        self.url_entry.insert(0, "https://music.youtube.com/watch?v=")
        self.url_entry.bind("<Return>", lambda e: self._on_download())

        # === Options ===
        options_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        options_frame.pack(fill=tk.X, pady=(0, 16))

        ctk.CTkLabel(options_frame, text="บันทึกที่", font=ctk.CTkFont(weight="bold")).pack(
            anchor=tk.W
        )
        dir_row = ctk.CTkFrame(options_frame, fg_color="transparent")
        dir_row.pack(fill=tk.X, pady=(6, 0))

        self.dir_entry = ctk.CTkEntry(
            dir_row,
            placeholder_text="โฟลเดอร์บันทึกไฟล์",
            height=36,
            font=ctk.CTkFont(size=12),
        )
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.dir_entry.insert(0, self.download_dir)

        browse_btn = ctk.CTkButton(
            dir_row, text="เลือกโฟลเดอร์", width=110, height=36, command=self._browse_dir
        )
        browse_btn.pack(side=tk.LEFT)

        # Info badge
        info_text = f"• {AUDIO_FORMAT.upper()} 192kbps  • หน้าปกอัตโนมัติ  • ชื่อเพลง + ศิลปิน"
        info_label = ctk.CTkLabel(
            options_frame, text=info_text, font=ctk.CTkFont(size=11), text_color="gray"
        )
        info_label.pack(anchor=tk.W, pady=(8, 0))

        # === Buttons ===
        btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        btn_frame.pack(fill=tk.X, pady=(20, 12))

        self.download_btn = ctk.CTkButton(
            btn_frame,
            text="ดาวน์โหลด",
            width=140,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._on_download,
        )
        self.download_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.clear_btn = ctk.CTkButton(
            btn_frame,
            text="ล้าง",
            width=80,
            height=40,
            fg_color=("#404040", "#2d2d2d"),
            hover_color=("#505050", "#3d3d3d"),
            command=self._clear_url,
        )
        self.clear_btn.pack(side=tk.LEFT)

        # === Progress ===
        self.progress = ctk.CTkProgressBar(
            main_frame, mode="indeterminate", indeterminate_speed=1.5
        )
        self.progress.pack(fill=tk.X, pady=(0, 12))

        # === Log ===
        ctk.CTkLabel(main_frame, text="สถานะ", font=ctk.CTkFont(weight="bold")).pack(
            anchor=tk.W
        )
        self.log_text = ctk.CTkTextbox(
            main_frame, height=120, wrap=tk.WORD, state="disabled", font=ctk.CTkFont(size=12)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=(6, 0))

        self._log("พร้อมใช้งาน — วางลิงก์จาก YouTube Music แล้วกดดาวน์โหลด")
        self._log(f"ไฟล์จะบันทึกที่: {os.path.abspath(self.download_dir)}")

    def _center_window(self):
        """Center window on screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"+{x}+{y}")

    def _log(self, message: str):
        """Append message to log area."""
        self.log_text.configure(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.configure(state="disabled")

    def _clear_url(self):
        """Clear URL input."""
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, "https://music.youtube.com/watch?v=")
        self.url_entry.focus()

    def _browse_dir(self):
        """Open folder browser."""
        path = filedialog.askdirectory(
            initialdir=self.dir_entry.get() or self.download_dir
        )
        if path:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, path)

    def _on_download(self):
        """Handle download button click."""
        if self.is_downloading:
            return

        url = self.url_entry.get().strip()
        output_dir = self.dir_entry.get().strip() or self.download_dir

        try:
            validate_youtube_url(url)
        except InvalidURLError as e:
            messagebox.showerror("URL ไม่ถูกต้อง", str(e))
            return

        self.is_downloading = True
        self.download_btn.configure(state="disabled")
        self.progress.start()

        def do_download():
            try:
                self.root.after(0, lambda: self._log(f"กำลังดาวน์โหลด: {url[:55]}..."))
                path = download_audio(url, output_dir)
                self.root.after(0, lambda: self._download_success(path))
            except DownloadFailedError as e:
                self.root.after(0, lambda: self._download_error(str(e)))
            except Exception as e:
                self.root.after(0, lambda: self._download_error(str(e)))
            finally:
                self.root.after(0, self._download_finished)

        thread = threading.Thread(target=do_download, daemon=True)
        thread.start()

    def _download_success(self, path: str):
        """Handle successful download."""
        self._log(f"✓ ดาวน์โหลดสำเร็จ (พร้อมหน้าปก): {os.path.basename(path)}")
        messagebox.showinfo("สำเร็จ", f"ดาวน์โหลดสำเร็จ!\n\n{path}")

    def _download_error(self, message: str):
        """Handle download error."""
        self._log(f"✗ ข้อผิดพลาด: {message}")
        messagebox.showerror("ดาวน์โหลดไม่สำเร็จ", message)

    def _download_finished(self):
        """Reset UI after download completes."""
        self.is_downloading = False
        self.download_btn.configure(state="normal")
        self.progress.stop()

    def run(self):
        """Start the application."""
        self.root.mainloop()


def main():
    """Entry point."""
    app = YouTubeDownloaderApp()
    app.run()


if __name__ == "__main__":
    main()
