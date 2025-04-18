🎥 VidLoader
VidLoader is a free, open-source tool to download videos and audio from major platforms like YouTube, Instagram, TikTok, and X (Twitter). It’s designed to be user-friendly, fast, and cross-platform with two powerful interfaces:

🌐 Web App: Flask-based web interface (with mobile and dark mode support).
🖥️ Desktop App: PyQt5 GUI for Windows, macOS, and Linux.


🚀 Features

🔻 Download videos (MP4) and audio (MP3/WebM).
🌓 Dark mode and 📱 mobile-responsive web UI.
🖥️ Simple and sleek desktop GUI (offline use).
⚡ Fast audio conversion using FFmpeg (-preset ultrafast).
🔁 WebM fallback if FFmpeg is unavailable.
🧠 Intelligent error handling for login issues, geo-restrictions, and timeouts.
📁 Files saved automatically to the user’s Downloads folder:
Windows: C:\Users\<User>\Downloads
Android: /sdcard/Download


📝 Logs all activities to vidloader.log for easy debugging.


🔧 Installation
✅ Prerequisites

Python 3.8+
FFmpeg (for audio conversion):
Windows: Download from gyan.dev or install via Chocolatey (choco install ffmpeg)
Linux: sudo apt-get install ffmpeg
macOS: brew install ffmpeg


Git


🌐 Web App Setup
# Clone the repo
git clone https://github.com/colloceo/VidLoader.git
cd VidLoader/web

# Virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

requirements.txt:
flask==3.0.3
yt-dlp==2024.8.6
gunicorn==22.0.0
requests==2.31.0

Install FFmpeg:

Place ffmpeg.exe and ffprobe.exe in VidLoader/ffmpeg/ (Windows only)

Run Locally:
python web_app.py

Open in browser:http://127.0.0.1:5000

🖥️ Desktop App Setup
cd VidLoader/desktop

# Virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

requirements.txt:
PyQt5==5.15.9
yt-dlp==2024.8.6
requests==2.31.0

Run the App:
python gui_app.py


📦 Releases
VidLoader v1.0.0 - Windows

Released: April 18, 2025
Download: VidLoader-v1.0.0-Windows.zip
Features:
Windows executable (VidLoader.exe) with custom icon.
Downloads videos (MP4) and audio (MP3/WebM) from YouTube, Instagram, TikTok, and X.
Built with PyQt5, yt-dlp, and FFmpeg.


Installation:
Download and extract VidLoader-v1.0.0-Windows.zip.
Double-click VidLoader.exe to run.
Paste a public video/audio URL and select format.


Notes:
Requires Windows 7/8/10/11 (64-bit).
Logs saved to vidloader.log in the same folder.
Source code included for GPL compliance.




📦 Build Windows Executable
pip install pyinstaller==5.13.0
cd desktop

pyinstaller --add-binary "../ffmpeg/ffmpeg.exe;ffmpeg" \
            --add-binary "../ffmpeg/ffprobe.exe;ffmpeg" \
            --add-data "vidloader.log;." \
            --icon "vidloader.ico" \
            -F -w -n VidLoader gui_app.py


Find VidLoader.exe in the dist/ folder.


✅ Usage
🌐 Web App

Visit http://127.0.0.1:5000
Paste a public video/audio URL
Select Video or Audio
Click Download Now
File will save in your Downloads folder

🖥️ Desktop App

Run gui_app.py or VidLoader.exe
Paste the URL
Choose MP4 or MP3/WebM
Click Download
Watch the status and confirm file saved


⚠️ Notes & Tips

Always use public URLs to avoid login errors
Use clean Instagram URLs (e.g., https://www.instagram.com/reel/xyz/)
If MP3 fails, WebM is used as a fallback (no FFmpeg needed)
Shorter videos = faster processing


🚀 Deployment
🌐 Web App Hosting

Platforms: PythonAnywhere, Heroku, Render
Make sure FFmpeg is installed on your server
Use a WSGI server like Gunicorn:gunicorn web_app:app



🖥️ Desktop App Distribution

Upload .exe to GitHub or your website
Bundle FFmpeg in the dist/ folder
Ensure GPL license compliance


🛠️ Troubleshooting



Problem
Fix



FFmpeg not working
Ensure ffmpeg/ffprobe are in place


Login errors
Use public links only


Timeouts
Shorten video length


Logs not showing
Check vidloader.log in app folder



🤝 Contributing
We welcome all contributions!
# Fork and clone
git clone https://github.com/yourusername/VidLoader.git

# Create feature branch
git checkout -b feature/YourFeature

# Make changes and commit
git commit -m "Add YourFeature"

# Push and open a PR
git push origin feature/YourFeature


📝 License
VidLoader is licensed under GNU GPL v3.0 due to dependencies:

FFmpeg: GPL
PyQt5: GPL
yt-dlp: Unlicense
Flask: BSD

📄 See LICENSE for full details. Distributors must include source code or acquire commercial licenses.

☕ Support & Contact

GitHub Issues: Bug reports & feature requests
GitHub Discussions: Community & help
Buy Me a Coffee: Donate to support development


🙏 Acknowledgments

🧠 yt_dlp – Download backend
🎧 FFmpeg – Audio conversion
🌐 Flask – Web interface
🖥️ PyQt5 – Desktop GUI



VidLoader: Download videos and audio with ease. Built for content lovers, by content lovers. 🎬


