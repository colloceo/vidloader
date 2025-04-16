from flask import Flask, render_template, request, send_file, jsonify, make_response
import yt_dlp
import os
import uuid
from werkzeug.utils import secure_filename
from concurrent.futures import ThreadPoolExecutor, TimeoutError

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'

# Ensure downloads folder exists
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    format_type = request.form.get('format', 'video')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    # Generate unique filename
    filename_base = str(uuid.uuid4())
    extension = 'mp3' if format_type == 'audio' else 'mp4'
    filename = f"{filename_base}.{extension}"
    output_path = os.path.join(DOWNLOAD_FOLDER, filename)

    ydl_opts = {
        'outtmpl': output_path,
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
    }

    if format_type == 'audio':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'

    def download_with_ydl():
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    try:
        # Run download in a thread with a timeout
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(download_with_ydl)
            future.result(timeout=60)  # 60-second timeout

        # Find the downloaded file
        for file in os.listdir(DOWNLOAD_FOLDER):
            if file.startswith(filename_base):
                file_path = os.path.join(DOWNLOAD_FOLDER, file)
                # Set explicit filename for download
                safe_filename = secure_filename(file) if format_type == 'audio' else f"video_{filename_base}.mp4"
                response = make_response(send_file(
                    file_path,
                    as_attachment=True,
                    download_name=safe_filename
                ))
                response.headers['Content-Disposition'] = f'attachment; filename="{safe_filename}"'
                # Clean up after sending
                @response.call_on_close
                def cleanup():
                    try:
                        os.remove(file_path)
                    except Exception:
                        pass
                return response

        return jsonify({'error': 'File not found after download'}), 500

    except yt_dlp.utils.DownloadError as e:
        return jsonify({'error': 'Failed to download: Invalid or unsupported URL'}), 400
    except TimeoutError:
        return jsonify({'error': 'Download timed out. Please try a shorter video or check the URL.'}), 504
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/cleanup', methods=['POST'])
def cleanup_downloads():
    """Clean up all files in the downloads folder."""
    try:
        for file in os.listdir(DOWNLOAD_FOLDER):
            file_path = os.path.join(DOWNLOAD_FOLDER, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        return jsonify({'message': 'Downloads folder cleaned up'}), 200
    except Exception as e:
        return jsonify({'error': f'Cleanup failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)