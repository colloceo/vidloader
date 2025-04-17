from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QComboBox, QMessageBox
import sys
import yt_dlp
import uuid
import os
import logging
from concurrent.futures import ThreadPoolExecutor, TimeoutError

class Downloader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VidLoader Desktop")
        self.setGeometry(200, 200, 400, 250)

        # Set up logging
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('vidloader.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

        # Ensure downloads folder exists
        self.download_dir = os.path.join(os.getcwd(), 'downloads')
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

        # UI setup
        layout = QVBoxLayout()
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter video URL (YouTube, Instagram, TikTok, X)")
        self.format_box = QComboBox()
        self.format_box.addItems(["Video (MP4)", "Audio (MP3 or WebM)"])
        self.download_btn = QPushButton("Download")
        self.status_label = QLabel("Ready to download")
        self.status_label.setWordWrap(True)

        layout.addWidget(QLabel("VidLoader Desktop"))
        layout.addWidget(self.url_input)
        layout.addWidget(self.format_box)
        layout.addWidget(self.download_btn)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

        self.download_btn.clicked.connect(self.download_video)

    def download_video(self):
        url = self.url_input.text().strip()
        format_type = self.format_box.currentText().lower().split()[0]  # 'video' or 'audio'
        if not url:
            QMessageBox.critical(self, "Error", "Please enter a valid URL")
            return

        self.logger.debug(f"Starting download for URL: {url}, Format: {format_type}")
        self.status_label.setText("Processing... Please wait.")
        self.download_btn.setEnabled(False)

        filename_base = str(uuid.uuid4())
        extension = 'mp3' if format_type == 'audio' else 'mp4'
        filename = f"{filename_base}.{extension}"
        output_path = os.path.join(self.download_dir, filename)

        ydl_opts = {
            'outtmpl': output_path,
            'noplaylist': True,
            'quiet': False,
            'no_warnings': False,
            'logger': self.logger,
        }

        if format_type == 'audio':
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'postprocessor_args': ['-loglevel', 'error', '-threads', '1', '-preset', 'ultrafast'],
            })
        else:
            ydl_opts['format'] = 'best[ext=mp4]/best'

        def download_with_ydl():
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            except Exception as e:
                self.logger.error(f"yt_dlp download failed: {str(e)}")
                raise

        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                timeout = 600 if format_type == 'audio' and 'instagram.com' in url.lower() else 300
                future = executor.submit(download_with_ydl)
                future.result(timeout=timeout)

            # Check for downloaded file
            for file in os.listdir(self.download_dir):
                if file.startswith(filename_base):
                    final_filename = f"audio_{filename_base}.mp3" if format_type == 'audio' else f"video_{filename_base}.mp4"
                    self.status_label.setText(f"✅ Download complete: {final_filename}")
                    QMessageBox.information(self, "Success", f"File saved to downloads/{final_filename}")
                    self.logger.debug(f"Download successful: {final_filename}")
                    return

            self.logger.error("File not found after download")
            self.status_label.setText("❌ Error: File not found after download")
            QMessageBox.critical(self, "Error", "File not found after download")

        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e).lower()
            self.logger.error(f"DownloadError: {error_msg}")
            if 'ffmpeg' in error_msg or 'ffprobe' in error_msg:
                if format_type == 'audio':
                    self.logger.debug("Falling back to raw audio download")
                    ydl_opts.update({
                        'format': 'bestaudio/best',
                        'postprocessors': [],
                    })
                    filename = f"{filename_base}.webm"
                    output_path = os.path.join(self.download_dir, filename)
                    try:
                        with ThreadPoolExecutor(max_workers=1) as executor:
                            future = executor.submit(download_with_ydl)
                            future.result(timeout=180)
                        for file in os.listdir(self.download_dir):
                            if file.startswith(filename_base):
                                final_filename = f"audio_{filename_base}.webm"
                                self.status_label.setText(f"✅ Download complete (WebM fallback): {final_filename}")
                                QMessageBox.information(self, "Success", f"File saved to downloads/{final_filename} (WebM due to FFmpeg issue)")
                                self.logger.debug(f"Fallback successful: {final_filename}")
                                return
                        self.logger.error("Fallback file not found")
                        self.status_label.setText("❌ Error: Fallback file not found")
                        QMessageBox.critical(self, "Error", "Fallback file not found")
                    except Exception as fallback_e:
                        self.logger.error(f"Fallback download failed: {str(fallback_e)}")
                        self.status_label.setText("❌ Error: Audio download failed")
                        QMessageBox.critical(self, "Error", "Audio download failed. Try video format or ensure FFmpeg is installed.")
                else:
                    self.status_label.setText("❌ Error: FFmpeg not found")
                    QMessageBox.critical(self, "Error", "FFmpeg is required for audio downloads. Please install FFmpeg.")
            elif 'sign in' in error_msg or 'login' in error_msg:
                self.status_label.setText("❌ Error: Login required")
                QMessageBox.critical(self, "Error", "This content requires login. Please use a publicly accessible URL.")
            elif 'geo-restricted' in error_msg:
                self.status_label.setText("❌ Error: Content geo-restricted")
                QMessageBox.critical(self, "Error", "This content is geo-restricted and cannot be downloaded.")
            elif 'not available' in error_msg or 'unavailable' in error_msg:
                self.status_label.setText("❌ Error: Video not available")
                QMessageBox.critical(self, "Error", "The video is not available or private.")
            else:
                self.status_label.setText("❌ Error: Download failed")
                QMessageBox.critical(self, "Error", f"Failed to download: {str(e)}")
        except TimeoutError:
            self.logger.error(f"Download timed out after {timeout} seconds")
            self.status_label.setText("❌ Error: Download timed out")
            QMessageBox.critical(self, "Error", "Download timed out. Try a shorter video, check your network, or select video format.")
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            self.status_label.setText("❌ Error: Unexpected error")
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")
        finally:
            self.download_btn.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    downloader = Downloader()
    downloader.show()
    sys.exit(app.exec_())