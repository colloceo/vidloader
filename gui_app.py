from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QComboBox, QMessageBox
import sys
import yt_dlp
import uuid
import os

class Downloader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VidLoader Desktop")
        self.setGeometry(200, 200, 400, 200)

        layout = QVBoxLayout()
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("Enter video URL")
        self.format_box = QComboBox()
        self.format_box.addItems(["video", "audio"])
        self.download_btn = QPushButton("Download")
        self.status_label = QLabel("")

        layout.addWidget(self.url_input)
        layout.addWidget(self.format_box)
        layout.addWidget(self.download_btn)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

        self.download_btn.clicked.connect(self.download_video)

    def download_video(self):
        url = self.url_input.text()
        format_type = self.format_box.currentText()
        filename = f"{uuid.uuid4()}.%(ext)s"

        opts = {'outtmpl': os.path.join("downloads", filename)}

        if format_type == 'audio':
            opts['format'] = 'bestaudio'
            opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        else:
            opts['format'] = 'best'

        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])
            self.status_label.setText("✅ Download complete")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    downloader = Downloader()
    downloader.show()
    sys.exit(app.exec_())
