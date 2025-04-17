VidLoader
VidLoader is a free, open-source tool to download videos and audio from platforms like YouTube, Instagram, TikTok, and X. It offers two interfaces:

Web App: A Flask-based web application for browser-based downloads.
Desktop App: A PyQt5-based desktop application for Windows, macOS, and Linux.

Built with yt_dlp and FFmpeg, VidLoader supports MP4 video and MP3 audio downloads, with a WebM fallback for audio if FFmpeg conversion fails. The project is designed for ease of use, reliability, and cross-platform compatibility.
Features

Download videos (MP4) and audio (MP3 or WebM) from YouTube, Instagram, TikTok, and X.
User-friendly web interface with dark mode and mobile support.
Desktop app with a simple GUI for offline use.
Optimized FFmpeg for fast audio conversion (-preset ultrafast).
WebM fallback for audio downloads if FFmpeg is unavailable.
Detailed error handling for login issues, geo-restrictions, and timeouts.
Logging for debugging (vidloader.log).
Saves files to the user’s Downloads folder (e.g., C:\Users\<User>\Downloads or /sdcard/Download).

Screenshots
Web App Interface
Desktop App Interface
Installation
Prerequisites

Python 3.8+: Required for both apps.
FFmpeg: Needed for audio (MP3) conversion. Download from gyan.dev (Windows) or install via package manager (e.g., sudo apt-get install ffmpeg on Linux).
Git: For cloning the repository.

Project Structure
VidLoader/
├── web/
│   ├── templates/
│   │   └── index.html
│   ├── web_app.py
│   └── requirements.txt
├── desktop/
│   ├── gui_app.py
│   └── requirements.txt
├── ffmpeg/
│   ├── ffmpeg.exe
│   └── ffprobe.exe
├── screenshots/
├── README.md
└── LICENSE

Web App Setup

Clone the Repository:git clone https://github.com/colloceo/VidLoader.git
cd VidLoader/web


Set Up Virtual Environment:python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate


Install Dependencies:pip install -r requirements.txt

requirements.txt:flask==3.0.3
yt-dlp==2024.8.6
gunicorn==22.0.0
requests==2.31.0


Install FFmpeg:
Windows: Place ffmpeg.exe and ffprobe.exe in VidLoader/ffmpeg/.
Linux/macOS: Install via sudo apt-get install ffmpeg or brew install ffmpeg.


Run Locally:python web_app.py


Open http://127.0.0.1:5000 in a browser.



Desktop App Setup

Navigate to Desktop Folder:cd VidLoader/desktop


Set Up Virtual Environment:python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate


Install Dependencies:pip install -r requirements.txt

requirements.txt:PyQt5==5.15.9
yt-dlp==2024.8.6
requests==2.31.0


Install FFmpeg:
Same as for the web app.


Run the App:python gui_app.py


A PyQt5 window will appear for downloading.



Standalone Executable (Windows)

Install PyInstaller:pip install pyinstaller==5.13.0


Build Executable:cd desktop
pyinstaller --add-binary "../ffmpeg/ffmpeg.exe;ffmpeg" --add-binary "../ffmpeg/ffprobe.exe;ffmpeg" --add-data "vidloader.log;." -F -n VidLoader gui_app.py


Run:
Find VidLoader.exe in dist/.
Double-click to launch.



Usage
Web App

Open the app in a browser (http://127.0.0.1:5000 locally).
Enter a public URL (e.g., https://youtu.be/wpJX49k9Wqk).
Select “Video” or “Audio”.
Click “Download Now”.
Check your Downloads folder for video_<uuid>.mp4, audio_<uuid>.mp3, or audio_<uuid>.webm.

Desktop App

Launch the app (gui_app.py or VidLoader.exe).
Enter a public URL.
Choose “Video (MP4)” or “Audio (MP3 or WebM)”.
Click “Download”.
View the status label and pop-up for success or errors.
Files save to your Downloads folder.

Notes:

Use public URLs to avoid login errors.
Instagram URLs should be clean (e.g., https://www.instagram.com/reel/DIgNemUo2TQ/).
Audio downloads may fall back to WebM if FFmpeg fails.

Production Deployment
Web App

Deploy on platforms like PythonAnywhere, Heroku, or Render.
Install FFmpeg on the server (e.g., apt-get install ffmpeg on Linux).
Use a WSGI server like Gunicorn.
Example for PythonAnywhere (see deployment guide in the repository).

Desktop App

Distribute VidLoader.exe via GitHub Releases or a website.
Bundle FFmpeg binaries in the executable.
Comply with GPL licensing for FFmpeg and PyQt5.

Troubleshooting

FFmpeg Errors: Ensure FFmpeg is installed and accessible. Check vidloader.log for details.
Timeouts: Try shorter videos or select video format (faster than audio).
Login Errors: Use public URLs or check platform restrictions.
Logs: Find vidloader.log in the app directory or executable folder.

Contributing
Contributions are welcome! Please:

Fork the repository.
Create a feature branch (git checkout -b feature/YourFeature).
Commit changes (git commit -m "Add YourFeature").
Push to the branch (git push origin feature/YourFeature).
Open a pull request.

License
VidLoader is open-source under the GNU General Public License v3.0 due to FFmpeg and PyQt5 dependencies. Key components:

FFmpeg: GPL
PyQt5: GPL
yt_dlp: Unlicense
Flask: BSD

See LICENSE for details. If distributing, include source code or obtain commercial licenses for FFmpeg/PyQt5.
Support

Issues: Report bugs or feature requests on the Issues page.
Contact: Reach out via GitHub Discussions.
Donate: Support development at Buy Me a Coffee.

Acknowledgments

yt_dlp for downloading functionality.
FFmpeg for audio conversion.
Flask and PyQt5 for the interfaces.


VidLoader: Download videos and audio with ease. Built for content lovers, by content lovers.
