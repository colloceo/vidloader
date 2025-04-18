# 🎥 VidLoader

**VidLoader** is a free, open-source tool to download videos and audio from major platforms like YouTube, Instagram, TikTok, and X (Twitter). It’s designed to be user-friendly, fast, and cross-platform with two powerful interfaces:

- 🌐 **Web App**: Flask-based web interface (mobile-ready, dark mode supported)
- 🖥️ **Desktop App**: PyQt5 GUI for Windows, macOS, and Linux

---

## 🚀 Features

- 🔻 Download videos (MP4) and audio (MP3/WebM)
- 🌓 Dark mode + 📱 Mobile-responsive UI
- 🖥️ Sleek offline desktop GUI
- ⚡ Fast audio conversion using FFmpeg (`-preset ultrafast`)
- 🔁 WebM fallback if FFmpeg is unavailable
- 🧠 Smart error handling: login issues, geo-restrictions, timeouts
- 📁 Files saved to user's Downloads folder:
  - Windows: `C:\Users\<User>\Downloads`
  - Android: `/sdcard/Download`
- 📝 Logs all activities to `vidloader.log`

---

## 🔧 Installation

### ✅ Prerequisites

- Python 3.8+
- FFmpeg:
  - Windows: [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) or `choco install ffmpeg`
  - Linux: `sudo apt-get install ffmpeg`
  - macOS: `brew install ffmpeg`
- Git

---

## 🌐 Web App Setup

```bash
# Clone the repo
git clone https://github.com/colloceo/VidLoader.git
cd VidLoader/web

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

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

**FFmpeg Setup (Windows):**  
Place `ffmpeg.exe` and `ffprobe.exe` in `VidLoader/ffmpeg/`

**Run locally:**
```bash
python web_app.py
```

Open in browser: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🖥️ Desktop App Setup

```bash
cd VidLoader/desktop

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

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

## 📦 Releases

**VidLoader v1.0.0 - Windows**  
📅 Released: April 18, 2025  
📥 Download: `VidLoader-v1.0.0-Windows.zip`

**Highlights:**
- Windows executable (`VidLoader.exe`) with custom icon
- Download MP4/MP3/WebM from major platforms
- Built with PyQt5 + yt-dlp + FFmpeg

**How to use:**
1. Extract the zip
2. Run `VidLoader.exe`
3. Paste a public video/audio URL
4. Choose format & download

**System Requirements:**
- Windows 7/8/10/11 (64-bit)
- Logs stored in `vidloader.log`

---

## 📦 Build Windows Executable

```bash
pip install pyinstaller==5.13.0
cd desktop

pyinstaller --add-binary "../ffmpeg/ffmpeg.exe;ffmpeg" \
            --add-binary "../ffmpeg/ffprobe.exe;ffmpeg" \
            --add-data "vidloader.log;." \
            --icon "vidloader.ico" \
            -F -w -n VidLoader gui_app.py
```

Built `.exe` will be found in the `dist/` folder.

---

## ✅ Usage

### 🌐 Web App

1. Visit [http://127.0.0.1:5000](http://127.0.0.1:5000)
2. Paste a public URL
3. Select Video or Audio
4. Click **Download Now**

### 🖥️ Desktop App

1. Run `gui_app.py` or `VidLoader.exe`
2. Paste URL
3. Choose format (MP4 / MP3 / WebM)
4. Click **Download**

---

## ⚠️ Notes & Tips

- Use public URLs to avoid login issues
- Use clean Instagram links (e.g. `https://www.instagram.com/reel/xyz/`)
- If MP3 fails, WebM is used as fallback (no FFmpeg required)
- Shorter videos = faster downloads

---

## 🚀 Deployment

### Web Hosting

Platforms: **PythonAnywhere**, **Heroku**, **Render**

- Ensure FFmpeg is installed
- Use Gunicorn for WSGI:  
```bash
gunicorn web_app:app
```

### Desktop Distribution

- Upload `.exe` to GitHub or a website
- Bundle FFmpeg inside `dist/`
- Include GPL license & source code

---

## 🛠️ Troubleshooting

| Problem               | Fix                                             |
|-----------------------|--------------------------------------------------|
| FFmpeg not working    | Ensure `ffmpeg/ffprobe` are in correct folder   |
| Login errors          | Use public links only                          |
| Timeouts              | Try shorter videos                             |
| Logs not showing      | Check `vidloader.log` in app folder            |

---

## 🤝 Contributing

We welcome contributions!

```bash
# Fork and clone
git clone https://github.com/yourusername/VidLoader.git

# Create branch
git checkout -b feature/YourFeature

# Commit and push
git commit -m "Add YourFeature"
git push origin feature/YourFeature
```

Open a Pull Request 🚀

---

## 📝 License

VidLoader is licensed under **GNU GPL v3.0** due to dependencies:

- FFmpeg: GPL
- PyQt5: GPL
- yt-dlp: Unlicense
- Flask: BSD

See `LICENSE` for details. Distributors must provide source code or obtain commercial licenses.

---

## ☕ Support & Contact

- **GitHub Issues** – Bug reports & feature requests  
- **GitHub Discussions** – Community help  
- **Buy Me a Coffee** – Support development ❤️

---

## 🙏 Acknowledgments

- 🧠 **yt-dlp** – Download engine  
- 🎧 **FFmpeg** – Audio processing  
- 🌐 **Flask** – Web interface  
- 🖥️ **PyQt5** – Desktop GUI

---

> **VidLoader:** Download videos and audio with ease.  
> _Built for content lovers, by content lovers._ 🎬
