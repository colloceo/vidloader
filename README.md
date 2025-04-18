# 🎥 VidLoader

**VidLoader** is a free, open-source tool to download videos and audio from major platforms like **YouTube**, **Instagram**, **TikTok**, and **X (Twitter)**. It’s designed to be user-friendly, fast, and cross-platform with two powerful interfaces:

- 🌐 **Web App**: Flask-based web interface (with mobile and dark mode support).
- 🖥️ **Desktop App**: PyQt5 GUI for Windows, macOS, and Linux.

---

## 🚀 Features

- 🔻 Download **videos (MP4)** and **audio (MP3/WebM)**.
- 🌓 **Dark mode** and 📱 **mobile-responsive web UI**.
- 🖥️ Simple and sleek **desktop GUI** (offline use).
- ⚡ Fast audio conversion using **FFmpeg (`-preset ultrafast`)**.
- 🔁 WebM fallback if FFmpeg is unavailable.
- 🧠 Intelligent error handling for login issues, geo-restrictions, and timeouts.
- 📁 Files saved automatically to the user’s **Downloads** folder:
  - Windows: `C:\Users\<User>\Downloads`
  - Android: `/sdcard/Download`
- 📝 Logs all activities to `vidloader.log` for easy debugging.

---

## 📁 Project Structure

```
VidLoader/
├── web/
│   ├── templates/
│      └── index.html
├── web_app.py # for flasck backend
│   
├── gui_app.py # for descktop app
│  
├── downloads/
├
└── requirements.txt
```

---

## 🔧 Installation

### ✅ Prerequisites

- Python 3.8+
- FFmpeg (for audio conversion):
  - **Windows**: [Download from gyan.dev](https://www.gyan.dev/ffmpeg/builds/)
  - **Linux**: `sudo apt-get install ffmpeg`
  - **macOS**: `brew install ffmpeg`
- Git

---

## 🌐 Web App Setup

```bash
# Clone the repo
git clone https://github.com/colloceo/VidLoader.git
cd VidLoader/web

# Virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**`requirements.txt`:**
```
flask==3.0.3
yt-dlp==2024.8.6
gunicorn==22.0.0
requests==2.31.0
```

**Install FFmpeg:**
- Place `ffmpeg.exe` and `ffprobe.exe` in `VidLoader/ffmpeg/` (Windows only)

**Run Locally:**
```bash
python web_app.py
```

**Open in browser:**
[http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🖥️ Desktop App Setup

```bash
cd VidLoader/desktop

# Virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**`requirements.txt`:**
```
PyQt5==5.15.9
yt-dlp==2024.8.6
requests==2.31.0
```

**Run the App:**
```bash
python gui_app.py
```

---

## 📦 Build Windows Executable

```bash
pip install pyinstaller==5.13.0
cd desktop

pyinstaller --add-binary "../ffmpeg/ffmpeg.exe;ffmpeg" \
            --add-binary "../ffmpeg/ffprobe.exe;ffmpeg" \
            --add-data "vidloader.log;." \
            -F -n VidLoader gui_app.py
```

- Find `VidLoader.exe` in the `dist/` folder.

---

## ✅ Usage

### 🌐 Web App

1. Visit `http://127.0.0.1:5000`
2. Paste a public video/audio URL
3. Select **Video** or **Audio**
4. Click **Download Now**
5. File will save in your Downloads folder

### 🖥️ Desktop App

1. Run `gui_app.py` or `VidLoader.exe`
2. Paste the URL
3. Choose MP4 or MP3/WebM
4. Click **Download**
5. Watch the status and confirm file saved

---

## ⚠️ Notes & Tips

- Always use **public URLs** to avoid login errors
- Use clean Instagram URLs (e.g., `https://www.instagram.com/reel/xyz/`)
- If MP3 fails, WebM is used as a fallback (no FFmpeg needed)
- Shorter videos = faster processing

---

## 🚀 Deployment

### 🌐 Web App Hosting

- Platforms: PythonAnywhere, Heroku, Render
- Make sure FFmpeg is installed on your server
- Use a WSGI server like **Gunicorn**:
  ```bash
  gunicorn web_app:app
  ```

### 🖥️ Desktop App Distribution

- Upload `.exe` to GitHub or your website
- Bundle FFmpeg in the `dist/` folder
- Ensure GPL license compliance

---

## 🛠️ Troubleshooting

| Problem           | Fix |
|-------------------|-----|
| FFmpeg not working | Ensure ffmpeg/ffprobe are in place |
| Login errors | Use public links only |
| Timeouts | Shorten video length |
| Logs not showing | Check `vidloader.log` in app folder |

---

## 🤝 Contributing

We welcome all contributions!

```bash
# Fork and clone
git clone https://github.com/colloceo/vidloader.git

# Create feature branch
git checkout -b feature/YourFeature

# Make changes and commit
git commit -m "Add YourFeature"

# Push and open a PR
git push origin feature/YourFeature
```

---

## 📝 License

VidLoader is licensed under **GNU GPL v3.0** due to dependencies:

- FFmpeg: GPL
- PyQt5: GPL
- yt-dlp: Unlicense
- Flask: BSD

📄 See `LICENSE` for full details. Distributors must include source code or acquire commercial licenses.

---

## ☕ Support & Contact

- [GitHub Issues](https://github.com/colloceo/vidloader/issues): Bug reports & feature requests
- [GitHub Discussions](https://github.com/colloceo/vilLoader/discussions): Community & help
- [Buy Me a Coffee](https://www.buymeacoffee.com/colloceo): Donate to support development

---

## 🙏 Acknowledgments

- 🧠 `yt_dlp` – Download backend
- 🎧 `FFmpeg` – Audio conversion
- 🌐 `Flask` – Web interface
- 🖥️ `PyQt5` – Desktop GUI

---

> **VidLoader**: *Download videos and audio with ease. Built for content lovers, by content lovers.* 🎬

---
