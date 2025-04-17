from flask import Flask, render_template, request, send_file, jsonify, make_response
import yt_dlp
import os
import uuid
from werkzeug.utils import secure_filename
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import logging
from threading import Lock

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'
download_lock = Lock()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def home():
    logger.debug("Serving home page")
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    format_type = request.form.get('format', 'video')

    if not url:
        logger.error("No URL provided")
        return jsonify({'error': 'URL is required'}), 400

    logger.debug(f"Processing download for URL: {url}, Format: {format_type}")

    filename_base = str(uuid.uuid4())
    extension = 'mp3' if format_type == 'audio' else 'mp4'
    filename = f"{filename_base}.{extension}"
    output_path = os.path.join(DOWNLOAD_FOLDER, filename)

    ydl_opts = {
        'outtmpl': output_path,
        'noplaylist': True,
        'quiet': False,
        'no_warnings': False,
        'logger': logger,
    }

    if format_type == 'audio':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'postprocessor_args': ['-loglevel', 'error', '-threads', '1', '-preset', 'ultrafast'],  # Optimize FFmpeg
        })
    else:
        ydl_opts['format'] = 'best[ext=mp4]/best'

    def download_with_ydl():
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            logger.error(f"yt_dlp download failed: {str(e)}")
            raise

    try:
        logger.debug("Starting download process")
        with download_lock:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(download_with_ydl)
                timeout = 600 if format_type == 'audio' and 'instagram.com' in url.lower() else 300
                future.result(timeout=timeout)

        logger.debug("Download completed, checking for file")
        for file in os.listdir(DOWNLOAD_FOLDER):
            if file.startswith(filename_base):
                file_path = os.path.join(DOWNLOAD_FOLDER, file)
                safe_filename = f"audio_{filename_base}.mp3" if format_type == 'audio' else f"video_{filename_base}.mp4"
                logger.debug(f"Sending file: {safe_filename}")
                response = make_response(send_file(
                    file_path,
                    as_attachment=True,
                    download_name=safe_filename
                ))
                response.headers['Content-Disposition'] = f'attachment; filename="{safe_filename}"'
                @response.call_on_close
                def cleanup():
                    try:
                        logger.debug(f"Cleaning up file: {file_path}")
                        os.remove(file_path)
                    except Exception as e:
                        logger.error(f"Cleanup failed: {str(e)}")
                return response

        logger.error("File not found after download")
        return jsonify({'error': 'File not found after download'}), 500

    except yt_dlp.utils.DownloadError as e:
        error_msg = str(e).lower()
        logger.error(f"DownloadError: {error_msg}")
        if 'ffmpeg' in error_msg or 'ffprobe' in error_msg:
            if format_type == 'audio':
                logger.debug("Falling back to raw audio download")
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [],
                })
                filename = f"{filename_base}.webm"
                output_path = os.path.join(DOWNLOAD_FOLDER, filename)
                try:
                    with download_lock:
                        with ThreadPoolExecutor(max_workers=1) as executor:
                            future = executor.submit(download_with_ydl)
                            future.result(timeout=180)
                    for file in os.listdir(DOWNLOAD_FOLDER):
                        if file.startswith(filename_base):
                            file_path = os.path.join(DOWNLOAD_FOLDER, file)
                            safe_filename = f"audio_{filename_base}.webm"
                            response = make_response(send_file(
                                file_path,
                                as_attachment=True,
                                download_name=safe_filename
                            ))
                            response.headers['Content-Disposition'] = f'attachment; filename="{safe_filename}"'
                            @response.call_on_close
                            def cleanup():
                                try:
                                    os.remove(file_path)
                                except Exception as e:
                                    logger.error(f"Cleanup failed: {str(e)}")
                            return response
                    return jsonify({'error': 'Fallback file not found'}), 500
                except Exception as fallback_e:
                    logger.error(f"Fallback download failed: {str(fallback_e)}")
                    return jsonify({'error': 'Audio download failed. Try video format or ensure FFmpeg is installed.'}), 400
            return jsonify({'error': 'FFmpeg error: Please ensure FFmpeg is installed and accessible.'}), 400
        elif 'sign in' in error_msg or 'login' in error_msg:
            return jsonify({'error': 'This content requires login. Please use a publicly accessible URL.'}), 403
        elif 'geo-restricted' in error_msg:
            return jsonify({'error': 'This content is geo-restricted and cannot be downloaded.'}), 403
        elif 'not available' in error_msg or 'unavailable' in error_msg:
            return jsonify({'error': 'The video is not available or private.'}), 404
        return jsonify({'error': f'Failed to download: {str(e)}'}), 400
    except TimeoutError:
        logger.error(f"Download timed out after {timeout} seconds")
        return jsonify({'error': 'Download timed out. Try a shorter video, check your network, or select video format.'}), 504
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@app.route('/cleanup', methods=['POST'])
def cleanup_downloads():
    try:
        for file in os.listdir(DOWNLOAD_FOLDER):
            file_path = os.path.join(DOWNLOAD_FOLDER, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        logger.debug("Downloads folder cleaned up")
        return jsonify({'message': 'Downloads folder cleaned up'}), 200
    except Exception as e:
        logger.error(f"Cleanup failed: {str(e)}")
        return jsonify({'error': f'Cleanup failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=False)